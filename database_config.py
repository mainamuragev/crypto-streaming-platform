import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'crypto_db'),
    'user': os.getenv('POSTGRES_USER', 'crypto_user'),
    'password': os.getenv('POSTGRES_PASSWORD', '')
}

CASSANDRA_CONFIG = {
    'hosts': os.getenv('CASSANDRA_HOSTS', 'localhost').split(','),
    'port': int(os.getenv('CASSANDRA_PORT', 9042)),
    'keyspace': os.getenv('CASSANDRA_KEYSPACE', 'crypto_data')
}

# Binance API configuration
BINANCE_CONFIG = {
    'api_key': os.getenv('BINANCE_API_KEY', ''),
    'api_secret': os.getenv('BINANCE_SECRET_KEY', '')
}
