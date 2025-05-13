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
import pickle
import pathlib

from clients import KalshiHttpClient, KalshiWebSocketClient, Environment

# Load environment variables
load_dotenv()
env = Environment.DEMO  # toggle environment here
KEYID = os.getenv('DEMO_KEYID') if env == Environment.DEMO else os.getenv('PROD_KEYID')
KEYFILE = os.getenv('DEMO_KEYFILE') if env == Environment.DEMO else os.getenv('PROD_KEYFILE')

# Set the maximum number of concurrent workers based on your machine
NUM_WORKERS = 32  # Increased from 16 for better parallelism

# Chunk size for parallel processing
CHUNK_SIZE = 200  # Increased from 50 to process more markets at once
CHUNK_DELAY = 0.05  # Reduced from 0.1s to 0.05s

# Rate limits - Aiming for Advanced tier (30 reads/sec)
API_RATE_LIMIT = 25  # Slightly under the Advanced tier limit of 30 req/s

# Checkpoint settings
CHECKPOINT_DIR = "checkpoints"
CHECKPOINT_INTERVAL = 1000  # Increased from 500 to reduce checkpoint overhead
MARKET_DATA_CHECKPOINT = os.path.join(CHECKPOINT_DIR, "market_data_checkpoint.json")
META_CHECKPOINT = os.path.join(CHECKPOINT_DIR, "meta_checkpoint.json")

# Ensure checkpoint directory exists
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

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
    rate_limit_per_second=API_RATE_LIMIT,  # Use the Advanced tier rate limit
    adaptive_rate_limiting=True  # Enable adaptive rate limiting
)

# Create a list to store all market data
all_market_data = []

def load_checkpoint():
    """Attempts to load checkpoint data if available"""
    checkpoint_data = {
        'processed_tickers': set(),
        'market_data': []
    }
    
    # Check if market data checkpoint exists
    if os.path.exists(MARKET_DATA_CHECKPOINT):
        try:
            with open(MARKET_DATA_CHECKPOINT, 'r') as f:
                checkpoint_data['market_data'] = json.load(f)
            # Extract processed tickers from the checkpoint
            checkpoint_data['processed_tickers'] = set(item['market_ticker'] for item in checkpoint_data['market_data'])
            print(f"Loaded {len(checkpoint_data['market_data'])} markets from checkpoint")
            print(f"Resuming from {len(checkpoint_data['processed_tickers'])} previously processed markets")
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
    
    return checkpoint_data

def save_checkpoint(market_data):
    """Save market data to checkpoint file"""
    try:
        with open(MARKET_DATA_CHECKPOINT, 'w') as f:
            json.dump(market_data, f, indent=2)
        print(f"Checkpoint saved: {len(market_data)} markets")
    except Exception as e:
        print(f"Error saving checkpoint: {e}")

def check_for_resume():
    """Check if we can resume from a checkpoint"""
    print("Checking for checkpoints to resume from...")
    checkpoint_exists = os.path.exists(MARKET_DATA_CHECKPOINT)
    
    if checkpoint_exists:
        response = input("Checkpoint found. Resume from checkpoint? (y/n): ")
        return response.lower() == 'y'
    else:
        print("No checkpoint found. Starting from scratch.")
        return False

async def fetch_all_market_data():
    start_time = time.time()
    
    # Performance monitoring variables
    request_count = 0
    error_count = 0
    last_progress_report = time.time()
    progress_report_interval = 30  # Report performance every 30 seconds
    
    # Check if we should resume from checkpoint
    should_resume = check_for_resume()
    checkpoint_data = load_checkpoint() if should_resume else {'processed_tickers': set(), 'market_data': []}
    
    # Restore market data from checkpoint if available
    if checkpoint_data['market_data']:
        all_market_data.extend(checkpoint_data['market_data'])
    
    # Keep track of processed tickers to avoid duplicates
    processed_tickers = checkpoint_data['processed_tickers']
    
    print("Fetching account balance...")
    # Get account balance
    balance = client.get_balance()
    print("Balance:", balance)
    
    print("\nFetching events...")
    all_events = []
    cursor = None
    
    with tqdm(desc="Fetching events", unit="page") as pbar:
        while True:
            try:
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
                request_count += 1
                
                if not cursor:
                    break
            except Exception as e:
                error_count += 1
                print(f"Error fetching events: {e}")
                # Add a short delay before retrying
                await asyncio.sleep(1)
                if error_count > 10:
                    print("Too many errors, aborting...")
                    return
    
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
    
    # Filter out already processed tickers
    unprocessed_tickers = [t for t in all_tickers if t not in processed_tickers]
    
    total_markets = len(all_tickers)
    remaining_markets = len(unprocessed_tickers)
    print(f"\nFetching details for {remaining_markets} remaining markets out of {total_markets} total")
    
    if unprocessed_tickers:
        # Split tickers into chunks to avoid overwhelming the API
        chunk_size = CHUNK_SIZE  # Use the configured chunk size constant
        num_chunks = (remaining_markets + chunk_size - 1) // chunk_size
        
        # Create progress bar for chunks
        checkpoint_count = 0
        successful_markets = 0
        
        with tqdm(total=remaining_markets, desc="Fetching market details", unit="market") as pbar:
            for chunk_start in range(0, remaining_markets, chunk_size):
                chunk_end = min(chunk_start + chunk_size, remaining_markets)
                chunk_tickers = unprocessed_tickers[chunk_start:chunk_end]
                
                # Monitor and report performance
                current_time = time.time()
                if current_time - last_progress_report > progress_report_interval:
                    elapsed = current_time - start_time
                    markets_per_second = successful_markets / elapsed if elapsed > 0 else 0
                    requests_per_second = request_count / elapsed if elapsed > 0 else 0
                    print(f"\nPerformance: {markets_per_second:.2f} markets/sec, {requests_per_second:.2f} requests/sec, {error_count} errors")
                    remaining_time = (remaining_markets - successful_markets) / markets_per_second if markets_per_second > 0 else 0
                    print(f"Estimated time remaining: {remaining_time/60:.2f} minutes")
                    last_progress_report = current_time
                
                try:
                    chunk_results = await client.get_markets_async(chunk_tickers)
                    request_count += len(chunk_tickers)  # Count each market request
                    
                    # Process results immediately
                    successful_chunk_markets = 0
                    for j, market_details in enumerate(chunk_results):
                        ticker = chunk_tickers[j]
                        event_ticker = event_market_map.get(ticker, 'N/A')
                        
                        # Find the event data
                        event_data = next((e for e in all_events 
                                         if e['event_ticker'] == event_ticker), {})
                        
                        # Skip if there was an error fetching this market
                        if isinstance(market_details, dict) and 'error' in market_details:
                            print(f"Error fetching details for {ticker}: {market_details['error']}")
                            processed_tickers.add(ticker)  # Mark as processed even if error
                            error_count += 1
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
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            # Store the raw market details for complete data
                            'raw_data': market_details
                        }
                        
                        all_market_data.append(market_data)
                        processed_tickers.add(ticker)
                        successful_chunk_markets += 1
                    
                    successful_markets += successful_chunk_markets
                    pbar.update(len(chunk_tickers))
                    checkpoint_count += len(chunk_tickers)
                    
                    # Create checkpoint every CHECKPOINT_INTERVAL markets
                    if checkpoint_count >= CHECKPOINT_INTERVAL:
                        save_checkpoint(all_market_data)
                        checkpoint_count = 0
                
                except Exception as e:
                    print(f"Error processing chunk: {e}")
                    error_count += 1
                    # If we encounter too many errors in a row, abort
                    if error_count > 50:
                        print("Too many errors, saving checkpoint and aborting...")
                        save_checkpoint(all_market_data)
                        return
                
                # Small delay between chunks to avoid rate limits - reduced for speed
                await asyncio.sleep(CHUNK_DELAY)
    
    # Final checkpoint save
    save_checkpoint(all_market_data)
    
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
    categories = {}  # Track categories and their market counts
    
    for event_ticker, markets in markets_by_event.items():
        if not markets:
            continue
            
        total_markets += len(markets)
        category = markets[0]['event_category']
        
        # Track category counts
        if category not in categories:
            categories[category] = 0
        categories[category] += len(markets)
        
        print(f"\nEvent: {event_ticker}")
        print(f"Category: {category}")
        print(f"Number of markets: {len(markets)}")
        
        # Show sample markets
        sample_size = min(3, len(markets))
        print(f"Sample markets:")
        for i in range(sample_size):
            market = markets[i]
            print(f"  {market['market_title']} ({market['market_ticker']}): " + 
                  (f"{market['last_price']:.1%}" if market['last_price'] is not None else "No price"))
    
    print(f"\nTotal number of markets found: {total_markets}")
    
    # Print category breakdown
    print("\nMarkets by Category:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: {count} markets ({count/total_markets:.1%})")
    
    print("\nNote: Prices shown as percentages (e.g., 55.0% means $0.55 per share)")
    
    # Export data to JSON
    if all_market_data:
        print("\nExporting data to JSON...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f'kalshi_markets_{timestamp}.json'
        
        # Save as JSON
        with open(json_filename, 'w') as f:
            json.dump(all_market_data, f, indent=2)
        print(f"Data exported to {json_filename}")
        
        # Also save a CSV version for easy viewing
        csv_filename = f'kalshi_markets_{timestamp}.csv'
        # Remove raw_data field for CSV export
        csv_data = [{k: v for k, v in item.items() if k != 'raw_data'} for item in all_market_data]
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False)
        print(f"Summary data also exported to {csv_filename}")
        
        # Clean up checkpoint files if export successful
        response = input("\nExport successful. Remove checkpoint file? (y/n): ")
        if response.lower() == 'y':
            if os.path.exists(MARKET_DATA_CHECKPOINT):
                os.remove(MARKET_DATA_CHECKPOINT)
            print("Checkpoint file removed.")
    
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

# WebSocket message handler
def handle_market_update(message_data):
    if 'message' in message_data and 'ticker' in message_data['message']:
        # Process and update market data in real-time
        ticker = message_data['message'].get('ticker')
        print(f"Received update for {ticker}")
        # TODO: Add more processing as needed

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