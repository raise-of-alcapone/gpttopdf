#!/bin/bash

# Nginx Setup Script for GPTtoPDF
# Run this ONCE on your VPC server

set -e

echo "🌐 Setting up Nginx for GPTtoPDF..."

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing Nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Get server IP for configuration
SERVER_IP=$(curl -s ifconfig.me)
echo "🔍 Detected server IP: $SERVER_IP"

# Create Nginx configuration
echo "⚙️ Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/gpttopdf > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    # Large file uploads for PDFs
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts for PDF generation
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
        proxy_send_timeout 300s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable the site
echo "🔗 Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/gpttopdf /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

# Restart Nginx
echo "🔄 Restarting Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# Check status
echo "📊 Nginx status:"
sudo systemctl status nginx --no-pager

echo "✅ Nginx setup completed!"
echo "🌐 Your app should now be available at: http://$SERVER_IP"
echo "🔧 Docker app runs on localhost:5000 (internal)"
echo "🌍 Nginx forwards port 80 to Docker app"
