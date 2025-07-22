#!/bin/bash
# Auto environment setup and repair script

echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬇️ Installing requirements..."
pip install --upgrade pip setuptools wheel

if pip install -r requirements.txt; then
    echo "✅ Requirements installed successfully."
else
    echo "⚠️ Initial install failed. Attempting to auto-repair..."
    pip cache purge
    pip install --no-cache-dir -r requirements.txt
fi

echo "📦 Installed packages:"
pip list
