#!/bin/bash
echo "🚀 Starting Cryptocurrency Dashboard..."
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "phase_3_visualization" ]; then
    echo "❌ Error: Please run this script from project_101_crypto_pipeline directory"
    exit 1
fi

# Check if packages are installed
python3 -c "import streamlit, plotly, pandas" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ All packages are installed!"
    echo "📊 Launching dashboard..."
    echo "🌐 Dashboard will open at: http://localhost:8501"
    echo "⏹️  Press Ctrl+C to stop the dashboard"
    echo "=========================================="
    streamlit run phase_3_visualization/crypto_dashboard.py
else
    echo "📦 Packages still installing..."
    echo "💫 Please wait for installation to complete"
    echo "Then run: streamlit run phase_3_visualization/crypto_dashboard.py"
fi
