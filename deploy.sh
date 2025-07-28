#!/bin/bash

# Smart deployment script with caching
# Usage: ./deploy.sh [--force-rebuild]

set -e

echo "🚀 Starting deployment..."

# Note: Run 'git pull origin main' manually before this script
echo "ℹ️  Make sure you have pulled latest changes with: git pull origin main"

# Check if force rebuild is requested
FORCE_REBUILD=false
if [[ "$1" == "--force-rebuild" ]]; then
    FORCE_REBUILD=true
    echo "🔨 Force rebuild requested"
fi

# Smart build strategy
if [[ "$FORCE_REBUILD" == "true" ]]; then
    echo "🔨 Building Docker image (no cache)..."
    docker-compose build --no-cache gpttopdf
else
    # Check what changed
    echo "� Checking for changes..."
    
    # Check if Dockerfile or requirements.txt changed (need rebuild)
    if git diff HEAD~1 --name-only 2>/dev/null | grep -E "(Dockerfile|requirements\.txt)" > /dev/null; then
        echo "🔨 Dockerfile or requirements changed - rebuilding without cache..."
        docker-compose build --no-cache gpttopdf
    else
        echo "⚡ Only code changes detected - using cache..."
        docker-compose build gpttopdf
    fi
fi

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
echo "🌐 App running at: http://localhost:5000"
echo "🔗 Public URL: https://blockz.gravityfight.de (after DNS + SSL setup)"
echo ""
echo "🐛 For debugging: docker-compose logs -f gpttopdf"
echo "🧪 Test PDF generation: curl http://localhost:5000/debug/test-pdf -o test.pdf"
echo ""
echo "💡 Usage tips:"
echo "   ./deploy.sh                 # Smart caching (fast for code changes)"
echo "   ./deploy.sh --force-rebuild # Full rebuild (slow, for major changes)"
