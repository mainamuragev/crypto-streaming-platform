-- Create keyspace for crypto data
CREATE KEYSPACE IF NOT EXISTS crypto_data 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- Create table for crypto ticker data
CREATE TABLE IF NOT EXISTS crypto_data.crypto_ticker_24hr (
    symbol text,
    event_time timestamp,
    last_price decimal,
    price_change_percent decimal,
    volume decimal,
    high_price decimal,
    low_price decimal,
    open_price decimal,
    PRIMARY KEY (symbol, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Create table for top gainers (for Grafana dashboard)
CREATE TABLE IF NOT EXISTS crypto_data.top_gainers (
    event_time timestamp,
    symbol text,
    last_price decimal,
    price_change_percent decimal,
    volume decimal,
    PRIMARY KEY (event_time, symbol)
) WITH CLUSTERING ORDER BY (symbol ASC);
