import pandas as pd
import os
import glob
import time
from datetime import datetime
from fuzzywuzzy import fuzz
import argparse

def find_latest_csv(pattern):
    """Find the latest CSV file matching the given pattern."""
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_polymarket_titles(csv_path, chunk_size=10000):
    """Load titles from Polymarket CSV in chunks to handle large files."""
    titles = []
    
    # Read CSV in chunks
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        if 'Title' in chunk.columns:
            # Add non-null titles to our list
            chunk_titles = chunk['Title'].dropna().tolist()
            titles.extend(chunk_titles)
    
    return titles

def load_kalshi_titles(csv_path, chunk_size=10000):
    """Load titles from Kalshi CSV in chunks to handle large files."""
    titles = []
    
    # Read CSV in chunks
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        if 'market_title' in chunk.columns:
            # Add non-null titles to our list
            chunk_titles = chunk['market_title'].dropna().tolist()
            titles.extend(chunk_titles)
    
    return titles

def preprocess_title(title):
    """Clean and standardize title for better matching."""
    if not isinstance(title, str):
        return ""
    
    # Convert to lowercase, remove extra whitespace
    cleaned = title.lower().strip()
    
    # Remove common terms and punctuation that might differ between platforms
    for term in ["will ", "what will ", "by ", "on ", "in ", "?"]:
        cleaned = cleaned.replace(term, " ")
    
    return cleaned

def find_best_match(title, target_titles, threshold=70):
    """Find the best match for a title in the target list."""
    best_score = 0
    best_match = None
    
    # Clean and standardize both titles
    clean_title = preprocess_title(title)
    
    for target in target_titles:
        clean_target = preprocess_title(target)
        
        # Skip if either title is empty after preprocessing
        if not clean_title or not clean_target:
            continue
        
        # Calculate similarity score
        score = fuzz.token_sort_ratio(clean_title, clean_target)
        
        if score > best_score:
            best_score = score
            best_match = target
    
    # Only return matches above threshold
    if best_score >= threshold:
        return best_match, best_score
    return None, 0

def compare_market_titles(polymarket_path, kalshi_path, threshold=70):
    """Compare market titles between Polymarket and Kalshi."""
    print(f"Loading titles from Polymarket CSV: {polymarket_path}")
    poly_titles = load_polymarket_titles(polymarket_path)
    print(f"Loaded {len(poly_titles)} Polymarket titles")
    
    print(f"Loading titles from Kalshi CSV: {kalshi_path}")
    kalshi_titles = load_kalshi_titles(kalshi_path)
    print(f"Loaded {len(kalshi_titles)} Kalshi titles")
    
    print("\nComparing titles...")
    matches = []
    start_time = time.time()
    
    # For each Polymarket title, find best match in Kalshi titles
    for i, poly_title in enumerate(poly_titles):
        # Print progress every 100 titles
        if i > 0 and i % 100 == 0:
            elapsed = time.time() - start_time
            titles_per_sec = i / elapsed
            remaining = (len(poly_titles) - i) / titles_per_sec if titles_per_sec > 0 else 0
            print(f"Processed {i}/{len(poly_titles)} titles ({i/len(poly_titles)*100:.1f}%). "
                  f"ETA: {remaining/60:.1f} minutes")
        
        best_match, score = find_best_match(poly_title, kalshi_titles, threshold)
        if best_match:
            matches.append((poly_title, best_match, score))
    
    # Calculate statistics
    match_percentage = len(matches) / len(poly_titles) * 100 if poly_titles else 0
    
    # Print results
    print("\n==== RESULTS ====")
    print(f"Total Polymarket titles: {len(poly_titles)}")
    print(f"Total Kalshi titles: {len(kalshi_titles)}")
    print(f"Matches found: {len(matches)} ({match_percentage:.2f}%)")
    
    # Show some sample matches
    if matches:
        print("\nSample matches (Polymarket -> Kalshi):")
        for poly, kalshi, score in matches[:10]:  # Show first 10 matches
            print(f"- [{score}%] {poly} -> {kalshi}")
    
    # Save matches to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"market_matches_{timestamp}.csv"
    
    matches_df = pd.DataFrame(matches, columns=['Polymarket Title', 'Kalshi Title', 'Match Score'])
    matches_df.to_csv(output_file, index=False)
    print(f"\nMatches saved to {output_file}")
    
    return matches, match_percentage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare market titles between Polymarket and Kalshi')
    parser.add_argument('--poly', help='Path to Polymarket CSV file')
    parser.add_argument('--kalshi', help='Path to Kalshi CSV file')
    parser.add_argument('--threshold', type=int, default=70, 
                        help='Minimum similarity score (0-100) to consider a match')
    args = parser.parse_args()
    
    # If no paths provided, try to find the latest CSVs
    poly_path = args.poly
    if not poly_path:
        poly_path = find_latest_csv("polymarket_markets_*.csv")
        if not poly_path:
            print("Error: No Polymarket CSV file found. Please provide a path with --poly.")
            exit(1)
    
    kalshi_path = args.kalshi
    if not kalshi_path:
        kalshi_path = find_latest_csv("kalshi_markets_*.csv")
        if not kalshi_path:
            print("Error: No Kalshi CSV file found. Please provide a path with --kalshi.")
            exit(1)
    
    # Run comparison
    compare_market_titles(poly_path, kalshi_path, args.threshold) 