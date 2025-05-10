import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
import json
from typing import Dict, List
from py_clob_client.constants import END_CURSOR
import csv
from datetime import datetime
from py_clob_client.clob_types import BookParams

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

def get_market_details(client: ClobClient, market: Dict) -> Dict:
    """Get additional market details including order book, prices, and trading info"""
    try:
        token_id = market['tokens'][0]['token_id'] if market.get('tokens') else None
        if not token_id:
            return {}
            
        details = {}
        
        # Get order book
        try:
            order_book = client.get_order_book(token_id)
            details['order_book'] = {
                'bids': [{'price': b.price, 'size': b.size} for b in order_book.bids] if order_book.bids else [],
                'asks': [{'price': a.price, 'size': a.size} for a in order_book.asks] if order_book.asks else []
            }
        except Exception as e:
            details['order_book'] = {'error': str(e)}
            
        # Get mid price
        try:
            mid_price = client.get_midpoint(token_id)
            details['mid_price'] = mid_price.get('mid')
        except Exception as e:
            details['mid_price'] = None
            
        # Get last trade price
        try:
            last_trade = client.get_last_trade_price(token_id)
            details['last_trade_price'] = last_trade.get('price')
        except Exception as e:
            details['last_trade_price'] = None
            
        # Get spread
        try:
            spread = client.get_spread(token_id)
            details['spread'] = spread.get('spread')
        except Exception as e:
            details['spread'] = None
            
        return details
    except Exception as e:
        return {'error': str(e)}

def export_markets_to_csv(markets: List[Dict], client: ClobClient, filename: str):
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
                # Get additional market details
                details = get_market_details(client, market)
                
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

def list_markets():
    """List all available markets on Polymarket CLOB"""
    try:
        # Initialize the client with minimal configuration
        client = ClobClient(
            host="https://clob.polymarket.com"  # Polymarket mainnet CLOB endpoint
        )
        
        # Fetch all markets using pagination
        print("Fetching markets...\n")
        all_markets = []
        next_cursor = "MA=="  # Initial cursor
        
        while next_cursor != END_CURSOR:
            response = client.get_markets(next_cursor=next_cursor)
            if isinstance(response, dict) and 'data' in response:
                all_markets.extend(response['data'])
                next_cursor = response.get('next_cursor', END_CURSOR)
            else:
                print("Unexpected response format:", response)
                break
        
        # Export to CSV with additional market data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"polymarket_markets_{timestamp}.csv"
        print(f"\nExporting market data to {csv_filename}")
        export_markets_to_csv(all_markets, client, csv_filename)
        print(f"Export complete!")
            
        # Group markets by type and status
        active_markets = {'Binary': [], 'Sports': [], 'Crypto': [], 'Other': []}
        closed_markets = {'Binary': [], 'Sports': [], 'Crypto': [], 'Other': []}
        archived_markets = {'Binary': [], 'Sports': [], 'Crypto': [], 'Other': []}
        
        for market in all_markets:
            market_type = get_market_type(market)
            if market['active'] and market['accepting_orders']:
                active_markets[market_type].append(market)
            elif market['closed']:
                closed_markets[market_type].append(market)
            elif market['archived']:
                archived_markets[market_type].append(market)
        
        # Print Active Markets by type
        print("\n=== ACTIVE MARKETS ===")
        for market_type in ['Binary', 'Sports', 'Crypto', 'Other']:
            if active_markets[market_type]:
                print(f"\n{market_type} Markets:")
                for idx, market in enumerate(active_markets[market_type], 1):
                    print(f"\n{idx}. {format_market_info(market)}")
            
        # Print Closed Markets by type
        print("\n=== CLOSED MARKETS ===")
        for market_type in ['Binary', 'Sports', 'Crypto', 'Other']:
            if closed_markets[market_type]:
                print(f"\n{market_type} Markets:")
                for idx, market in enumerate(closed_markets[market_type], 1):
                    print(f"\n{idx}. {format_market_info(market)}")
            
        # Print Archived Markets by type
        print("\n=== ARCHIVED MARKETS ===")
        for market_type in ['Binary', 'Sports', 'Crypto', 'Other']:
            if archived_markets[market_type]:
                print(f"\n{market_type} Markets:")
                for idx, market in enumerate(archived_markets[market_type], 1):
                    print(f"\n{idx}. {format_market_info(market)}")
        
        # Print total counts
        print("\n=== MARKET COUNTS ===")
        print(f"Total Markets: {len(all_markets)}")
        print(f"Total Active Markets: {sum(len(m) for m in active_markets.values())}")
        print(f"Total Closed Markets: {sum(len(m) for m in closed_markets.values())}")
        print(f"Total Archived Markets: {sum(len(m) for m in archived_markets.values())}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    list_markets() 