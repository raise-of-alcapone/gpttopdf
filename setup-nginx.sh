#!/bin/bash

# Nginx Setup Script for GPTtoPDF with SNI
# Domain: gpt.gravityfight.de

set -e

echo "🌐 Setting up Nginx for gpt.gravityfight.de..."

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing Nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Create Nginx configuration for gpt.gravityfight.de
echo "⚙️ Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/gpt.gravityfight.de > /dev/null <<'EOF'
server {
    listen 80;
    server_name gpt.gravityfight.de;

    # Large file uploads for PDFs
    client_max_body_size 50M;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
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
sudo ln -sf /etc/nginx/sites-available/gpt.gravityfight.de /etc/nginx/sites-enabled/

# Remove default site if it exists
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
echo "🌐 Your app should now be available at: http://gpt.gravityfight.de"
echo "🔧 Docker app runs on localhost:5000 (internal)"
echo "🌍 Nginx forwards gpt.gravityfight.de to Docker app"
echo ""
echo "🔒 Next steps:"
echo "   1. Make sure DNS A-Record gpt.gravityfight.de points to this server"
echo "   2. Test: curl -H 'Host: gpt.gravityfight.de' http://localhost"
echo "   3. Setup SSL with: sudo certbot --nginx -d gpt.gravityfight.de"
