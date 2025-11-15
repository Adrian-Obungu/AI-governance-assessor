#!/bin/bash
echo "🔍 Testing AI Governance Pro Setup"
echo "==================================="

# Check Python
echo "Python version: $(python3 --version)"
echo "Streamlit version: $(streamlit version)"

# Check if main app exists
if [ -f "src/app/main.py" ]; then
    echo "✅ Main application found"
else
    echo "❌ Main application missing"
fi

# Check requirements
if [ -f "requirements.txt" ]; then
    echo "✅ Requirements file found"
else
    echo "❌ Requirements file missing"
fi

echo ""
echo "🚀 To start the application:"
echo "   streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0"
echo ""
echo "🔧 If ports don't auto-forward:"
echo "   1. Go to Ports tab"
echo "   2. Add port 8501 manually"
echo "   3. Set to Public visibility"
