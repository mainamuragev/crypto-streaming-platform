import requests
import psycopg2
import time
import json
from datetime import datetime
import sys
import os

# Add current directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_config import DB_CONFIG

class BinanceDataCollector:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"
        self.db_config = DB_CONFIG
        
    def get_db_connection(self):
        """Create database connection to Aiven PostgreSQL"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def create_table_if_not_exists(self):
        """Create the crypto table if it doesn't exist"""
        conn = self.get_db_connection()
        if not conn:
            return False
            
        try:
            with conn.cursor() as cur:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS crypto_ticker_24hr (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(20) NOT NULL,
                    price_change DECIMAL(18, 8),
                    price_change_percent DECIMAL(8, 4),
                    weighted_avg_price DECIMAL(18, 8),
                    prev_close_price DECIMAL(18, 8),
                    last_price DECIMAL(18, 8),
                    last_qty DECIMAL(18, 8),
                    bid_price DECIMAL(18, 8),
                    ask_price DECIMAL(18, 8),
                    open_price DECIMAL(18, 8),
                    high_price DECIMAL(18, 8),
                    low_price DECIMAL(18, 8),
                    volume DECIMAL(18, 2),
                    quote_volume DECIMAL(18, 2),
                    open_time TIMESTAMP,
                    close_time TIMESTAMP,
                    first_trade_id BIGINT,
                    last_trade_id BIGINT,
                    trade_count BIGINT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cur.execute(create_table_query)
                
                # Create indexes
                cur.execute("CREATE INDEX IF NOT EXISTS idx_crypto_symbol_time ON crypto_ticker_24hr(symbol, created_at);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_crypto_created_at ON crypto_ticker_24hr(created_at);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_crypto_price_change ON crypto_ticker_24hr(price_change_percent DESC);")
                
            conn.commit()
            print("✅ Database table created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating table: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def fetch_24hr_ticker(self, symbol='BTCUSDT'):
        """Fetch 24hr ticker data for a symbol"""
        url = f"{self.base_url}/ticker/24hr"
        params = {'symbol': symbol}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def fetch_all_symbols(self):
        """Fetch all available trading pairs from Binance"""
        url = f"{self.base_url}/exchangeInfo"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get USDT pairs for major cryptocurrencies
            symbols = [
                symbol['symbol'] for symbol in data['symbols'] 
                if symbol['symbol'].endswith('USDT') and symbol['status'] == 'TRADING'
            ]
            return symbols[:10]  # Limit to top 10 for testing
        except requests.exceptions.RequestException as e:
            print(f"Error fetching symbols: {e}")
            return ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
    
    def insert_ticker_data(self, ticker_data):
        """Insert ticker data into PostgreSQL"""
        if not ticker_data:
            return False
            
        conn = self.get_db_connection()
        if not conn:
            return False
            
        try:
            with conn.cursor() as cur:
                query = """
                INSERT INTO crypto_ticker_24hr (
                    symbol, price_change, price_change_percent, weighted_avg_price,
                    prev_close_price, last_price, last_qty, bid_price, ask_price,
                    open_price, high_price, low_price, volume, quote_volume,
                    open_time, close_time, first_trade_id, last_trade_id, trade_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Convert timestamp from milliseconds to datetime
                open_time = datetime.fromtimestamp(ticker_data['openTime'] / 1000) if ticker_data['openTime'] else None
                close_time = datetime.fromtimestamp(ticker_data['closeTime'] / 1000) if ticker_data['closeTime'] else None
                
                cur.execute(query, (
                    ticker_data['symbol'],
                    float(ticker_data['priceChange']),
                    float(ticker_data['priceChangePercent']),
                    float(ticker_data['weightedAvgPrice']),
                    float(ticker_data['prevClosePrice']),
                    float(ticker_data['lastPrice']),
                    float(ticker_data['lastQty']),
                    float(ticker_data['bidPrice']),
                    float(ticker_data['askPrice']),
                    float(ticker_data['openPrice']),
                    float(ticker_data['highPrice']),
                    float(ticker_data['lowPrice']),
                    float(ticker_data['volume']),
                    float(ticker_data['quoteVolume']),
                    open_time,
                    close_time,
                    ticker_data.get('firstId'),
                    ticker_data.get('lastId'),
                    ticker_data.get('count')
                ))
                
            conn.commit()
            print(f"✅ Inserted data for {ticker_data['symbol']} - Price: ${float(ticker_data['lastPrice']):.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error inserting data for {ticker_data['symbol']}: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def run_collection(self):
        """Main method to run data collection"""
        print("🚀 Starting Binance data collection with Aiven PostgreSQL...")
        
        # Create table first
        if not self.create_table_if_not_exists():
            print("❌ Failed to create table. Exiting.")
            return
        
        symbols = self.fetch_all_symbols()
        print(f"📊 Tracking {len(symbols)} symbols: {symbols}")
        
        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                print(f"\n🔄 Collection cycle {cycle_count} at {datetime.now()}")
                
                for symbol in symbols:
                    ticker_data = self.fetch_24hr_ticker(symbol)
                    if ticker_data:
                        self.insert_ticker_data(ticker_data)
                
                print(f"✅ Cycle {cycle_count} completed")
                time.sleep(60)  # Wait 1 minute between cycles
                
            except KeyboardInterrupt:
                print("🛑 Data collection stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in collection cycle: {e}")
                time.sleep(30)  # Wait 30 seconds before retrying

if __name__ == "__main__":
    collector = BinanceDataCollector()
    collector.run_collection()
