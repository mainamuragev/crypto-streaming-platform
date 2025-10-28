import psycopg2
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_config import DB_CONFIG
except ImportError:
    # Fallback configuration
    DB_CONFIG = {
        'host': 'pg-3d8a57ed-muragevincent39-e823.b.aivencloud.com',
        'port': 14040,
        'database': 'defaultdb',
        'user': 'avnadmin',
        'password': 'AVNS_eCMPC7l_2vPN3FNsiHr',
        'sslmode': 'require'
    }

def setup_replication():
    print("🔧 Setting up PostgreSQL logical replication for CDC...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Enable logical replication (if not already enabled)
        print("✅ Checking logical replication settings...")
        
        # Create replication slot
        try:
            cur.execute("SELECT pg_create_logical_replication_slot('crypto_cdc_slot', 'pgoutput');")
            print("✅ Created replication slot: crypto_cdc_slot")
        except Exception as e:
            print(f"⚠️  Replication slot may already exist: {e}")
        
        # Create publication for our table
        try:
            cur.execute("CREATE PUBLICATION crypto_publication FOR TABLE crypto_ticker_24hr;")
            print("✅ Created publication: crypto_publication")
        except Exception as e:
            print(f"⚠️  Publication may already exist: {e}")
        
        # Verify the table has REPLICA IDENTITY FULL
        cur.execute("ALTER TABLE crypto_ticker_24hr REPLICA IDENTITY FULL;")
        print("✅ Set REPLICA IDENTITY FULL for crypto_ticker_24hr")
        
        # Verify setup
        cur.execute("SELECT slot_name, plugin FROM pg_replication_slots WHERE slot_name = 'crypto_cdc_slot';")
        slot = cur.fetchone()
        if slot:
            print(f"✅ Replication slot verified: {slot[0]} with plugin {slot[1]}")
        
        cur.execute("SELECT pubname FROM pg_publication WHERE pubname = 'crypto_publication';")
        pub = cur.fetchone()
        if pub:
            print(f"✅ Publication verified: {pub[0]}")
        
        conn.commit()
        cur.close()
        conn.close()
        print("🎉 PostgreSQL replication setup completed!")
        
    except Exception as e:
        print(f"❌ Error setting up replication: {e}")

if __name__ == "__main__":
    setup_replication()
