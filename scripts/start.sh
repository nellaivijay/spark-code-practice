#!/bin/bash

# Spark Code Practice - Start Script
# This script starts the Spark development environment

set -e

echo "🚀 Starting Spark Code Practice environment..."

# Start services
echo "🎬 Starting Spark services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service status:"
docker-compose ps

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📝 Access URLs:"
echo "  Jupyter Notebook:  http://localhost:8888"
echo "  Spark Master UI:   http://localhost:8080"
echo "  Spark Worker UIs:  Available from Master UI"
echo "  MinIO Console:    http://localhost:9001"
echo ""
echo "📊 To view logs, run: docker-compose logs -f"
echo "🛑 To stop services, run: ./scripts/stop.sh"