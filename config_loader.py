import os
from dotenv import load_dotenv

def load_config():
    """Load configuration from environment variables"""
    load_dotenv()
    
    config = {
        'postgres': {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'crypto_db'),
            'user': os.getenv('POSTGRES_USER', 'crypto_user'),
            'password': os.getenv('POSTGRES_PASSWORD', '')
        },
        'cassandra': {
            'hosts': os.getenv('CASSANDRA_HOSTS', 'localhost').split(','),
            'port': int(os.getenv('CASSANDRA_PORT', 9042)),
            'keyspace': os.getenv('CASSANDRA_KEYSPACE', 'crypto_data')
        },
        'binance': {
            'api_key': os.getenv('BINANCE_API_KEY', ''),
            'api_secret': os.getenv('BINANCE_SECRET_KEY', '')
        }
    }
    
    return config

if __name__ == "__main__":
    config = load_config()
    print("Configuration loaded successfully")
