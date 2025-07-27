#!/bin/bash
set -e

echo "=== Starting WeasyPrint build process ==="

# Step 1: Install Python packages
echo "Step 1: Installing Python packages..."
pip install -r requirements.txt

echo "=== Build process completed successfully ==="
