#!/bin/bash
# AEGIS EMERGENCY RECOVERY SCRIPT
# This script bypasses Docker completely to fix the "500 Error" and "Not Responding" issues.

echo "🚨 AEGIS OS: STARTING EMERGENCY RECOVERY..."

# 1. KILL ALL STUCK PROCESSES
echo "🧹 Cleaning up stuck processes..."
pkill -9 -f "Docker" || true
pkill -9 -f "uvicorn" || true
pkill -9 -f "python" || true
pkill -9 -f "Ollama" || true

# 2. CLEAR TEMP FILES
echo "🗑 Clearing temporary system locks..."
rm -f backend.log
rm -rf backend/__pycache__

# 3. RESTART OLLAMA (The local AI engine)
echo "🧠 Restarting Ollama..."
open -a Ollama
sleep 5

# 4. START AEGIS NATIVELY (Zero Latency)
echo "🚀 Launching AEGIS OS (Native Mode)..."
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/backend
export OLLAMA_BASE_URL=http://localhost:11434
export LITELLM_BASE_URL=http://localhost:4000/v1

# Start the backend in the background
python3 backend/main.py > backend.log 2>&1 &

echo "----------------------------------------------------"
echo "✅ RECOVERY COMPLETE"
echo "----------------------------------------------------"
echo "1. Wait 10 seconds for the brain to wake up."
echo "2. OPEN THIS LINK: http://localhost:8001/health"
echo "3. If you see 'online', the 500 error is DEAD."
echo "----------------------------------------------------"
echo "Note: If it still says 500, please empty your TRASH."
