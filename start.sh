#!/bin/bash
# SurakshaVaani Pro - Local Launch Script
# Usage: bash start.sh

set -e
cd "$(dirname "$0")"

VENV=./venv

echo "======================================"
echo "  🛡️  SurakshaVaani Pro - Launcher   "
echo "======================================"

# 1. Check venv
if [ ! -d "$VENV" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3.11 -m venv venv"
    echo "   venv/bin/pip install -r requirements.txt"
    exit 1
fi

# 2. Check / create model
if [ ! -f "models/surakshavaani_final.h5" ] || [ "$(wc -c < models/surakshavaani_final.h5)" -lt 1000 ]; then
    echo ""
    echo "⚠️  No valid model found. Creating placeholder model..."
    $VENV/bin/python create_dummy_model.py
fi

# 3. Kill any existing server on port 8000 / 8501
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8501 | xargs kill -9 2>/dev/null || true
sleep 1

# 4. Start FastAPI backend
echo ""
echo "🚀 Starting FastAPI Backend on http://localhost:8000 ..."
$VENV/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!
echo "   Backend PID: $API_PID"

# 5. Wait for backend to be ready
echo "   Waiting for backend..."
for i in {1..20}; do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo "   ✅ Backend is ready!"
        break
    fi
    sleep 1
done

# 6. Start Streamlit frontend
echo ""
echo "🎛️  Starting Streamlit Dashboard on http://localhost:8501 ..."
$VENV/bin/streamlit run dashboard.py --server.port 8501 --server.headless true &
DASH_PID=$!
echo "   Dashboard PID: $DASH_PID"

echo ""
echo "======================================"
echo "  ✅ All services running!"
echo "  📡 API:       http://localhost:8000"
echo "  🖥️  Dashboard: http://localhost:8501"
echo "  📖 API Docs:  http://localhost:8000/docs"
echo "======================================"
echo ""
echo "  Press Ctrl+C to stop all services."
echo ""

# Wait for both processes
wait $API_PID $DASH_PID
