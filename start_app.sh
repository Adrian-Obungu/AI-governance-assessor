#!/bin/bash
echo "🚀 Starting AI Governance Pro on port 8501..."
echo "If the port doesn't auto-forward, manually forward port 8501 in Codespaces"

# Start Streamlit with explicit port and configuration
streamlit run src/app/main.py     --server.port=8501     --server.address=0.0.0.0     --server.headless=true     --browser.serverAddress="0.0.0.0"     --browser.gatherUsageStats=false

echo "Streamlit process ended"
