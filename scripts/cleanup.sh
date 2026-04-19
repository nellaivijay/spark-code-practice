#!/bin/bash

# Spark Code Practice - Cleanup Script
# This script cleans up the Spark environment

set -e

echo "🧹 Cleaning up Spark Code Practice environment..."

# Stop services
echo "🛑 Stopping services..."
docker-compose down

# Remove volumes
echo "🗑️  Removing volumes..."
docker-compose down -v

# Clean up data directories
echo "📁 Cleaning up data directories..."
read -p "Remove data directory? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf data/*
    echo "✅ Data directory cleaned"
fi

read -p "Remove logs directory? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf logs/*
    echo "✅ Logs directory cleaned"
fi

read -p "Remove checkpoint directory? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf checkpoint/*
    echo "✅ Checkpoint directory cleaned"
fi

# Clean up Docker images
read -p "Remove Docker images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker system prune -a -f
    echo "✅ Docker images cleaned"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "💡 To set up a fresh environment, run: ./scripts/setup.sh"