import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
import json
from typing import Dict, List, Optional
from py_clob_client.constants import END_CURSOR
import csv
from datetime import datetime
from py_clob_client.clob_types import BookParams
import concurrent.futures
from tqdm import tqdm
import time
from functools import lru_cache

# Load environment variables
load_dotenv()

def get_market_type(market: Dict) -> str:
    """Determine the type of market based on its characteristics"""
    if not market or 'tokens' not in market:
        return "Unknown"
        
    tokens = market['tokens']
    if len(tokens) != 2:
        return "Unknown"
        
    outcomes = [t['outcome'].lower() for t in tokens]
    
    # Check for Yes/No markets
    if 'yes' in outcomes and 'no' in outcomes:
        return "Binary"
        
    # Check for sports teams
    sports_keywords = ['vs', 'fc', 'united', 'city', 'warriors', 'lakers', 'celtics', 'bulls', 'eagles', 'chiefs']
    if any(keyword in outcome.lower() for keyword in sports_keywords for outcome in outcomes):
        return "Sports"
        
    # Check for crypto markets
    crypto_keywords = ['btc', 'eth', 'bitcoin', 'ethereum', 'crypto']
    if any(keyword in outcome.lower() for keyword in crypto_keywords for outcome in outcomes):
        return "Crypto"
        
    return "Other"

def get_market_status(market: Dict) -> str:
    """Get the market status as a single string"""
    status = []
    if market['active']: status.append("Active")
    if market['closed']: status.append("Closed")
    if market['archived']: status.append("Archived")
    if market['accepting_orders']: status.append("Accepting Orders")
    return ", ".join(status)

def format_market_info(market: Dict) -> str:
    """Format market information into a readable string"""
    if not market or 'tokens' not in market:
        return "Invalid market data"
        
    market_type = get_market_type(market)
    title = market.get('title', 'No title available')
    question = market.get('question', 'No question available')
    outcomes = " vs ".join([f"{t['outcome']}({t['price']})" for t in market['tokens']])
    status = get_market_status(market)
    
    return f"[{market_type}] {title}\nQuestion: {question}\nOutcomes: {outcomes}\nStatus: [{status}]"

@lru_cache(maxsize=128)
def get_order_book(client: ClobClient, token_id: str) -> Dict:
    """Get order book with caching"""
    try:
        order_book = client.get_order_book(token_id)
        return {
            'bids': [{'price': b.price, 'size': b.size} for b in order_book.bids] if order_book.bids else [],
            'asks': [{'price': a.price, 'size': a.size} for a in order_book.asks] if order_book.asks else []
        }
    except Exception as e:
        return {'error': str(e)}

@lru_cache(maxsize=128)
def get_midpoint(client: ClobClient, token_id: str) -> Optional[float]:
    """Get midpoint with caching"""
    try:
        mid_price = client.get_midpoint(token_id)
        return mid_price.get('mid')
    except Exception:
        return None

@lru_cache(maxsize=128)
def get_last_trade_price(client: ClobClient, token_id: str) -> Optional[float]:
    """Get last trade price with caching"""
    try:
        last_trade = client.get_last_trade_price(token_id)
        return last_trade.get('price')
    except Exception:
        return None

@lru_cache(maxsize=128)
def get_spread(client: ClobClient, token_id: str) -> Optional[float]:
    """Get spread with caching"""
    try:
        spread = client.get_spread(token_id)
        return spread.get('spread')
    except Exception:
        return None

def get_market_details(client: ClobClient, market: Dict) -> Dict:
    """Get additional market details including order book, prices, and trading info"""
    try:
        token_id = market['tokens'][0]['token_id'] if market.get('tokens') else None
        if not token_id:
            return {}
            
        details = {}
        
        # Use the cached functions
        details['order_book'] = get_order_book(client, token_id)
        details['mid_price'] = get_midpoint(client, token_id)
        details['last_trade_price'] = get_last_trade_price(client, token_id)
        details['spread'] = get_spread(client, token_id)
            
        return details
    except Exception as e:
        return {'error': str(e)}

def process_market_details(client: ClobClient, market: Dict) -> Dict:
    """Process a single market with details for threading"""
    market_result = market.copy()
    market_result['details'] = get_market_details(client, market)
    return market_result

def export_markets_to_csv(markets: List[Dict], filename: str):
    """Export markets data to a CSV file"""
    fieldnames = [
        'Market Type',
        'Title',
        'Question',
        'Status',
        'Outcome 1',
        'Price 1',
        'Outcome 2',
        'Price 2',
        'Market ID',
        'Created At',
        'Updated At',
        'Mid Price',
        'Last Trade Price',
        'Spread',
        'Order Book Bids',
        'Order Book Asks',
        'Total Bid Volume',
        'Total Ask Volume'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for market in markets:
            if 'tokens' in market and len(market['tokens']) == 2:
                # Get details
                details = market.get('details', {})
                
                # Calculate total volumes
                total_bid_volume = sum(float(bid['size']) for bid in details.get('order_book', {}).get('bids', []))
                total_ask_volume = sum(float(ask['size']) for ask in details.get('order_book', {}).get('asks', []))
                
                writer.writerow({
                    'Market Type': get_market_type(market),
                    'Title': market.get('title', ''),
                    'Question': market.get('question', ''),
                    'Status': get_market_status(market),
                    'Outcome 1': market['tokens'][0]['outcome'],
                    'Price 1': market['tokens'][0]['price'],
                    'Outcome 2': market['tokens'][1]['outcome'],
                    'Price 2': market['tokens'][1]['price'],
                    'Market ID': market.get('market_id', ''),
                    'Created At': market.get('created_at', ''),
                    'Updated At': market.get('updated_at', ''),
                    'Mid Price': details.get('mid_price'),
                    'Last Trade Price': details.get('last_trade_price'),
                    'Spread': details.get('spread'),
                    'Order Book Bids': json.dumps(details.get('order_book', {}).get('bids', [])),
                    'Order Book Asks': json.dumps(details.get('order_book', {}).get('asks', [])),
                    'Total Bid Volume': total_bid_volume,
                    'Total Ask Volume': total_ask_volume
                })

def fetch_markets_batch(client: ClobClient, cursor: str, batch_size: int = 50):
    """Fetch a batch of markets starting from a cursor"""
    response = client.get_markets(next_cursor=cursor)
    if isinstance(response, dict) and 'data' in response:
        markets = response['data']
        next_cursor = response.get('next_cursor', END_CURSOR)
        return markets, next_cursor
    return [], END_CURSOR

def list_markets():
    """List all available markets on Polymarket CLOB"""
    try:
        # Initialize the client with minimal configuration
        client = ClobClient(
            host="https://clob.polymarket.com"  # Polymarket mainnet CLOB endpoint
        )
        
        # First pass: Just fetch all market IDs to get total count
        print("Estimating total markets...")
        markets_count = 0
        temp_cursor = "MA=="  # Initial cursor
        while temp_cursor != END_CURSOR:
            batch, temp_cursor = fetch_markets_batch(client, temp_cursor)
            markets_count += len(batch)
        
        print(f"Found approximately {markets_count} markets")
        
        # Create a single progress bar for the entire process
        with tqdm(total=markets_count*2, desc="Fetching and processing markets") as pbar:
            # Fetch all markets
            all_markets = []
            next_cursor = "MA=="  # Initial cursor
            while next_cursor != END_CURSOR:
                batch, next_cursor = fetch_markets_batch(client, next_cursor)
                all_markets.extend(batch)
                pbar.update(len(batch))
            
            # Create a thread pool with a reasonable number of workers
            # On M2 with 32GB RAM, we can use a higher number of workers
            max_workers = min(32, os.cpu_count() * 4)  # Adjust based on your needs
            
            # Process markets in parallel
            processed_markets = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks
                future_to_market = {
                    executor.submit(process_market_details, client, market): i
                    for i, market in enumerate(all_markets)
                }
                
                # Process results as they complete
                for future in concurrent.futures.as_completed(future_to_market):
                    processed_market = future.result()
                    processed_markets.append(processed_market)
                    pbar.update(1)
        
        # Export to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"polymarket_markets_{timestamp}.csv"
        print(f"\nExporting market data to {csv_filename}")
        export_markets_to_csv(processed_markets, csv_filename)
        print(f"Export complete!")
            
        # Group markets by type and status
        active_markets = {'Binary': [], 'Sports': [], 'Crypto': [], 'Other': []}
        closed_markets = {'Binary': [], 'Sports': [], 'Crypto': [], 'Other': []}
        archived_markets = {'Binary': [], 'Sports': [], 'Crypto': [], 'Other': []}
        
        for market in processed_markets:
            market_type = get_market_type(market)
            if market_type not in active_markets:
                active_markets[market_type] = []
                closed_markets[market_type] = []
                archived_markets[market_type] = []
                
            if market['active'] and market['accepting_orders']:
                active_markets[market_type].append(market)
            elif market['closed']:
                closed_markets[market_type].append(market)
            elif market['archived']:
                archived_markets[market_type].append(market)
        
        # Print Active Markets by type
        print("\n=== ACTIVE MARKETS ===")
        for market_type in active_markets:
            if active_markets[market_type]:
                print(f"\n{market_type} Markets:")
                for idx, market in enumerate(active_markets[market_type], 1):
                    print(f"\n{idx}. {format_market_info(market)}")
            
        # Print Closed Markets by type
        print("\n=== CLOSED MARKETS ===")
        for market_type in closed_markets:
            if closed_markets[market_type]:
                print(f"\n{market_type} Markets:")
                for idx, market in enumerate(closed_markets[market_type], 1):
                    print(f"\n{idx}. {format_market_info(market)}")
            
        # Print Archived Markets by type
        print("\n=== ARCHIVED MARKETS ===")
        for market_type in archived_markets:
            if archived_markets[market_type]:
                print(f"\n{market_type} Markets:")
                for idx, market in enumerate(archived_markets[market_type], 1):
                    print(f"\n{idx}. {format_market_info(market)}")
        
        # Print total counts
        print("\n=== MARKET COUNTS ===")
        print(f"Total Markets: {len(processed_markets)}")
        print(f"Total Active Markets: {sum(len(m) for m in active_markets.values())}")
        print(f"Total Closed Markets: {sum(len(m) for m in closed_markets.values())}")
        print(f"Total Archived Markets: {sum(len(m) for m in archived_markets.values())}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    list_markets() 