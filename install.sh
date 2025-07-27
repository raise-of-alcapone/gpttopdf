#!/bin/bash
set -e

echo "=== Starting pdfkit/wkhtmltopdf build process for Render.com ==="

# Check if we're on Render.com (has specific environment)
if [ -n "$RENDER" ] || [ -n "$RENDER_SERVICE_NAME" ]; then
    echo "Detected Render.com environment"
    
    # On Render.com, we need to use the package manager differently
    echo "Installing wkhtmltopdf via render packages..."
    
    # Try to install wkhtmltopdf if available in the system
    if command -v wkhtmltopdf &> /dev/null; then
        echo "✅ wkhtmltopdf already available!"
        wkhtmltopdf --version
    else
        echo "⚠️ wkhtmltopdf not found - will try to continue with Python packages only"
        echo "Note: This may require manual package configuration on Render.com"
    fi
else
    echo "Local development environment detected"
    
    # For local Linux development
    if command -v apt-get &> /dev/null; then
        echo "Installing via apt-get..."
        sudo apt-get update
        sudo apt-get install -y wkhtmltopdf xvfb fonts-noto-color-emoji fonts-noto-emoji
    elif command -v yum &> /dev/null; then
        echo "Installing via yum..."
        sudo yum install -y wkhtmltopdf xorg-x11-server-Xvfb
    else
        echo "Package manager not found - please install wkhtmltopdf manually"
    fi
fi

# Install Python packages (this should work on Render.com)
echo "Installing Python packages..."
pip install -r requirements.txt

echo "=== Build process completed successfully ==="

# Test if wkhtmltopdf is available
if command -v wkhtmltopdf &> /dev/null; then
    echo "✅ wkhtmltopdf is available:"
    wkhtmltopdf --version
else
    echo "⚠️ wkhtmltopdf not found - app may need fallback configuration"
fi
