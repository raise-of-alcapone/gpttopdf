#!/bin/bash

# Simple deployment script for debugging
# Usage: ./deploy.sh

set -e

echo "🚀 Starting deployment..."

# Pull latest changes
echo "📥 Pulling latest changes from git..."
git pull origin main

# Build and restart Docker containers
echo "🔨 Building Docker image..."
docker-compose build --no-cache gpttopdf

echo "🔄 Restarting services..."
docker-compose stop gpttopdf 2>/dev/null || true
docker-compose up -d gpttopdf

# Health check
echo "🏥 Performing health check..."
sleep 10
if curl -f http://localhost:5000 >/dev/null 2>&1; then
    echo "✅ Service is running on localhost:5000"
else
    echo "❌ Health check failed. Check logs with: docker-compose logs gpttopdf"
fi

# Status and logs for debugging
echo "📊 Service status:"
docker-compose ps gpttopdf

echo "📋 Recent logs:"
docker-compose logs --tail=20 gpttopdf

echo "✅ Deployment completed!"
echo "🐛 For debugging: docker-compose logs -f gpttopdf"
echo "🧪 Test PDF generation: curl http://localhost:5000/debug/test-pdf -o test.pdf"
