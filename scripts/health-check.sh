#!/bin/bash

# Spark Code Practice - Health Check Script
# This script checks the health of Spark services

set -e

echo "🏥 Checking Spark Code Practice service health..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

# Check if services are running
echo "📊 Checking service status..."
docker-compose ps

# Check Spark Master
echo ""
echo "🔍 Checking Spark Master..."
if curl -f http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Spark Master is healthy"
else
    echo "❌ Spark Master is not accessible"
fi

# Check Jupyter Notebook
echo "🔍 Checking Jupyter Notebook..."
if curl -f http://localhost:8888 > /dev/null 2>&1; then
    echo "✅ Jupyter Notebook is healthy"
else
    echo "❌ Jupyter Notebook is not accessible"
fi

# Check MinIO
echo "🔍 Checking MinIO..."
if curl -f http://localhost:9000/minio/health/live > /dev/null 2>&1; then
    echo "✅ MinIO is healthy"
else
    echo "❌ MinIO is not accessible"
fi

# Check logs for errors
echo ""
echo "📋 Checking for errors in logs..."
ERRORS=$(docker-compose logs --tail=50 | grep -i error || true)
if [ -z "$ERRORS" ]; then
    echo "✅ No recent errors found"
else
    echo "⚠️  Recent errors found:"
    echo "$ERRORS"
fi

echo ""
echo "✅ Health check complete!"