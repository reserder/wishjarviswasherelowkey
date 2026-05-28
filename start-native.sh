#!/bin/bash
# AEGIS NATIVE ENGINE STARTUP
echo "🚀 Starting AEGIS OS Natively (Zero Latency Mode)..."

# Ensure venv is used
source venv/bin/activate

# Add backend to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/backend

# Start the server
python3 backend/main.py
