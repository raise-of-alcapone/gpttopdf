#!/bin/bash

# Setup Docker BuildKit for better caching
echo "🔧 Setting up Docker BuildKit for better caching..."

# Enable BuildKit globally
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bashrc

# Activate for current session
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

echo "✅ BuildKit enabled!"
echo "🔄 Please run: source ~/.bashrc"
echo "📊 Or restart your shell session"
