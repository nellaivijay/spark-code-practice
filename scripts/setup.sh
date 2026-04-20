#!/bin/bash

# Spark Code Practice - Setup Script
# This script sets up the development environment for Spark Code Practice

set -e

echo "🚀 Setting up Spark Code Practice environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs checkpoint notebooks solutions config/hive

# Setup sample data
echo "📊 Setting up sample data..."
python3 scripts/setup-data.py

# Copy environment example if .env doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration if needed."
else
    echo "✅ .env file already exists."
fi

# Pull Docker images
echo "🐳 Pulling Docker images..."
docker-compose pull

# Start services
echo "🎬 Starting Spark services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Access Jupyter Notebook: http://localhost:8888"
echo "  2. Access Spark Master UI: http://localhost:8080"
echo "  3. Access MinIO Console: http://localhost:9001"
echo "  4. Start working on the labs in the labs/ directory"
echo ""
echo "📚 For more information, see README.md"