"""
Seed Script for Demo Data
Creates sample data for testing the finance app
"""

import json
import random
from datetime import datetime, timedelta


def generate_sample_users():
    """Generate sample user accounts"""
    users = [
        {
            'id': 1,
            'username': 'demo_user',
            'email': 'demo@example.com',
            'created_at': '2024-10-01 10:00:00'
        },
        {
            'id': 2,
            'username': 'test_trader',
            'email': 'trader@example.com',
            'created_at': '2024-10-15 14:30:00'
        },
        {
            'id': 3,
            'username': 'investor_jane',
            'email': 'jane@example.com',
            'created_at': '2024-10-20 09:15:00'
        }
    ]
    return users


def generate_sample_stocks():
    """Generate sample stock watchlist data"""
    stocks = [
        {'ticker': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology'},
        {'ticker': 'MSFT', 'name': 'Microsoft Corporation', 'sector': 'Technology'},
        {'ticker': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology'},
        {'ticker': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Automotive'},
        {'ticker': 'NVDA', 'name': 'NVIDIA Corporation', 'sector': 'Technology'},
        {'ticker': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'E-commerce'}
    ]
    return stocks


def generate_sample_predictions():
    """Generate sample stock predictions"""
    predictions = []
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
    
    for i, ticker in enumerate(tickers, 1):
        prediction = {
            'id': i,
            'ticker': ticker,
            'predicted_trend': random.choice(['up', 'down', 'neutral']),
            'confidence': round(random.uniform(0.6, 0.95), 2),
            'predicted_change': round(random.uniform(-5.0, 5.0), 2),
            'timestamp': datetime.now().isoformat(),
            'model_version': 'v1.0'
        }
        predictions.append(prediction)
    
    return predictions


def generate_sample_news():
    """Generate sample news articles"""
    news = [
        {
            'id': 1,
            'ticker': 'AAPL',
            'headline': 'Apple Announces New iPhone Release',
            'summary': 'Apple unveils latest iPhone with improved features',
            'sentiment': 'positive',
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'source': 'TechNews'
        },
        {
            'id': 2,
            'ticker': 'TSLA',
            'headline': 'Tesla Reports Strong Q3 Earnings',
            'summary': 'Tesla exceeds analyst expectations for quarterly earnings',
            'sentiment': 'positive',
            'timestamp': (datetime.now() - timedelta(hours=5)).isoformat(),
            'source': 'FinancialTimes'
        },
        {
            'id': 3,
            'ticker': 'GOOGL',
            'headline': 'Google Faces Regulatory Challenges',
            'summary': 'EU regulators investigate Google business practices',
            'sentiment': 'negative',
            'timestamp': (datetime.now() - timedelta(hours=8)).isoformat(),
            'source': 'Reuters'
        }
    ]
    return news


def generate_sample_watchlists():
    """Generate sample user watchlists"""
    watchlists = [
        {
            'user_id': 1,
            'stocks': ['AAPL', 'MSFT', 'GOOGL']
        },
        {
            'user_id': 2,
            'stocks': ['TSLA', 'NVDA']
        },
        {
            'user_id': 3,
            'stocks': ['AAPL', 'TSLA', 'AMZN', 'NVDA']
        }
    ]
    return watchlists


def generate_all_seed_data():
    """Generate all seed data and save to JSON file"""
    
    print("Generating seed data...")
    
    seed_data = {
        'users': generate_sample_users(),
        'stocks': generate_sample_stocks(),
        'predictions': generate_sample_predictions(),
        'news': generate_sample_news(),
        'watchlists': generate_sample_watchlists(),
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'purpose': 'Demo and testing'
        }
    }
    
    # Save to JSON file
    filename = 'seed_data.json'
    with open(filename, 'w') as f:
        json.dump(seed_data, f, indent=2)
    
    print(f"\n[SUCCESS] Seed data generated and saved to {filename}")
    print(f"\nSummary:")
    print(f"  - Users: {len(seed_data['users'])}")
    print(f"  - Stocks: {len(seed_data['stocks'])}")
    print(f"  - Predictions: {len(seed_data['predictions'])}")
    print(f"  - News Articles: {len(seed_data['news'])}")
    print(f"  - Watchlists: {len(seed_data['watchlists'])}")
    
    return seed_data


if __name__ == "__main__":
    print("="*60)
    print("SEED DATA GENERATION SCRIPT")
    print("="*60)
    
    data = generate_all_seed_data()
    
    print("\n" + "="*60)
    print("Sample Data Preview:")
    print("="*60)
    print("\nSample User:")
    print(json.dumps(data['users'][0], indent=2))
    print("\nSample Prediction:")
    print(json.dumps(data['predictions'][0], indent=2))