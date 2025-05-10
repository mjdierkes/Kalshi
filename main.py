import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
import asyncio
import json
from datetime import datetime

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
                print(f"\n  Title: {market_details.get('title', 'N/A')}")
                print(f"  Ticker: {market_details.get('ticker', 'N/A')}")
                print(f"  Status: {market_details.get('status', 'N/A')}")
                print(f"  Market Type: {market_details.get('market_type', 'N/A')}")
                print(f"  Close Time: {market_details.get('close_time', 'N/A')}")
                
                # Format prices as percentages
                last_price = market_details.get('last_price', 0)
                yes_bid = market_details.get('yes_bid', 0)
                yes_ask = market_details.get('yes_ask', 0)
                
                if last_price is not None:
                    last_price_percent = last_price / 100
                    print(f"  Last Price: {last_price_percent:.1f}%")
                
                if yes_bid is not None and yes_bid > 0:
                    yes_bid_percent = yes_bid / 100
                    print(f"  Yes Bid: {yes_bid_percent:.1f}%")
                
                if yes_ask is not None and yes_ask > 0:
                    yes_ask_percent = yes_ask / 100
                    print(f"  Yes Ask: {yes_ask_percent:.1f}%")
                
                print(f"  Volume 24h: {market_details.get('volume_24h', 0)} contracts")
                print(f"  Open Interest: {market_details.get('open_interest', 0)} contracts")
            except Exception as e:
                print(f"  Error fetching details for {market['ticker']}: {str(e)}")

print("\nNote: Prices shown as percentages (e.g., 55.0% means $0.55 per share)")

# Initialize the WebSocket client
ws_client = KalshiWebSocketClient(
    key_id=KEYID,
    private_key=private_key,
    environment=env
)

# Connect via WebSocket
asyncio.run(ws_client.connect())