import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
import asyncio
import json
from datetime import datetime
import csv
import pandas as pd

from clients import KalshiHttpClient, KalshiWebSocketClient, Environment

# Load environment variables
load_dotenv()
env = Environment.DEMO # toggle environment here
KEYID = os.getenv('DEMO_KEYID') if env == Environment.DEMO else os.getenv('PROD_KEYID')
KEYFILE = os.getenv('DEMO_KEYFILE') if env == Environment.DEMO else os.getenv('PROD_KEYFILE')

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

# Initialize the HTTP client
client = KalshiHttpClient(
    key_id=KEYID,
    private_key=private_key,
    environment=env
)

# Get account balance
balance = client.get_balance()
print("Balance:", balance)

# Create a list to store all market data
all_market_data = []

# Get election events
events = client.get_events(status="open", with_nested_markets=True)
print("\nOpen Election Events:")
for event in events.get('events', []):
    print(f"\nEvent: {event['event_ticker']}")
    print(f"Category: {event.get('category', 'N/A')}")
    
    if 'markets' in event:
        print("Markets:")
        for market in event['markets']:
            # Get detailed market info
            try:
                market_details = client.get_market(market['ticker'])['market']
                
                # Create a dictionary for this market's data
                market_data = {
                    'event_ticker': event['event_ticker'],
                    'event_category': event.get('category', 'N/A'),
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
                
                # Print market details
                print(f"\n  Title: {market_data['market_title']}")
                print(f"  Ticker: {market_data['market_ticker']}")
                print(f"  Status: {market_data['status']}")
                print(f"  Market Type: {market_data['market_type']}")
                print(f"  Close Time: {market_data['close_time']}")
                
                if market_data['last_price'] is not None:
                    print(f"  Last Price: {market_data['last_price']:.1%}")
                
                if market_data['yes_bid'] is not None and market_data['yes_bid'] > 0:
                    print(f"  Yes Bid: {market_data['yes_bid']:.1%}")
                
                if market_data['yes_ask'] is not None and market_data['yes_ask'] > 0:
                    print(f"  Yes Ask: {market_data['yes_ask']:.1%}")
                
                print(f"  Volume 24h: {market_data['volume_24h']} contracts")
                print(f"  Open Interest: {market_data['open_interest']} contracts")
            except Exception as e:
                print(f"  Error fetching details for {market['ticker']}: {str(e)}")

print("\nNote: Prices shown as percentages (e.g., 55.0% means $0.55 per share)")

# Export data to CSV
if all_market_data:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'kalshi_markets_{timestamp}.csv'
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_market_data)
    df.to_csv(csv_filename, index=False)
    print(f"\nData exported to {csv_filename}")

# Initialize the WebSocket client
ws_client = KalshiWebSocketClient(
    key_id=KEYID,
    private_key=private_key,
    environment=env
)

# Connect via WebSocket
asyncio.run(ws_client.connect())