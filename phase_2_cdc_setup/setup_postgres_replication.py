import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration from environment
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'crypto_db'),
    'user': os.getenv('POSTGRES_USER', 'crypto_user'),
    'password': os.getenv('POSTGRES_PASSWORD', '')
}

def setup_replication():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create publication
        cursor.execute("""
            DROP PUBLICATION IF EXISTS crypto_publication;
            CREATE PUBLICATION crypto_publication FOR TABLE crypto_ticker_24hr;
        """)
        
        print("✅ PostgreSQL replication setup completed")
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error setting up replication: {e}")

if __name__ == "__main__":
    setup_replication()
