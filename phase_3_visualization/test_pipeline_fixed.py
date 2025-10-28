import json
from kafka import KafkaProducer, KafkaAdminClient
from cassandra.cluster import Cluster
from datetime import datetime
import time
from decimal import Decimal

def test_kafka_connection():
    """Test Kafka connection and list topics"""
    print("🔍 Checking Kafka connection and topics...")

    try:
        # Test connection with admin client
        admin_client = KafkaAdminClient(
            bootstrap_servers=['localhost:9092'],
            request_timeout_ms=10000
        )

        # List topics to verify connection
        topics = admin_client.list_topics()
        print(f"✅ Connected to Kafka successfully!")
        print(f"📋 Available topics: {list(topics)}")
        admin_client.close()
        return True

    except Exception as e:
        print(f"❌ Kafka connection failed: {e}")
        return False

def test_kafka_producer():
    """Test producing messages to Kafka"""
    print("\n🧪 Testing Kafka producer...")

    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=30000,
            retries=3,
            acks='all'
        )

        # Create test message matching your table schema
        test_message = {
            "schema": {
                "type": "struct",
                "fields": [
                    {"type": "string", "optional": True, "field": "symbol"},
                    {"type": "string", "optional": True, "field": "event_time"},
                    {"type": "string", "optional": True, "field": "last_price"},
                    {"type": "string", "optional": True, "field": "price_change_percent"},
                    {"type": "string", "optional": True, "field": "volume"},
                    {"type": "string", "optional": True, "field": "high_price"},
                    {"type": "string", "optional": True, "field": "low_price"},
                    {"type": "string", "optional": True, "field": "open_price"}
                ],
                "optional": False,
                "name": "crypto_ticker_24hr.Value"
            },
            "payload": {
                "after": {
                    "symbol": "TESTUSDT",
                    "event_time": datetime.now().isoformat(),
                    "last_price": "123.45",
                    "price_change_percent": "2.5",
                    "volume": "10000.0",
                    "high_price": "125.00",
                    "low_price": "122.00",
                    "open_price": "123.00"
                },
                "op": "c",
                "ts_ms": int(time.time() * 1000)
            }
        }

        print(f"📤 Sending test message to topic: crypto_cdc.public.crypto_ticker_24hr")
        
        # Send to the topic
        future = producer.send('crypto_cdc.public.crypto_ticker_24hr', test_message)
        result = future.get(timeout=10)
        
        producer.flush()
        producer.close()
        
        print(f"✅ Test message sent successfully!")
        print(f"📨 Message sent to partition: {result.partition}, offset: {result.offset}")
        return True

    except Exception as e:
        print(f"❌ Failed to send message to Kafka: {e}")
        return False

def test_cassandra_connection():
    """Test Cassandra connection with correct schema"""
    print("\n🔍 Testing Cassandra connection...")
    
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect()
        
        # Use your keyspace
        session.set_keyspace('crypto_data')
        
        # Test insert with correct column names and types
        insert_stmt = session.prepare("""
            INSERT INTO crypto_ticker_24hr (
                symbol, event_time, last_price, price_change_percent, volume,
                high_price, low_price, open_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """)
        
        test_event_time = datetime.now()
        session.execute(insert_stmt, (
            'TESTUSDT', 
            test_event_time,
            Decimal('123.45'), 
            Decimal('2.5'), 
            Decimal('10000.0'),
            Decimal('125.00'),
            Decimal('122.00'), 
            Decimal('123.00')
        ))
        
        # Test read back
        rows = session.execute("""
            SELECT symbol, last_price, price_change_percent 
            FROM crypto_ticker_24hr 
            WHERE symbol = 'TESTUSDT'
        """)
        
        for row in rows:
            print(f"✅ Cassandra test: {row.symbol} - ${row.last_price} ({row.price_change_percent}%)")
        
        cluster.shutdown()
        return True
        
    except Exception as e:
        print(f"❌ Cassandra connection test failed: {e}")
        return False

def test_existing_cassandra_data():
    """Test reading existing data from Cassandra"""
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect('crypto_data')
        
        # Count records
        count_result = session.execute("SELECT COUNT(*) as total FROM crypto_ticker_24hr")
        total_records = count_result.one().total
        print(f"📊 Current records in Cassandra: {total_records}")
        
        # Get sample data
        rows = session.execute("""
            SELECT symbol, last_price, price_change_percent 
            FROM crypto_ticker_24hr 
            LIMIT 5
        """)
        
        print("📋 Sample data:")
        for row in rows:
            print(f"  {row.symbol}: ${row.last_price} ({row.price_change_percent}%)")
        
        cluster.shutdown()
        return True
        
    except Exception as e:
        print(f"❌ Existing data test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Crypto Pipeline Components...")
    print("=" * 50)
    
    # Test Cassandra
    cassandra_success = test_cassandra_connection()
    if cassandra_success:
        test_existing_cassandra_data()
    
    # Test Kafka
    kafka_connected = test_kafka_connection()
    kafka_producer_success = False
    if kafka_connected:
        kafka_producer_success = test_kafka_producer()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"  Cassandra connection: {'✅' if cassandra_success else '❌'}")
    print(f"  Kafka connection: {'✅' if kafka_connected else '❌'}")
    print(f"  Kafka producer: {'✅' if kafka_producer_success else '❌'}")
    
    if cassandra_success:
        print("\n🎉 Cassandra is working! Ready for Phase 3 visualization.")
    else:
        print("\n💡 Please check your Cassandra connection.")

if __name__ == "__main__":
    main()
