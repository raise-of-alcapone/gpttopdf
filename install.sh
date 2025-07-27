#!/bin/bash
set -e

echo "=== Starting pdfkit/wkhtmltopdf build process ==="

# Step 1: Update package list
echo "Step 1: Updating package list..."
apt-get update

# Step 2: Install wkhtmltopdf for pdfkit with color emoji support
echo "Step 2: Installing wkhtmltopdf with dependencies..."
apt-get install -y wkhtmltopdf xvfb

# Step 3: Install font packages for better emoji support
echo "Step 3: Installing emoji fonts..."
apt-get install -y fonts-noto-color-emoji fonts-noto-emoji

# Step 4: Install Python packages
echo "Step 4: Installing Python packages..."
pip install -r requirements.txt

echo "=== Build process completed successfully ==="
echo "wkhtmltopdf version:"
wkhtmltopdf --version
echo "Available emoji fonts installed!"
