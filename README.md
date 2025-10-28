
# 🚀 Crypto Streaming Platform

A real-time cryptocurrency data pipeline with streaming, storage, and visualization capabilities. This project demonstrates a complete data engineering workflow for processing live cryptocurrency market data.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-Streaming-orange)
![Cassandra](https://img.shields.io/badge/Cassandra-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)

## 📊 Live Dashboard
**Access the real-time dashboard:** [http://localhost:8501](http://localhost:8501)

![Dashboard Preview](https://via.placeholder.com/800x400/0D1117/00D4AA?text=Crypto+Analytics+Dashboard)

## 🏗️ Architecture Overview

```
Binance API → Kafka → Debezium CDC → Cassandra → Streamlit Dashboard
     ↓
 PostgreSQL → Grafana (Monitoring)
```

## 🎯 Features

- **Real-time Data Ingestion**: Live cryptocurrency prices from Binance API
- **Stream Processing**: Apache Kafka with Debezium Change Data Capture
- **Time-Series Storage**: Apache Cassandra for high-performance data storage
- **Interactive Visualization**: Multiple Streamlit dashboards with Plotly charts
- **Containerized Deployment**: Full Docker Compose setup
- **Real-time Analytics**: Market trends, price movements, and volume analysis

## 📁 Project Structure

```
crypto-streaming-platform/
├── phase_1_binance_ingest/          # Data collection from Binance API
├── phase_2_cdc_setup/               # Kafka & Debezium configuration
├── phase_3_visualization/           # Streamlit dashboards
│   ├── working_dashboard.py         # Basic dashboard
│   ├── plotly_dashboard.py          # Enhanced with interactive charts
│   └── cassandra_dashboard.py       # Real Cassandra data connection
├── sql/                             # Database schemas
├── data/                            # Sample data files
├── docker-compose.yml               # Container orchestration
├── database_config.py              # Database configuration
├── config_loader.py                # Environment configuration
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment template
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Streaming** | Apache Kafka, Debezium | Real-time data pipeline |
| **Database** | Apache Cassandra, PostgreSQL | Time-series and relational storage |
| **Visualization** | Streamlit, Plotly | Interactive dashboards |
| **Monitoring** | Grafana | System metrics |
| **Containers** | Docker, Docker Compose | Deployment |
| **Languages** | Python, CQL, SQL | Application logic |

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/mainamuragev/crypto-streaming-platform.git
cd crypto-streaming-platform
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services
```bash
# Start all services (Kafka, Cassandra, PostgreSQL, Debezium)
docker-compose up -d
```

### 4. Run Dashboard
```bash
# Setup Python environment
python -m venv crypto_venv
source crypto_venv/bin/activate
pip install -r requirements.txt

# Launch dashboard
streamlit run phase_3_visualization/working_dashboard.py
```

### 5. Access Applications
- **Dashboard**: http://localhost:8501
- **Grafana**: http://localhost:3000
- **Kafka Connect**: http://localhost:8083

## 📈 Dashboard Features

### 🔍 Real-time Metrics
- Live cryptocurrency prices
- 24-hour price changes
- Trading volume analytics
- Market cap information

### 📊 Interactive Charts
- Price history with time series
- Volume analysis
- Market comparison charts
- Price vs Volume scatter plots

### 🌐 Market Overview
- Multiple cryptocurrency support
- Performance comparison
- Market trends visualization
- Real-time data updates

## 🗄️ Database Schema

### Cassandra Table: `crypto_ticker_24hr`
```sql
CREATE TABLE crypto_data.crypto_ticker_24hr (
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
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file from the template:
```bash
# Database
POSTGRES_PASSWORD=your_password
CASSANDRA_HOSTS=localhost

# API Keys (optional)
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
```

### Docker Services
The platform includes:
- **Zookeeper**: Kafka coordination
- **Kafka**: Message brokering
- **PostgreSQL**: Source database
- **Cassandra**: Time-series storage
- **Debezium**: Change Data Capture
- **Grafana**: Monitoring

## 🎮 Usage Examples

### View Basic Dashboard
```bash
streamlit run phase_3_visualization/working_dashboard.py
```

### Advanced Dashboard with Plotly
```bash
streamlit run phase_3_visualization/plotly_dashboard.py
```

### Connect to Real Cassandra Data
```bash
streamlit run phase_3_visualization/cassandra_dashboard.py
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, fork the repository, and create pull requests.

### Areas for Improvement
- Additional data sources (more exchanges)
- Machine learning price predictions
- Alert systems and notifications
- Mobile application interface
- Advanced analytics features

## 📊 Project Phases

### Phase 1: Data Ingestion
- Binance API integration
- Real-time price streaming
- Data validation and formatting

### Phase 2: CDC Setup
- Kafka topics configuration
- Debezium connectors
- Database replication setup

### Phase 3: Visualization
- Multiple dashboard versions
- Interactive charts
- Real-time data display

## 🐛 Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 8501, 3000, 8083 are available
2. **Docker memory**: Allocate sufficient memory for containers
3. **API limits**: Respect Binance API rate limits

### Logs and Debugging
```bash
# View container logs
docker-compose logs -f

# Check service status
docker-compose ps
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Binance](https://www.binance.com/) for market data API
- [Apache Foundation](https://www.apache.org/) for Kafka and Cassandra
- [Streamlit](https://streamlit.io/) for visualization framework
- [Docker](https://www.docker.com/) for containerization

---

**⭐ Star this repo if you find it helpful!**

**Built with  for Data Engineering **
EOF
```
