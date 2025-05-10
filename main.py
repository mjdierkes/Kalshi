import os
import sys
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
import asyncio
import json
from datetime import datetime
import csv
import pandas as pd
import time
import concurrent.futures
from functools import partial
from tqdm import tqdm

from clients import KalshiHttpClient, KalshiWebSocketClient, Environment

# Load environment variables
load_dotenv()
env = Environment.DEMO  # toggle environment here
KEYID = os.getenv('DEMO_KEYID') if env == Environment.DEMO else os.getenv('PROD_KEYID')
KEYFILE = os.getenv('DEMO_KEYFILE') if env == Environment.DEMO else os.getenv('PROD_KEYFILE')

# Set the maximum number of concurrent workers based on your machine
NUM_WORKERS = 16  # Adjust based on your M2 performance

try:
    with open(KEYFILE, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None  # Provide the password if your key is encrypted
        )
except FileNotFoundError:
    raise FileNotFoundError(f"Private key file not found at {KEYFILE}")
except Exception as e:
    raise Exception(f"Error loading private key: {str(e)}")

# Initialize the HTTP client with performance settings
client = KalshiHttpClient(
    key_id=KEYID,
    private_key=private_key,
    environment=env,
    max_workers=NUM_WORKERS,
    rate_limit_ms=25  # More aggressive rate limit
)

# Create a list to store all market data
all_market_data = []

# WebSocket message handler
def handle_market_update(message_data):
    if 'message' in message_data and 'ticker' in message_data['message']:
        # Process and update market data in real-time
        ticker = message_data['message'].get('ticker')
        print(f"Received update for {ticker}")
        # TODO: Add more processing as needed

# Async function to fetch all market data
async def fetch_all_market_data():
    start_time = time.time()
    
    print("Fetching account balance...")
    # Get account balance
    balance = client.get_balance()
    print("Balance:", balance)
    
    print("\nFetching election events...")
    # Get election events with pagination
    all_events = []
    cursor = None
    
    with tqdm(desc="Fetching events", unit="page") as pbar:
        while True:
            events_response = client.get_events(
                status="open,closed",  # Get both open and closed markets
                with_nested_markets=True,
                limit=200,  # Maximum limit per request
                cursor=cursor
            )
            
            if not events_response.get('events'):
                break
                
            all_events.extend(events_response.get('events', []))
            cursor = events_response.get('cursor')
            pbar.update(1)
            
            if not cursor:
                break
    
    print(f"\nFound {len(all_events)} events")
    
    # Collect all market tickers across all events
    all_tickers = []
    event_market_map = {}  # Map tickers to their events
    
    print("\nOrganizing markets by events...")
    for event in all_events:
        if 'markets' in event:
            event_tickers = [market['ticker'] for market in event['markets']]
            all_tickers.extend(event_tickers)
            
            # Map each ticker to its event
            for ticker in event_tickers:
                event_market_map[ticker] = event['event_ticker']
    
    total_markets = len(all_tickers)
    print(f"\nFetching details for {total_markets} markets in parallel...")
    
    # Split tickers into chunks to avoid overwhelming the API
    chunk_size = 50
    market_details_list = []
    num_chunks = (total_markets + chunk_size - 1) // chunk_size
    
    # Create progress bar for chunks
    with tqdm(total=total_markets, desc="Fetching market details", unit="market") as pbar:
        for i in range(0, total_markets, chunk_size):
            chunk = all_tickers[i:i + chunk_size]
            chunk_results = await client.get_markets_async(chunk)
            market_details_list.extend(chunk_results)
            pbar.update(len(chunk))
            
            # Small delay between chunks to avoid rate limits
            await asyncio.sleep(0.1)
    
    print("\nProcessing market data...")
    # Process market details and create data records
    with tqdm(total=len(market_details_list), desc="Processing markets", unit="market") as pbar:
        for i, market_details in enumerate(market_details_list):
            ticker = all_tickers[i]
            event_ticker = event_market_map.get(ticker, 'N/A')
            
            # Find the event data
            event_data = next((e for e in all_events 
                             if e['event_ticker'] == event_ticker), {})
            
            # Skip if there was an error fetching this market
            if isinstance(market_details, dict) and 'error' in market_details:
                print(f"Error fetching details for {ticker}: {market_details['error']}")
                pbar.update(1)
                continue
                
            # Create a dictionary for this market's data
            market_data = {
                'event_ticker': event_ticker,
                'event_category': event_data.get('category', 'N/A'),
                'market_title': market_details.get('title', 'N/A'),
                'market_ticker': market_details.get('ticker', 'N/A'),
                'status': market_details.get('status', 'N/A'),
                'market_type': market_details.get('market_type', 'N/A'),
                'close_time': market_details.get('close_time', 'N/A'),
                'last_price': market_details.get('last_price', 0) / 100 if market_details.get('last_price') is not None else None,
                'yes_bid': market_details.get('yes_bid', 0) / 100 if market_details.get('yes_bid') is not None else None,
                'yes_ask': market_details.get('yes_ask', 0) / 100 if market_details.get('yes_ask') is not None else None,
                'volume_24h': market_details.get('volume_24h', 0),
                'open_interest': market_details.get('open_interest', 0),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            all_market_data.append(market_data)
            pbar.update(1)
    
    # Group markets by event for display
    print("\nGrouping markets by event...")
    markets_by_event = {}
    for market_data in all_market_data:
        event_ticker = market_data['event_ticker']
        if event_ticker not in markets_by_event:
            markets_by_event[event_ticker] = []
        markets_by_event[event_ticker].append(market_data)
    
    # Print summary by event
    print("\nSummary of Events:")
    total_markets = 0
    for event_ticker, markets in markets_by_event.items():
        if not markets:
            continue
            
        total_markets += len(markets)
        print(f"\nEvent: {event_ticker}")
        print(f"Category: {markets[0]['event_category']}")
        print(f"Number of markets: {len(markets)}")
        
        # Show sample markets
        sample_size = min(3, len(markets))
        print(f"Sample markets:")
        for i in range(sample_size):
            market = markets[i]
            print(f"  {market['market_title']} ({market['market_ticker']}): " + 
                  (f"{market['last_price']:.1%}" if market['last_price'] is not None else "No price"))
    
    print(f"\nTotal number of markets found: {total_markets}")        
    print("\nNote: Prices shown as percentages (e.g., 55.0% means $0.55 per share)")
    
    # Export data to CSV
    if all_market_data:
        print("\nExporting data to CSV...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'kalshi_markets_{timestamp}.csv'
        
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(all_market_data)
        df.to_csv(csv_filename, index=False)
        print(f"Data exported to {csv_filename}")
    
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

# WebSocket event handler
async def handle_websocket():
    # Initialize the WebSocket client
    ws_client = KalshiWebSocketClient(
        key_id=KEYID,
        private_key=private_key,
        environment=env,
        max_workers=NUM_WORKERS,
    )
    
    # Add message handler
    ws_client.add_message_handler(handle_market_update)
    
    # Connect via WebSocket
    await ws_client.connect()

async def main():
    """Main async function to run both data fetching and websocket."""
    # Run the market data fetching
    await fetch_all_market_data()
    
    # Ask if user wants to start WebSocket listening
    response = input("\nDo you want to start real-time WebSocket updates? (y/n): ")
    if response.lower() == 'y':
        print("Starting WebSocket connection...")
        await handle_websocket()
    else:
        print("Exiting without starting WebSocket.")

if __name__ == "__main__":
    # Check if we're in IPython/Jupyter
    try:
        import IPython
        if IPython.get_ipython() is not None:
            # In Jupyter, we need to use asyncio.ensure_future
            future = asyncio.ensure_future(main())
        else:
            # Regular Python
            asyncio.run(main())
    except (ImportError, AttributeError):
        # Regular Python
        asyncio.run(main())