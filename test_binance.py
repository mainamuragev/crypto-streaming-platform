import requests
import psycopg2
from datetime import datetime

def test_binance_connection():
    print("🔗 Testing Binance API connection...")
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT", timeout=10)
        data = response.json()
        print(f"✅ Binance API working - BTC price: ${float(data['lastPrice']):.2f}")
        return True
    except Exception as e:
        print(f"❌ Binance API failed: {e}")
        return False

def test_postgres_connection():
    print("🔗 Testing PostgreSQL connection...")
    try:
        conn = psycopg2.connect(
            host='localhost', port=5432,
            database='crypto_db', user='crypto_user', password='crypto_pass'
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM crypto_ticker_24hr")
        count = cur.fetchone()[0]
        print(f"✅ PostgreSQL working - {count} records in table")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Running connectivity tests...")
    binance_ok = test_binance_connection()
    postgres_ok = test_postgres_connection()
    
    if binance_ok and postgres_ok:
        print("🎉 All tests passed! Ready for data collection.")
    else:
        print("❌ Some tests failed. Please check the issues above.")
