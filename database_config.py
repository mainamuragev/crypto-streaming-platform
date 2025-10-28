# Database configuration - replace with your actual credentials
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'crypto_db',
    'user': 'crypto_user',
    'password': 'your_password_here'  # Replace with actual password
}

CASSANDRA_CONFIG = {
    'hosts': ['localhost'],
    'port': 9042,
    'keyspace': 'crypto_data'
}
