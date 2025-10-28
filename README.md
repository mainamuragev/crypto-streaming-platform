```bash
cat > README.md << 'EOF'
# Crypto Streaming Platform

Real-time cryptocurrency data pipeline with Kafka, Cassandra, and Streamlit.

## Quick Start

```bash
# Start services
docker-compose up -d

# Run dashboard
streamlit run phase_3_visualization/working_dashboard.py
```

## What's Included

- Data Ingestion: Binance API to PostgreSQL
- Stream Processing: Kafka with Debezium CDC  
- Storage: Cassandra for time-series data
- Visualization: Streamlit dashboards

## Architecture

```
Binance API -> PostgreSQL -> Kafka -> Cassandra -> Streamlit
```

## Features

- Real-time cryptocurrency price tracking
- Interactive charts and metrics
- Multiple dashboard versions
- Docker containerization

## Tech Stack

- Apache Kafka and Debezium
- Cassandra and PostgreSQL
- Streamlit and Plotly
- Docker and Python

## Project Structure

```
phase_1_binance_ingest/    # Data collection
phase_2_cdc_setup/         # Kafka configuration  
phase_3_visualization/     # Dashboards
docker-compose.yml         # Services
```

**Dashboard**: http://localhost:8501

<img width="1920" height="1080" alt="Screenshot 2025-10-28 161013" src="https://github.com/user-attachments/assets/8ee42f5b-d876-456d-86cc-9a9b1f04f7df" />
<img width="1920" height="1080" alt="Screenshot 2025-10-28 161413" src="https://github.com/user-attachments/assets/5451eb65-f4b3-483f-afa6-c94c47862227" />
<img width="1920" height="1080" alt="Screenshot 2025-10-28 161433" src="https://github.com/user-attachments/assets/6629c46c-bfb1-4ba3-b3cb-70b014627f0b" />

