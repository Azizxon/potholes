#!/bin/bash

echo "🕳️  Pothole Detection System Setup"
echo "=================================="

# Check Python version
python_version=$(python --version 2>&1)
echo "Python version: $python_version"

# Try to install dependencies
echo "Installing dependencies..."

# Try to install required packages
pip install fastapi uvicorn python-multipart 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Basic dependencies installed successfully"
else
    echo "⚠️  Warning: Could not install some dependencies"
    echo "The system will run with basic functionality"
fi

# Try to install OpenCV and other advanced packages
echo "Attempting to install advanced packages..."
pip install opencv-python numpy pillow 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Advanced packages installed - full functionality available"
    USE_SIMPLE=false
else
    echo "⚠️  Advanced packages not available - using simple detector"
    USE_SIMPLE=true
fi

echo ""
echo "Starting Pothole Detection API..."
echo "Open http://localhost:8000 in your browser"
echo ""

# Start the appropriate version
if [ "$USE_SIMPLE" = true ]; then
    python simple_app.py
else
    python app.py
fi