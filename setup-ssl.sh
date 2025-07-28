#!/bin/bash

#!/bin/bash

# SSL Setup Script for bd.gravityfight.de und blockdown.gravityfight.de
# Run this AFTER DNS is configured

set -e

echo "🔒 Setting up SSL for bd.gravityfight.de und blockdown.gravityfight.de..."

# Install Certbot if not installed
if ! command -v certbot &> /dev/null; then
    echo "📦 Installing Certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
fi

echo "🔑 Obtaining SSL certificates..."
sudo certbot --nginx -d bd.gravityfight.de -d blockdown.gravityfight.de --non-interactive --agree-tos --email admin@gravityfight.de --redirect

# Test SSL configuration
echo "🧪 Testing SSL configuration..."
sudo nginx -t

# Setup auto-renewal
echo "🔄 Setting up auto-renewal..."
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test renewal
echo "🧪 Testing SSL renewal..."
sudo certbot renew --dry-run

echo "✅ SSL setup completed!"
echo "🔒 Your app is now available at: https://bd.gravityfight.de und https://blockdown.gravityfight.de"
echo "🔄 Auto-renewal is configured"
echo "📊 Check renewal status: sudo systemctl status certbot.timer"
