import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Try to import Cassandra, but provide fallback if not available
try:
    from cassandra.cluster import Cluster
    CASSANDRA_AVAILABLE = True
except ImportError:
    CASSANDRA_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Cryptocurrency Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #00D4AA;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #0E1117;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #262730;
    }
    .positive {
        color: #00FF00;
    }
    .negative {
        color: #FF0000;
    }
</style>
""", unsafe_allow_html=True)

def get_cassandra_data():
    """Fetch data from Cassandra if available"""
    if not CASSANDRA_AVAILABLE:
        return pd.DataFrame()
    
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect('crypto_data')
        
        # Get data from Cassandra
        rows = session.execute("""
            SELECT symbol, event_time, last_price, price_change_percent, volume,
                   high_price, low_price, open_price
            FROM crypto_ticker_24hr 
            ORDER BY event_time DESC
            LIMIT 100
        """)
        
        data = []
        for row in rows:
            data.append({
                'symbol': row.symbol,
                'timestamp': row.event_time,
                'price': float(row.last_price) if row.last_price else 0,
                'price_change_percent': float(row.price_change_percent) if row.price_change_percent else 0,
                'volume': float(row.volume) if row.volume else 0,
                'high': float(row.high_price) if row.high_price else 0,
                'low': float(row.low_price) if row.low_price else 0,
                'open': float(row.open_price) if row.open_price else 0
            })
        
        cluster.shutdown()
        return pd.DataFrame(data)
    
    except Exception as e:
        st.sidebar.error(f"Cassandra error: {e}")
        return pd.DataFrame()

def get_sample_data():
    """Generate sample data for demonstration"""
    symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'SOLUSDT', 'LINKUSDT']
    data = []
    
    for i, symbol in enumerate(symbols):
        base_price = [45000, 3500, 1.25, 25, 120, 18][i]
        base_volume = [25000000, 15000000, 5000000, 8000000, 12000000, 3000000][i]
        base_change = [2.5, 1.8, -0.5, 3.2, 5.2, 4.5][i]
        
        # Create multiple time points for each symbol
        for j in range(10):
            data.append({
                'symbol': symbol,
                'timestamp': datetime.now() - timedelta(hours=j),
                'price': base_price + (j * 10 * (i+1)),
                'price_change_percent': base_change + (j * 0.1),
                'volume': base_volume + (j * 100000),
                'high': base_price + 100 * (i+1),
                'low': base_price - 50 * (i+1),
                'open': base_price
            })
    
    return pd.DataFrame(data)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Cryptocurrency Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Data source selection
    data_source = st.sidebar.radio(
        "Data Source:",
        ["Live Cassandra Data", "Sample Data"],
        index=1 if not CASSANDRA_AVAILABLE else 0
    )
    
    # Refresh control
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Data source info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Source Info")
    
    if data_source == "Live Cassandra Data" and CASSANDRA_AVAILABLE:
        st.sidebar.info("📊 Live Cassandra Data")
        with st.spinner("Loading data from Cassandra..."):
            df = get_cassandra_data()
        
        if df.empty:
            st.sidebar.warning("No data found in Cassandra")
            st.sidebar.info("Switching to sample data")
            df = get_sample_data()
    else:
        st.sidebar.warning("📊 Sample Data (Demo)")
        df = get_sample_data()
    
    if not CASSANDRA_AVAILABLE:
        st.sidebar.error("Cassandra driver not installed")
        st.sidebar.info("Run: pip install cassandra-driver")
    
    st.sidebar.markdown(f"**Total Records:** {len(df):,}")
    st.sidebar.markdown(f"**Unique Symbols:** {df['symbol'].nunique()}")
    
    # Get unique symbols
    symbols = sorted(df['symbol'].unique().tolist())
    
    # Symbol selector
    selected_symbol = st.sidebar.selectbox("🔍 Select Cryptocurrency", symbols)
    
    # Filter data for selected symbol
    symbol_df = df[df['symbol'] == selected_symbol].sort_values('timestamp')
    
    if symbol_df.empty:
        st.warning(f"No data found for {selected_symbol}")
        return
    
    # Latest data
    latest = symbol_df.iloc[0]
    
    # Key Metrics Row
    st.subheader(f"📊 {selected_symbol} - Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if latest['price_change_percent'] >= 0 else "inverse"
        st.metric(
            label="💵 Current Price",
            value=f"${latest['price']:,.2f}",
            delta=f"{latest['price_change_percent']:.2f}%",
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            label="📈 24h High",
            value=f"${latest['high']:,.2f}"
        )
    
    with col3:
        st.metric(
            label="📉 24h Low",
            value=f"${latest['low']:,.2f}"
        )
    
    with col4:
        st.metric(
            label="💰 24h Volume",
            value=f"${latest['volume']:,.0f}"
        )
    
    # Charts Section
    st.markdown("---")
    st.subheader("📈 Price Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price chart
        fig_price = px.line(
            symbol_df, 
            x='timestamp', 
            y='price',
            title=f"🔄 {selected_symbol} Price History",
            labels={'price': 'Price (USD)', 'timestamp': 'Time'}
        )
        fig_price.update_layout(
            showlegend=False,
            hovermode='x unified'
        )
        fig_price.update_traces(line=dict(color='#00D4AA', width=3))
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        # Volume chart
        fig_volume = px.area(
            symbol_df,
            x='timestamp',
            y='volume',
            title=f"💧 {selected_symbol} Trading Volume",
            labels={'volume': 'Volume (USD)', 'timestamp': 'Time'}
        )
        fig_volume.update_layout(
            showlegend=False,
            hovermode='x unified'
        )
        fig_volume.update_traces(fillcolor='rgba(0, 212, 170, 0.3)', line=dict(color='#00D4AA'))
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # Market Overview Section
    st.markdown("---")
    st.subheader("🌐 Market Overview - All Cryptocurrencies")
    
    # Latest prices for all symbols
    latest_prices = df.sort_values('timestamp').groupby('symbol').last().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price change bar chart
        fig_changes = px.bar(
            latest_prices,
            x='symbol',
            y='price_change_percent',
            title="📊 24h Price Change %",
            color='price_change_percent',
            color_continuous_scale=['red', 'white', 'green'],
            labels={'price_change_percent': 'Price Change %', 'symbol': 'Cryptocurrency'}
        )
        fig_changes.update_layout(showlegend=False)
        st.plotly_chart(fig_changes, use_container_width=True)
    
    with col2:
        # Price vs Volume scatter
        fig_comparison = px.scatter(
            latest_prices,
            x='volume',
            y='price',
            size='price',
            color='price_change_percent',
            hover_name='symbol',
            title="⚖️ Price vs Volume Analysis",
            labels={'price': 'Price (USD)', 'volume': 'Volume (USD)', 'price_change_percent': 'Change %'},
            color_continuous_scale=['red', 'yellow', 'green']
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Data Tables Section
    st.markdown("---")
    st.subheader("📋 Detailed Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Raw data table
        st.write(f"**{selected_symbol} - Recent Data**")
        display_df = symbol_df[['timestamp', 'price', 'price_change_percent', 'volume', 'high', 'low']].head(10).copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        display_df['price'] = display_df['price'].apply(lambda x: f"${x:,.2f}")
        display_df['volume'] = display_df['volume'].apply(lambda x: f"${x:,.0f}")
        display_df['high'] = display_df['high'].apply(lambda x: f"${x:,.2f}")
        display_df['low'] = display_df['low'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display_df, use_container_width=True)
    
    with col2:
        # Statistics
        st.write("**📊 Quick Stats**")
        st.metric("Data Points", len(symbol_df))
        st.metric("Avg Price", f"${symbol_df['price'].mean():.2f}")
        st.metric("Max Change", f"{symbol_df['price_change_percent'].max():.2f}%")
        st.metric("Total Volume", f"${symbol_df['volume'].sum():,.0f}")
    
    # Installation Status
    if not CASSANDRA_AVAILABLE:
        st.markdown("---")
        st.warning("""
        ## 📦 Package Installation Status
        Cassandra driver is not yet installed. The dashboard is currently showing sample data.
        
        Once the pip installation completes, restart the dashboard to see live Cassandra data.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit, Plotly, and Apache Cassandra | "
        "Project 101 Crypto Pipeline | Phase 3 Visualization"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
