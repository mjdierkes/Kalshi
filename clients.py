import requests
import base64
import time
from typing import Any, Dict, Optional, List, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
import asyncio
import concurrent.futures
import random

from requests.exceptions import HTTPError

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

import websockets

class Environment(Enum):
    DEMO = "demo"
    PROD = "prod"

class KalshiBaseClient:
    """Base client class for interacting with the Kalshi API."""
    def __init__(
        self,
        key_id: str,
        private_key: rsa.RSAPrivateKey,
        environment: Environment = Environment.DEMO,
        max_workers: int = 10
    ):
        """Initializes the client with the provided API key and private key.

        Args:
            key_id (str): Your Kalshi API key ID.
            private_key (rsa.RSAPrivateKey): Your RSA private key.
            environment (Environment): The API environment to use (DEMO or PROD).
            max_workers (int): Maximum number of worker threads for parallel requests.
        """
        self.key_id = key_id
        self.private_key = private_key
        self.environment = environment
        self.last_api_call = datetime.now()
        self.max_workers = max_workers
        self.rate_limit_lock = asyncio.Lock() if asyncio.get_event_loop_policy().get_event_loop().is_running() else None
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        if self.environment == Environment.DEMO:
            self.HTTP_BASE_URL = "https://demo-api.kalshi.co"
            self.WS_BASE_URL = "wss://demo-api.kalshi.co"
        elif self.environment == Environment.PROD:
            self.HTTP_BASE_URL = "https://api.elections.kalshi.com"
            self.WS_BASE_URL = "wss://api.elections.kalshi.com"
        else:
            raise ValueError("Invalid environment")

    def request_headers(self, method: str, path: str) -> Dict[str, Any]:
        """Generates the required authentication headers for API requests."""
        current_time_milliseconds = int(time.time() * 1000)
        timestamp_str = str(current_time_milliseconds)

        # Remove query params from path
        path_parts = path.split('?')

        msg_string = timestamp_str + method + path_parts[0]
        signature = self.sign_pss_text(msg_string)

        headers = {
            "Content-Type": "application/json",
            "KALSHI-ACCESS-KEY": self.key_id,
            "KALSHI-ACCESS-SIGNATURE": signature,
            "KALSHI-ACCESS-TIMESTAMP": timestamp_str,
        }
        return headers

    def sign_pss_text(self, text: str) -> str:
        """Signs the text using RSA-PSS and returns the base64 encoded signature."""
        message = text.encode('utf-8')
        try:
            signature = self.private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.DIGEST_LENGTH
                ),
                hashes.SHA256()
            )
            return base64.b64encode(signature).decode('utf-8')
        except InvalidSignature as e:
            raise ValueError("RSA sign PSS failed") from e

class KalshiHttpClient(KalshiBaseClient):
    """Client for handling HTTP connections to the Kalshi API."""
    def __init__(
        self,
        key_id: str,
        private_key: rsa.RSAPrivateKey,
        environment: Environment = Environment.DEMO,
        max_workers: int = 10,
        rate_limit_per_second: int = 8,  # Default to slightly under Basic tier's 10 reads/second
        adaptive_rate_limiting: bool = True
    ):
        super().__init__(key_id, private_key, environment, max_workers)
        self.host = self.HTTP_BASE_URL
        self.exchange_url = "/trade-api/v2/exchange"
        self.markets_url = "/trade-api/v2/markets"
        self.portfolio_url = "/trade-api/v2/portfolio"
        self.events_url = "/trade-api/v2/events"
        self.rate_limit_per_second = rate_limit_per_second
        self.adaptive_rate_limiting = adaptive_rate_limiting
        
        # Configure session with connection pooling for better performance
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=max_workers,
            pool_maxsize=max_workers * 2,
            max_retries=3
        )
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        
        self._last_requests = []  # Track the timestamps of last N requests
        self._request_times_lock = asyncio.Lock() if asyncio.get_event_loop_policy().get_event_loop().is_running() else None

    def _adaptive_rate_limit(self) -> None:
        """Adaptive rate limiter that adjusts based on recent request history and configured limits."""
        now = datetime.now()
        
        # Keep only timestamps from the last second
        self._last_requests = [ts for ts in self._last_requests if (now - ts).total_seconds() < 1.0]
        
        # Add current timestamp
        self._last_requests.append(now)
        
        # If we have more than our rate limit in the last second, sleep to respect the limit
        if len(self._last_requests) > self.rate_limit_per_second:
            sleep_time = max(0, 1.0 - (now - self._last_requests[0]).total_seconds())
            if sleep_time > 0:
                time.sleep(sleep_time)

    async def async_rate_limit(self) -> None:
        """Asynchronous rate limiter for use with async functions."""
        if self._request_times_lock:
            async with self._request_times_lock:
                if self.adaptive_rate_limiting:
                    self._adaptive_rate_limit()
                else:
                    # Simple rate limiting - space requests evenly
                    await asyncio.sleep(1.0 / self.rate_limit_per_second)
        else:
            if self.adaptive_rate_limiting:
                self._adaptive_rate_limit()
            else:
                # Simple rate limiting - space requests evenly
                time.sleep(1.0 / self.rate_limit_per_second)

    def rate_limit(self) -> None:
        """Non-async version of rate limiter."""
        if self.adaptive_rate_limiting:
            self._adaptive_rate_limit()
        else:
            # Simple rate limiting - space requests evenly
            time.sleep(1.0 / self.rate_limit_per_second)

    def raise_if_bad_response(self, response: requests.Response) -> None:
        """Raises an HTTPError if the response status code indicates an error."""
        if response.status_code not in range(200, 299):
            response.raise_for_status()

    def post(self, path: str, body: dict) -> Any:
        """Performs an authenticated POST request to the Kalshi API."""
        self.rate_limit()
        response = self._session.post(
            self.host + path,
            json=body,
            headers=self.request_headers("POST", path)
        )
        self.raise_if_bad_response(response)
        return response.json()

    def get(self, path: str, params: Dict[str, Any] = {}) -> Any:
        """Performs an authenticated GET request to the Kalshi API."""
        self.rate_limit()
        response = self._session.get(
            self.host + path,
            headers=self.request_headers("GET", path),
            params=params
        )
        self.raise_if_bad_response(response)
        return response.json()

    def delete(self, path: str, params: Dict[str, Any] = {}) -> Any:
        """Performs an authenticated DELETE request to the Kalshi API."""
        self.rate_limit()
        response = self._session.delete(
            self.host + path,
            headers=self.request_headers("DELETE", path),
            params=params
        )
        self.raise_if_bad_response(response)
        return response.json()
        
    def batch_get(self, paths: List[str], params_list: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """Performs multiple GET requests in parallel using a thread pool.
        
        Args:
            paths: List of API paths to request
            params_list: Optional list of params dictionaries for each request
        
        Returns:
            List of API responses
        """
        if params_list is None:
            params_list = [{} for _ in paths]
            
        if len(paths) != len(params_list):
            raise ValueError("paths and params_list must have the same length")
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.get, path, params)
                for path, params in zip(paths, params_list)
            ]
            
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
                    
        return results
        
    async def async_get(self, path: str, params: Dict[str, Any] = {}, retries: int = 3) -> Any:
        """Async version of the GET method with retry logic."""
        await self.async_rate_limit()
        
        loop = asyncio.get_event_loop()
        attempt = 0
        last_error = None

        while attempt < retries:
            try:
                response = await loop.run_in_executor(
                    self.thread_executor,
                    lambda: self._session.get(
                        self.host + path,
                        headers=self.request_headers("GET", path),
                        params=params,
                        timeout=(3.0, 10.0)  # (connect timeout, read timeout)
                    )
                )
                
                self.raise_if_bad_response(response)
                return response.json()
            except (requests.RequestException, HTTPError) as e:
                attempt += 1
                last_error = e
                if attempt < retries:
                    # Exponential backoff with jitter
                    backoff = 0.1 * (2 ** attempt) + (random.random() * 0.1)
                    await asyncio.sleep(backoff)
        
        # If we get here, all retries failed
        if last_error:
            return {"error": str(last_error)}
        return {"error": "Unknown error during request"}
        
    async def async_batch_get(self, paths: List[str], params_list: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """Performs multiple GET requests in parallel using asyncio with concurrency control.
        
        Args:
            paths: List of API paths to request
            params_list: Optional list of params dictionaries for each request
        
        Returns:
            List of API responses
        """
        if params_list is None:
            params_list = [{} for _ in paths]
            
        if len(paths) != len(params_list):
            raise ValueError("paths and params_list must have the same length")
        
        # Set max concurrent tasks but not more than we have workers
        # This prevents overwhelming the connection pool or the API
        semaphore = asyncio.Semaphore(min(20, self.max_workers))
        
        async def fetch_with_semaphore(path, params):
            async with semaphore:
                return await self.async_get(path, params)
        
        tasks = [
            fetch_with_semaphore(path, params)
            for path, params in zip(paths, params_list)
        ]
        
        return await asyncio.gather(*tasks, return_exceptions=True)

    def get_balance(self) -> Dict[str, Any]:
        """Retrieves the account balance."""
        return self.get(self.portfolio_url + '/balance')

    def get_exchange_status(self) -> Dict[str, Any]:
        """Retrieves the exchange status."""
        return self.get(self.exchange_url + "/status")

    def get_trades(
        self,
        ticker: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        max_ts: Optional[int] = None,
        min_ts: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieves trades based on provided filters."""
        params = {
            'ticker': ticker,
            'limit': limit,
            'cursor': cursor,
            'max_ts': max_ts,
            'min_ts': min_ts,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.get(self.markets_url + '/trades', params=params)

    def get_events(
        self,
        status: Optional[str] = None,
        series_ticker: Optional[str] = None,
        with_nested_markets: bool = True,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieves events based on provided filters.
        
        Args:
            status: Comma separated list of statuses (unopened, open, closed, settled)
            series_ticker: Series ticker to retrieve contracts for
            with_nested_markets: Include nested market data in response
            limit: Number of results per page (1-200)
            cursor: Pagination cursor from previous request
            
        Returns:
            Dict containing events data and pagination cursor
        """
        params = {
            'status': status,
            'series_ticker': series_ticker,
            'with_nested_markets': str(with_nested_markets).lower(),
            'limit': limit,
            'cursor': cursor,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        response = self.get(self.events_url, params=params)
        
        # Add cursor to response if it exists in headers
        if 'cursor' in response:
            return response
        elif 'next_cursor' in response:
            response['cursor'] = response['next_cursor']
            return response
        else:
            response['cursor'] = None
            return response
        
    def get_markets_batch(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """Retrieve multiple markets in parallel.
        
        Args:
            tickers: List of market ticker symbols
            
        Returns:
            List of market details dictionaries
        """
        paths = [f"{self.markets_url}/{ticker}" for ticker in tickers]
        results = self.batch_get(paths)
        
        # Extract the 'market' field from each result
        return [r.get('market', r) for r in results]
        
    async def get_markets_async(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """Retrieve multiple markets in parallel using async.
        
        Args:
            tickers: List of market ticker symbols
            
        Returns:
            List of market details dictionaries
        """
        paths = [f"{self.markets_url}/{ticker}" for ticker in tickers]
        results = await self.async_batch_get(paths)
        
        # Extract the 'market' field from each result and handle exceptions
        markets = []
        for r in results:
            if isinstance(r, Exception):
                markets.append({"error": str(r)})
            else:
                markets.append(r.get('market', r))
        
        return markets

    def get_market(self, ticker: str) -> Dict[str, Any]:
        """Retrieves detailed information about a specific market.
        
        Args:
            ticker: Market ticker symbol
            
        Returns:
            Dict containing market details
        """
        return self.get(f"{self.markets_url}/{ticker}")

class KalshiWebSocketClient(KalshiBaseClient):
    """Client for handling WebSocket connections to the Kalshi API."""
    def __init__(
        self,
        key_id: str,
        private_key: rsa.RSAPrivateKey,
        environment: Environment = Environment.DEMO,
        max_workers: int = 10,
    ):
        super().__init__(key_id, private_key, environment, max_workers)
        self.ws = None
        self.url_suffix = "/trade-api/ws/v2"
        self.message_id = 1  # Add counter for message IDs
        self.reconnect_delay = 1  # Initial reconnect delay in seconds
        self.max_reconnect_delay = 30  # Maximum reconnect delay
        self.message_handlers = []  # List of message handler callbacks

    async def connect(self, auto_reconnect=True):
        """Establishes a WebSocket connection using authentication."""
        host = self.WS_BASE_URL + self.url_suffix
        auth_headers = self.request_headers("GET", self.url_suffix)
        
        while True:
            try:
                async with websockets.connect(host, additional_headers=auth_headers) as websocket:
                    self.ws = websocket
                    self.reconnect_delay = 1  # Reset reconnect delay on successful connection
                    await self.on_open()
                    await self.handler()
            except Exception as e:
                await self.on_error(e)
                
                if not auto_reconnect:
                    break
                    
                # Exponential backoff for reconnect
                print(f"Reconnecting in {self.reconnect_delay} seconds...")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)

    def add_message_handler(self, handler: Callable[[dict], None]):
        """Add a callback function to handle incoming messages."""
        self.message_handlers.append(handler)

    async def on_open(self):
        """Callback when WebSocket connection is opened."""
        print("WebSocket connection opened.")
        await self.subscribe_to_tickers()

    async def subscribe_to_tickers(self, tickers=None):
        """Subscribe to ticker updates for markets.
        
        Args:
            tickers: Optional list of specific tickers to subscribe to. If None, subscribes to all.
        """
        params = {"channels": ["ticker"]}
        if tickers:
            params["tickers"] = tickers
            
        subscription_message = {
            "id": self.message_id,
            "cmd": "subscribe",
            "params": params
        }
        await self.ws.send(json.dumps(subscription_message))
        self.message_id += 1

    async def handler(self):
        """Handle incoming messages."""
        try:
            async for message in self.ws:
                await self.on_message(message)
        except websockets.ConnectionClosed as e:
            await self.on_close(e.code, e.reason)
        except Exception as e:
            await self.on_error(e)

    async def on_message(self, message):
        """Callback for handling incoming messages."""
        try:
            data = json.loads(message)
            
            # Process with all registered handlers
            for handler in self.message_handlers:
                # Run handlers in executor to avoid blocking the event loop
                await asyncio.get_event_loop().run_in_executor(
                    self.thread_executor, 
                    handler, 
                    data
                )
        except Exception as e:
            print(f"Error processing message: {e}")
        
        # For backward compatibility
        print("Received message:", message)

    async def on_error(self, error):
        """Callback for handling errors."""
        print("WebSocket error:", error)

    async def on_close(self, close_status_code, close_msg):
        """Callback when WebSocket connection is closed."""
        print("WebSocket connection closed with code:", close_status_code, "and message:", close_msg)