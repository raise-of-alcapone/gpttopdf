#!/bin/bash


# Nginx Setup Script for Blockz (blockz.gravityfight.de)
# Run this AFTER DNS is configured

set -e

echo "🌐 Setting up Nginx for blockz.gravityfight.de..."

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing Nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Create Nginx configuration for both domains

CONFIG_PATH="/etc/nginx/sites-available/blockz"
echo "⚙️ Creating Nginx configuration..."
sudo tee "$CONFIG_PATH" > /dev/null <<'EOF'
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/m;
limit_req_zone $binary_remote_addr zone=pdf:10m rate=3r/m;

server {
    listen 80;
    server_name blockz.gravityfight.de;

    # Large file uploads for Markdown/Docs
    client_max_body_size 50M;
    client_body_timeout 60s;
    client_header_timeout 60s;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()";
    server_tokens off;

    location / {
        limit_req zone=general burst=5 nodelay;
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_hide_header X-Powered-By;
        proxy_hide_header Server;
        limit_req_status 429;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
        proxy_send_timeout 300s;
    }

    location /create_pdf {
        limit_req zone=pdf burst=1 nodelay;
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_hide_header X-Powered-By;
        proxy_hide_header Server;
        proxy_read_timeout 600s;
        proxy_connect_timeout 75s;
        proxy_send_timeout 600s;
    }

    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF


# Enable the site
echo "🔗 Enabling Nginx site..."
sudo ln -sf "$CONFIG_PATH" /etc/nginx/sites-enabled/blockz


# Remove default site if it exists
sudo rm -f /etc/nginx/sites-enabled/default

# Remove alte gpt.gravityfight.de/blockdown-Konfiguration, falls vorhanden
if [ -e /etc/nginx/sites-enabled/gpt.gravityfight.de ]; then
    echo "🗑️ Entferne alte gpt.gravityfight.de-Konfiguration..."
    sudo rm -f /etc/nginx/sites-enabled/gpt.gravityfight.de
fi
if [ -e /etc/nginx/sites-enabled/blockdown ]; then
    echo "🗑️ Entferne alte blockdown-Konfiguration..."
    sudo rm -f /etc/nginx/sites-enabled/blockdown
fi

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
echo "🌐 Your app should now be available at: http://blockz.gravityfight.de"
echo "🔧 Docker app runs on localhost:5000 (internal)"
echo "🌍 Nginx forwards blockz.gravityfight.de zu Docker app"
echo ""
echo "🔒 Next steps:"
echo "   1. Make sure DNS A-Record für blockz.gravityfight.de auf diesen Server zeigt"
echo "   2. Test: curl -H 'Host: blockz.gravityfight.de' http://localhost"
echo "   3. Setup SSL mit: sudo certbot --nginx -d blockz.gravityfight.de"
