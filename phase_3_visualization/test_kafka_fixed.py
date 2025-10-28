from kafka import KafkaProducer, KafkaAdminClient
import json
from datetime import datetime

def test_kafka_fixed():
    print("🔧 Testing Kafka with fixed configuration...")
    
    try:
        # Use simpler configuration
        admin_client = KafkaAdminClient(
            bootstrap_servers=['localhost:9092'],
            request_timeout_ms=15000,
            api_version_auto_timeout_ms=30000
        )
        
        topics = admin_client.list_topics()
        print(f"✅ Admin client connected! Topics: {list(topics)}")
        admin_client.close()
        
        # Test producer
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=15000,
            retries=2
        )
        
        test_msg = {
            "test": "message",
            "timestamp": datetime.now().isoformat(),
            "data": {"symbol": "TEST", "price": 100.0}
        }
        
        # Try sending to a simple topic first
        future = producer.send('test-cdc', test_msg)
        result = future.get(timeout=10)
        
        print(f"✅ Producer test passed! Partition: {result.partition}, Offset: {result.offset}")
        producer.close()
        return True
        
    except Exception as e:
        print(f"❌ Kafka test failed: {e}")
        return False

if __name__ == "__main__":
    test_kafka_fixed()
