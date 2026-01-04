#!/bin/bash

# oneM2M Code Generator - Startup Script
# This script sets up and starts the Flask server

echo "oneM2M Code Generator - Starting..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment created!"
else
    source venv/bin/activate
    echo "Virtual environment activated!"
fi

echo ""
echo "Installing dependencies..."
pip install -r backend/requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo ""
    echo "Dependencies installed successfully!"
    echo ""
    echo "Starting oneM2M Code Generator..."
    echo "Server will be available at: http://localhost:5000"
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Start Flask server
    python app.py
else
    echo ""
    echo "Failed to install dependencies!"
    exit 1
fi
