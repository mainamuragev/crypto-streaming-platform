import streamlit as st
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta

# Try to import Cassandra
try:
    from cassandra.cluster import Cluster
    CASSANDRA_AVAILABLE = True
except ImportError:
    CASSANDRA_AVAILABLE = False

st.set_page_config(
    page_title="Crypto Dashboard - Live Data",
    page_icon="📊",
    layout="wide"
)

st.title("💰 Live Cryptocurrency Dashboard")
st.markdown("### Phase 3 - Real Cassandra Data")

def get_cassandra_data():
    """Get real data from Cassandra"""
    if not CASSANDRA_AVAILABLE:
        return None
    
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect('crypto_data')
        
        # Get the latest data for each symbol
        rows = session.execute("""
            SELECT symbol, event_time, last_price, price_change_percent, volume
            FROM crypto_ticker_24hr 
            ORDER BY event_time DESC
            LIMIT 100
        """)
        
        data = []
        for row in rows:
            data.append({
                'Symbol': row.symbol,
                'Time': row.event_time,
                'Price': float(row.last_price),
                'Change %': float(row.price_change_percent),
                'Volume': float(row.volume)
            })
        
        cluster.shutdown()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Cassandra connection failed: {e}")
        return None

def get_sample_data():
    """Fallback sample data"""
    symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'SOLUSDT']
    data = []
    
    for symbol in symbols:
        base_price = random.uniform(100, 50000)
        for i in range(5):
            data.append({
                'Symbol': symbol,
                'Time': datetime.now() - timedelta(hours=i),
                'Price': base_price,
                'Change %': random.uniform(-5, 5),
                'Volume': random.uniform(1000000, 50000000)
            })
    
    return pd.DataFrame(data)

# Sidebar
st.sidebar.title("🔧 Controls")

# Load data
with st.spinner("Loading data..."):
    df = get_cassandra_data()
    if df is None or df.empty:
        st.sidebar.warning("Using sample data - Cassandra not available")
        df = get_sample_data()
    else:
        st.sidebar.success("✅ Live Cassandra Data")

if not df.empty:
    # Get latest prices
    latest = df.sort_values('Time').groupby('Symbol').last().reset_index()
    
    # Display metrics
    st.subheader("📊 Market Overview")
    
    cols = st.columns(len(latest))
    for i, (_, row) in enumerate(latest.iterrows()):
        with cols[i]:
            st.metric(
                row['Symbol'],
                f"${row['Price']:,.2f}",
                f"{row['Change %']:+.2f}%"
            )
    
    # Price chart
    st.subheader("📈 Price History")
    selected = st.selectbox("Select Cryptocurrency", latest['Symbol'].unique())
    
    symbol_data = df[df['Symbol'] == selected].sort_values('Time')
    if not symbol_data.empty:
        fig = px.line(symbol_data, x='Time', y='Price', 
                      title=f"{selected} Price Movement")
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Raw Data")
    st.dataframe(latest, use_container_width=True)

# Status
st.sidebar.markdown("---")
if CASSANDRA_AVAILABLE:
    st.sidebar.success("Cassandra: Available")
else:
    st.sidebar.error("Cassandra: Not Installed")

st.sidebar.info(f"Records: {len(df)}")
st.sidebar.info(f"Symbols: {df['Symbol'].nunique()}")

# Footer
st.markdown("---")
st.caption("Project 101 Crypto Pipeline • Live Cassandra Data • Phase 3 Complete 🎉")
