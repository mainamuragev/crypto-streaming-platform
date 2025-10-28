import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration - replace with your actual credentials
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'crypto_db',
    'user': 'crypto_user',
    'password': 'your_password_here'
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
