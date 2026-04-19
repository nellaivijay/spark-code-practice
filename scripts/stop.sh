#!/bin/bash

# Spark Code Practice - Stop Script
# This script stops the Spark development environment

set -e

echo "🛑 Stopping Spark Code Practice environment..."

# Stop services
docker-compose down

echo "✅ Services stopped successfully!"
echo ""
echo "💡 To remove volumes and completely clean up, run: docker-compose down -v"
echo "🚀 To start services again, run: ./scripts/start.sh"