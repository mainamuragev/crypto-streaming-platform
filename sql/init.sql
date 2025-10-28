-- Create database schema for crypto data
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

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_crypto_symbol_time ON crypto_ticker_24hr(symbol, created_at);
CREATE INDEX IF NOT EXISTS idx_crypto_created_at ON crypto_ticker_24hr(created_at);
CREATE INDEX IF NOT EXISTS idx_crypto_price_change ON crypto_ticker_24hr(price_change_percent DESC);

-- Enable logical replication for Debezium CDC
ALTER TABLE crypto_ticker_24hr REPLICA IDENTITY FULL;

-- Create a view for top gainers (will be useful for Grafana)
CREATE OR REPLACE VIEW top_gainers AS
SELECT 
    symbol,
    last_price,
    price_change_percent,
    volume,
    created_at
FROM crypto_ticker_24hr
WHERE created_at >= NOW() - INTERVAL '1 hour'
ORDER BY price_change_percent DESC
LIMIT 10;
