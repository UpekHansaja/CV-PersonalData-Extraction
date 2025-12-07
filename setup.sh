#!/bin/bash

# Quick Setup Script for CV Personal Data Extraction System
# This script automates the setup process

echo "======================================"
echo "CV Extraction System - Setup"
echo "======================================"
echo ""

# Check Python version
python3 --version 2>/dev/null || { echo "❌ Python 3 is required"; exit 1; }

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "ℹ️  .env file already exists"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "Setup Complete! ✓"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Run: python cv_extractor.py"
echo "3. Enter your CV folder path when prompted"
echo ""
echo "For more details, see README.md"
