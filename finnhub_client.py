"""
Finnhub Stock Data Interface
Fetches stock data (OHLCV) from Finnhub API
Format: ticker, open, high, low, close, volume, timestamp
"""

import requests
import time
import json
import csv
from datetime import datetime
from config import FINNHUB_API_KEY


class FinnhubStockData:
    """Main class for fetching stock data from Finnhub"""
    
    def __init__(self):
        """Initialize with API key from config"""
        self.api_key = FINNHUB_API_KEY
        self.base_url = "https://finnhub.io/api/v1"
        self.rate_limit_delay = 1.1
        print("[OK] FinnhubStockData initialized")
    
    def get_stock_candles(self, ticker, days=30, resolution='D'):
        """
        Get historical stock price data (OHLCV)
        
        Parameters:
            ticker (str): Stock symbol like 'AAPL', 'TSLA'
            days (int): How many days of history to get
            resolution (str): 'D' = daily, '60' = hourly, '5' = 5 minutes
        
        Returns:
            list: List of dicts with stock data
        """
        print(f"\nFetching {days} days of {resolution} data for {ticker}...")
        
        to_timestamp = int(time.time())
        from_timestamp = to_timestamp - (days * 24 * 60 * 60)
        
        url = f"{self.base_url}/stock/candle"
        params = {
            'symbol': ticker,
            'resolution': resolution,
            'from': from_timestamp,
            'to': to_timestamp,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('s') == 'no_data':
                print(f"[ERROR] No data available for {ticker}")
                return []
            
            if data.get('s') != 'ok':
                print(f"[ERROR] API returned status: {data.get('s')}")
                return []
            
            formatted_data = []
            
            for i in range(len(data['t'])):
                formatted_data.append({
                    'ticker': ticker,
                    'open': data['o'][i],
                    'high': data['h'][i],
                    'low': data['l'][i],
                    'close': data['c'][i],
                    'volume': data['v'][i],
                    'timestamp': data['t'][i]
                })
            
            print(f"[OK] Successfully fetched {len(formatted_data)} data points")
            return formatted_data
            
        except requests.exceptions.Timeout:
            print(f"[ERROR] Request timed out for {ticker}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error fetching data for {ticker}: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return []
    
    def get_multiple_tickers(self, tickers, days=30, resolution='D'):
        """
        Get stock data for multiple tickers at once
        
        Parameters:
            tickers (list): List of stock symbols ['AAPL', 'TSLA', ...]
            days (int): How many days of history
            resolution (str): Time interval
        
        Returns:
            dict: {ticker: [data], ticker: [data], ...}
        """
        print(f"\nFetching data for {len(tickers)} tickers...")
        results = {}
        
        for i, ticker in enumerate(tickers, 1):
            print(f"\n[{i}/{len(tickers)}]", end=" ")
            data = self.get_stock_candles(ticker, days, resolution)
            results[ticker] = data
            
            if i < len(tickers):
                time.sleep(self.rate_limit_delay)
        
        print(f"\n[OK] Completed fetching all {len(tickers)} tickers")
        return results
    
    def get_current_quote(self, ticker):
        """
        Get real-time current price for a stock
        
        Parameters:
            ticker (str): Stock symbol
        
        Returns:
            dict: Current price information
        """
        print(f"\nFetching current quote for {ticker}...")
        
        url = f"{self.base_url}/quote"
        params = {
            'symbol': ticker,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = {
                'ticker': ticker,
                'current_price': data['c'],
                'change': data['d'],
                'percent_change': data['dp'],
                'high': data['h'],
                'low': data['l'],
                'open': data['o'],
                'previous_close': data['pc'],
                'timestamp': data['t']
            }
            
            print(f"[OK] Current price: ${data['c']}")
            return result
            
        except Exception as e:
            print(f"[ERROR] Error fetching quote: {e}")
            return None
    
    def save_to_json(self, data, filename):
        """Save data to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[OK] Data saved to {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Error saving JSON: {e}")
            return False
    
    def save_to_csv(self, data, filename):
        """Save data to a CSV file"""
        try:
            if not data:
                print("[ERROR] No data to save")
                return False
            
            headers = list(data[0].keys())
            
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"[OK] Data saved to {filename}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error saving CSV: {e}")
            return False
    
    def convert_timestamp_to_date(self, timestamp):
        """Convert Unix timestamp to readable date"""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    print("Testing FinnhubStockData class...")
    client = FinnhubStockData()
    
    data = client.get_stock_candles('AAPL', days=7)
    
    if data:
        print(f"\nSample data point:")
        print(data[0])
        print(f"\nDate: {client.convert_timestamp_to_date(data[0]['timestamp'])}")