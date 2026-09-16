#!/bin/bash

# SurakshaVaani Pro - Quick Test Script
# Tests the improved emotion detection with sample analysis

echo "🛡️ SurakshaVaani Pro - Emotion Detection Test"
echo "=============================================="
echo ""

# Check if server is running
echo "📡 Checking API server status..."
curl -s http://127.0.0.1:8000/ > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ API Server is running on http://127.0.0.1:8000"
else
    echo "❌ API Server is NOT running!"
    echo "   Start it with: source venv/bin/activate && python -m uvicorn api.main:app --host 127.0.0.1 --port 8000"
    exit 1
fi

echo ""
echo "📊 Current Improvements Active:"
echo "   ✅ Multi-Feature Extraction (Mel + MFCC + Spectral + Chroma)"
echo "   ✅ Acoustic Post-Processing Corrector"
echo "   ✅ Anger vs Fear Distinction Rules"
echo ""
echo "🎯 Test Instructions:"
echo "   1. Open dashboard: http://localhost:8501"
echo "   2. Upload an angry voice sample"
echo "   3. Check server terminal for correction log:"
echo "      🎯 Raw Prediction: fear (0.75) → Corrected: angry (0.85)"
echo ""
echo "📝 To view detailed improvements:"
echo "   cat AI_MODEL_IMPROVEMENTS.md"
echo ""
echo "🔧 To adjust correction thresholds:"
echo "   Edit: src/emotion_corrector.py"
echo ""
echo "Ready to test! 🚀"
