#!/bin/bash
set -e

echo "=== Starting custom build process ==="

# Step 1: Install Python packages
echo "Step 1: Installing Python packages..."
pip install -r requirements.txt

# Step 2: Install Playwright Chromium
echo "Step 2: Installing Playwright Chromium..."
python -m playwright install chromium

# Step 3: Verify installation
echo "Step 3: Verifying Chromium installation..."
ls -la /opt/render/.cache/ms-playwright/

echo "=== Build process completed successfully ==="
