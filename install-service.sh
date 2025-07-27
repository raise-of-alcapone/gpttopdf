#!/bin/bash

# Installation script for systemd service
# Run this on your VPC server

set -e

APP_NAME="gpttopdf"
APP_USER="www-data"
APP_DIR="/opt/gpttopdf"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"

echo "📦 Installing $APP_NAME as systemd service..."

# Create application directory
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR

# Clone repository (adjust URL as needed)
echo "📥 Cloning repository..."
sudo -u $APP_USER git clone https://github.com/raise-of-alcapone/gpttopdf.git $APP_DIR
cd $APP_DIR

# Create virtual environment
echo "🐍 Setting up Python environment..."
sudo -u $APP_USER python3 -m venv venv
sudo -u $APP_USER ./venv/bin/pip install -r requirements.txt
sudo -u $APP_USER ./venv/bin/playwright install chromium
sudo -u $APP_USER ./venv/bin/playwright install-deps chromium

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=GPT to PDF Flask Application
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME

echo "✅ Installation completed!"
echo "🔧 Service status: sudo systemctl status $APP_NAME"
echo "📜 View logs: sudo journalctl -u $APP_NAME -f"
