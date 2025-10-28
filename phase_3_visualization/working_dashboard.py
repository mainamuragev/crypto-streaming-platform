import streamlit as st
import random
from datetime import datetime, timedelta

# Simple dashboard without complex dependencies
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("💰 Cryptocurrency Dashboard")
st.markdown("### Phase 3 Visualization - Real-time Market Data")

# Sample data
cryptos = {
    'BTCUSDT': {'price': 45250.75, 'change': 2.34, 'volume': '28.4M'},
    'ETHUSDT': {'price': 3489.25, 'change': 1.67, 'volume': '15.7M'},
    'ADAUSDT': {'price': 1.28, 'change': -0.45, 'volume': '5.2M'},
    'DOTUSDT': {'price': 26.45, 'change': 3.12, 'volume': '8.5M'},
    'SOLUSDT': {'price': 122.80, 'change': 5.23, 'volume': '12.3M'},
}

# Sidebar
st.sidebar.title("Controls")
selected = st.sidebar.selectbox("Choose Crypto", list(cryptos.keys()))

# Display metrics
st.subheader(f"📊 {selected} Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Price", 
        f"${cryptos[selected]['price']:,.2f}",
        f"{cryptos[selected]['change']:+.2f}%"
    )

with col2:
    st.metric("24h Volume", cryptos[selected]['volume'])

with col3:
    st.metric("Market Cap", "Simulated")

# Price chart simulation
st.subheader("📈 Price Movement")

# Generate sample price data
dates = [datetime.now() - timedelta(hours=x) for x in range(24, 0, -1)]
base_price = cryptos[selected]['price']
prices = [base_price * (1 + random.uniform(-0.02, 0.02)) for _ in dates]

# Simple chart using native streamlit
chart_data = {"Time": [d.strftime('%H:%M') for d in dates], "Price": prices}
st.line_chart(chart_data)

# All cryptocurrencies table
st.subheader("🌐 Market Overview")

for symbol, data in cryptos.items():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**{symbol}**")
    with col2:
        st.write(f"${data['price']:,.2f}")
    with col3:
        color = "green" if data['change'] >= 0 else "red"
        st.markdown(f"<span style='color: {color}'>{data['change']:+.2f}%</span>", unsafe_allow_html=True)
    st.progress(min(abs(data['change']) / 10, 1.0))

# Status
st.sidebar.markdown("---")
st.sidebar.success("✅ Dashboard Running")
st.sidebar.info("Streamlit 1.28.0")

# Footer
st.markdown("---")
st.caption("Project 101 Crypto Pipeline • Phase 3 Visualization")
