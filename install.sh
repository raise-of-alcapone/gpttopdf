#!/bin/bash
set -e

echo "=== Starting custom build process ==="

# Step 1: Install Python packages
echo "Step 1: Installing Python packages..."
pip install -r requirements.txt

# Step 2: Install Playwright Chromium
echo "Step 2: Installing Playwright Chromium..."
python -m playwright install chromium

# Step 3: Create symlinks for Playwright's expected paths
echo "Step 3: Creating browser symlinks..."
cd /opt/render/.cache/ms-playwright

# Create the expected directory structure
if [ -d "chromium-1181" ] && [ ! -d "chromium_headless_shell-1181/chrome-linux" ]; then
    echo "Creating symlink for chromium_headless_shell..."
    mkdir -p chromium_headless_shell-1181/chrome-linux
    ln -sf ../../chromium-1181/chrome-linux/chrome chromium_headless_shell-1181/chrome-linux/headless_shell
fi

# Step 4: Verify installation
echo "Step 4: Verifying Chromium installation..."
ls -la /opt/render/.cache/ms-playwright/
echo "Checking headless_shell symlink..."
ls -la /opt/render/.cache/ms-playwright/chromium_headless_shell-1181/chrome-linux/

echo "=== Build process completed successfully ==="
