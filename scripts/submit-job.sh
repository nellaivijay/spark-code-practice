#!/bin/bash

# Spark Code Practice - Job Submission Script
# This script submits Spark jobs to the cluster

set -e

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Spark services are not running. Start them with ./scripts/start.sh"
    exit 1
fi

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: ./scripts/submit-job.sh <job-script> [args]"
    echo ""
    echo "Example:"
    echo "  ./scripts/submit-job.sh notebooks/example.py"
    echo "  ./scripts/submit-job.sh notebooks/example.py --arg1 value1"
    exit 1
fi

JOB_SCRIPT=$1
shift
JOB_ARGS="$@"

echo "🚀 Submitting Spark job: $JOB_SCRIPT"
echo "📝 Arguments: $JOB_ARGS"

# Submit job
docker-compose exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    $JOB_SCRIPT $JOB_ARGS

echo ""
echo "✅ Job submission complete!"
echo "📊 Check Spark Master UI at http://localhost:8080 for job status"