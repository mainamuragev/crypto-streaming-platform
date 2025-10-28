import json
from kafka import KafkaProducer
from cassandra.cluster import Cluster
from datetime import datetime

def test_kafka_producer():
    """Test producing messages to Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        test_message = {
            "after": {
                "symbol": "TESTUSDT",
                "last_price": 123.45,
                "price_change_percent": 2.5,
                "volume": 10000.0
            }
        }
        
        producer.send('crypto_cdc.public.crypto_ticker_24hr', test_message)
        producer.flush()
        print("✅ Test message sent to Kafka")
        return True
    except Exception as e:
        print(f"❌ Kafka producer test failed: {e}")
        return False

def test_cassandra_connection():
    """Test Cassandra connection and insert"""
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect('crypto_data')
        
        # Insert test data
        session.execute("""
            INSERT INTO crypto_ticker_24hr 
            (symbol, event_time, last_price, price_change_percent, volume, high_price, low_price, open_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            "TESTUSDT", 
            datetime.now(),
            123.45, 
            2.5, 
            10000.0,
            130.0,
            120.0,
            121.0
        ))
        
        # Query to verify
        rows = session.execute("SELECT symbol, last_price FROM crypto_ticker_24hr WHERE symbol = 'TESTUSDT'")
        for row in rows:
            print(f"✅ Cassandra test: {row.symbol} - ${row.last_price}")
        
        cluster.shutdown()
        return True
    except Exception as e:
        print(f"❌ Cassandra test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing pipeline components...")
    kafka_ok = test_kafka_producer()
    cassandra_ok = test_cassandra_connection()
    
    if kafka_ok and cassandra_ok:
        print("🎉 All pipeline tests passed!")
    else:
        print("❌ Some tests failed")
