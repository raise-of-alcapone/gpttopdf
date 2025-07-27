#!/bin/bash

# Deployment script for VPC
# Usage: ./deploy.sh

set -e

echo "🚀 Starting deployment..."

# Pull latest changes
echo "📥 Pulling latest changes from git..."
git pull origin main

# Build and restart Docker containers
echo "🔨 Building Docker image..."
docker-compose build --no-cache

echo "🔄 Restarting services..."
docker-compose down
docker-compose up -d

# Health check
echo "🏥 Performing health check..."
sleep 10
if curl -f http://localhost:5000 >/dev/null 2>&1; then
    echo "✅ Deployment successful! Service is running."
else
    echo "❌ Health check failed. Check logs with: docker-compose logs"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
