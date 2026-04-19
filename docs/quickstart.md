---
title: Quick Start
description: Get started with Spark Code Practice in 5 minutes
---

# Quick Start

Get started with Spark Code Practice in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

- Docker installed
- Docker Compose installed
- At least 8GB RAM available
- 10GB free disk space

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/nellaivijay/spark-code-practice.git
cd spark-code-practice
./scripts/setup.sh
```

That's it! The setup script will:
- Download and configure Docker images
- Start all Spark services
- Create necessary directories
- Display access URLs

### 2. Access Services

Once setup is complete, you can access:

- **Jupyter Notebook**: http://localhost:8888
- **Spark Master UI**: http://localhost:8080
- **MinIO Console**: http://localhost:9001

### 3. Start Learning

Open Jupyter Notebook and navigate to the `notebooks/` directory. Start with:

```
notebooks/chapter-01-spark-fundamentals.ipynb
```

## Your First Spark Program

### In Jupyter Notebook

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("HelloSpark") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Create a simple DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])

# Display the DataFrame
df.show()

# Stop Spark session
spark.stop()
```

## Common Commands

### Start/Stop Services

```bash
# Start services
./scripts/start.sh

# Stop services
./scripts/stop.sh

# Check service health
./scripts/health-check.sh
```

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs spark-master

# Follow logs in real-time
docker-compose logs -f spark-master
```

## Lab Structure

| Chapter | Topic | Duration |
|---------|-------|----------|
| 1 | Spark Fundamentals | 60-90 min |
| 2 | Data Loading and Transformation | 90-120 min |
| 3 | Advanced DataFrame Operations | 90-120 min |
| 4 | Spark SQL and Optimization | 90-120 min |
| 5 | Spark Streaming Fundamentals | 90-120 min |
| 6 | Machine Learning with MLlib | 90-120 min |
| 7 | Production Deployment | 90-120 min |

## Learning Path

### For Beginners

1. Start with Chapter 1: Spark Fundamentals
2. Complete Chapter 2: Data Loading and Transformation
3. Learn Spark SQL in Chapter 4

### For Intermediate Users

1. Complete beginner chapters
2. Learn advanced operations in Chapter 3
3. Explore streaming in Chapter 5

### For Advanced Users

1. Complete all previous chapters
2. Build ML pipelines in Chapter 6
3. Deploy to production in Chapter 7

## Tips for Success

### 1. Understand the Concepts

Before running code, read the explanations in the lab markdown files.

### 2. Experiment

Don't just copy the code. Try modifying it:
- Change the data
- Add new transformations
- Experiment with different parameters

### 3. Use the Spark UI

Monitor your jobs using the Spark Master UI:
- Check job progress
- View execution plans
- Identify bottlenecks

### 4. Take Notes

Document what you learn:
- Write down concepts you find challenging
- Note solutions to problems you encounter
- Keep track of useful code snippets

## Next Steps

1. Complete the [Installation Guide](installation.md) if you haven't already
2. Start with [Chapter 1: Spark Fundamentals](../labs/chapter-01-spark-fundamentals.md)
3. Explore the [Lab Descriptions](labs.md) for detailed information

## Resources

- [Official Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)