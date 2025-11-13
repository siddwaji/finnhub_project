"""
Database manager for Feather Finance App
"""

import sqlite3
import os
from contextlib import contextmanager


class Database:
    """SQLite database wrapper"""
    
    def __init__(self, db_path='feather.db'):
        self.db_path = db_path
        print(f"[OK] Database initialized: {db_path}")
    
    @contextmanager
    def get_connection(self):
        """Safe database connection with automatic commit/rollback"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] {e}")
            raise e
        finally:
            conn.close()
    
    # ============================================
    # INSERT FUNCTIONS
    # ============================================
    
    def insert_stock_data(self, data):
        """
        Insert stock OHLCV data
        
        Example:
        db.insert_stock_data({
            'ticker': 'AAPL',
            'open': 270.5,
            'high': 272.3,
            'low': 269.8,
            'close': 271.2,
            'volume': 45000000,
            'timestamp': 1730419200
        })
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO stock_data 
                (ticker, open, high, low, close, volume, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['ticker'], data['open'], data['high'], 
                  data['low'], data['close'], data['volume'], data['timestamp']))
            print(f"[OK] Inserted stock data for {data['ticker']}")
            return cursor.lastrowid
    
    def insert_prediction(self, prediction):
        """
        Insert ML prediction
        
        Example:
        db.insert_prediction({
            'ticker': 'AAPL',
            'predicted_trend': 'up',
            'confidence': 0.85,
            'predicted_change': 2.5,
            'model_version': 'v1.0'
        })
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions 
                (ticker, predicted_trend, confidence, predicted_change, model_version)
                VALUES (?, ?, ?, ?, ?)
            ''', (prediction['ticker'], prediction['predicted_trend'],
                  prediction['confidence'], prediction.get('predicted_change'),
                  prediction['model_version']))
            print(f"[OK] Inserted prediction for {prediction['ticker']}")
            return cursor.lastrowid
    
    def insert_news_article(self, article):
        """
        Insert news article
        
        Example:
        db.insert_news_article({
            'ticker': 'AAPL',
            'headline': 'Apple Announces New iPhone',
            'summary': 'Latest model features...',
            'sentiment': 'positive',
            'source': 'TechNews',
            'url': 'https://...'
        })
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO news_articles 
                (ticker, headline, summary, sentiment, source, url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (article['ticker'], article['headline'], article.get('summary'),
                  article.get('sentiment'), article.get('source'), article.get('url')))
            print(f"[OK] Inserted news: {article['headline'][:50]}...")
            return cursor.lastrowid
    
    def add_to_watchlist(self, user_id, ticker):
        """
        Add stock to user's watchlist
        
        Example:
        db.add_to_watchlist(1, 'AAPL')
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO watchlists (user_id, ticker)
                VALUES (?, ?)
            ''', (user_id, ticker))
            print(f"[OK] Added {ticker} to user {user_id}'s watchlist")
            return cursor.lastrowid
    
    # ============================================
    # QUERY FUNCTIONS
    # ============================================
    
    def get_stock_data(self, ticker, limit=30):
        """
        Get historical stock data for a ticker
        Returns most recent data first
        
        Example:
        data = db.get_stock_data('AAPL', limit=30)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM stock_data 
                WHERE ticker = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (ticker, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_latest_prediction(self, ticker):
        """
        Get most recent prediction for a stock
        
        Example:
        pred = db.get_latest_prediction('AAPL')
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM predictions 
                WHERE ticker = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (ticker,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_watchlist(self, user_id):
        """
        Get all stocks in user's watchlist
        
        Example:
        stocks = db.get_user_watchlist(1)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT w.ticker, s.name, s.sector, w.added_at
                FROM watchlists w
                JOIN stocks s ON w.ticker = s.ticker
                WHERE w.user_id = ?
                ORDER BY w.added_at DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_recent_news(self, ticker, limit=5):
        """
        Get recent news for a stock
        
        Example:
        news = db.get_recent_news('AAPL', limit=5)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM news_articles 
                WHERE ticker = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (ticker, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_all_stocks(self):
        """
        Get list of all stocks in database
        
        Example:
        stocks = db.get_all_stocks()
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM stocks ORDER BY ticker')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


# Test the database
if __name__ == "__main__":
    print("="*60)
    print("TESTING DATABASE")
    print("="*60)
    
    # Initialize
    db = Database()
    
    # Check if database exists
    if not os.path.exists('feather.db'):
        print("[ERROR] Database not found!")
        print("Run 'python setup_database.py' first")
        exit(1)
    
    print("\n[TEST 1] Inserting sample stock data...")
    db.insert_stock_data({
        'ticker': 'AAPL',
        'open': 270.5,
        'high': 272.3,
        'low': 269.8,
        'close': 271.2,
        'volume': 45000000,
        'timestamp': 1730419200
    })
    
    print("\n[TEST 2] Inserting sample prediction...")
    db.insert_prediction({
        'ticker': 'AAPL',
        'predicted_trend': 'up',
        'confidence': 0.85,
        'predicted_change': 2.5,
        'model_version': 'test_v1.0'
    })
    
    print("\n[TEST 3] Adding to watchlist...")
    db.add_to_watchlist(1, 'AAPL')
    
    print("\n[TEST 4] Querying stock data...")
    stock_data = db.get_stock_data('AAPL')
    print(f"Found {len(stock_data)} stock data points")
    
    print("\n[TEST 5] Querying prediction...")
    prediction = db.get_latest_prediction('AAPL')
    if prediction:
        print(f"Latest prediction: {prediction['predicted_trend']} (confidence: {prediction['confidence']})")
    
    print("\n[TEST 6] Getting all stocks...")
    stocks = db.get_all_stocks()
    print(f"Stocks in database: {', '.join([s['ticker'] for s in stocks])}")
    
    print("\n" + "="*60)
    print("[SUCCESS] Database is working perfectly!")
    print(f"Database file: {db.db_path}")
    print("="*60)