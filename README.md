# Apache Spark Code Practice

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5%2B-orange)](https://spark.apache.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)](https://jupyter.org/)

7 hands-on labs for mastering Apache Spark through progressive, practical exercises. From fundamentals to production deployment.

![Lab Progression](assets/diagrams/lab-progression.mmd)

## Labs

| # | Lab | Difficulty | Time | Topics |
|---|-----|------------|------|--------|
| 01 | [Spark Fundamentals](labs/chapter-01-spark-fundamentals.md) | Beginner | 60-90 min | Architecture, DataFrames, basic operations |
| 02 | [Data Loading & Transformation](labs/chapter-02-data-loading-transformation.md) | Beginner | 60-90 min | Data ingestion, cleaning, validation |
| 03 | [Advanced DataFrame Operations](labs/chapter-03-advanced-dataframe-operations.md) | Intermediate | 90-120 min | Joins, window functions, UDFs, complex types |
| 04 | [Spark SQL & Optimization](labs/chapter-04-spark-sql-optimization.md) | Intermediate | 90-120 min | SQL operations, Catalyst optimizer, performance tuning |
| 05 | [Spark Streaming Fundamentals](labs/chapter-05-spark-streaming-fundamentals.md) | Intermediate | 90-120 min | Structured streaming, windowed operations, watermarking |
| 06 | [Machine Learning with MLlib](labs/chapter-06-machine-learning-mllib.md) | Advanced | 90-120 min | ML pipelines, classification, regression, clustering |
| 07 | [Production Deployment](labs/chapter-07-production-deployment.md) | Advanced | 90-120 min | Docker, Kubernetes, monitoring, CI/CD |

**Total: ~9.5-13 hours**

## Domain Coverage

![Domain Coverage](assets/diagrams/domain-coverage.mmd)

| Domain | Coverage | Labs |
|--------|----------|------|
| Spark Architecture | 15% | Lab 1, Lab 7 |
| DataFrame API | 30% | Lab 1, Lab 2, Lab 3 |
| Spark SQL | 20% | Lab 4 |
| Data Loading | 10% | Lab 2 |
| Streaming | 10% | Lab 5 |
| MLlib | 10% | Lab 6 |
| Production | 5% | Lab 7 |

## Getting Started

### 1. Check Prerequisites
Review [prerequisites.md](prerequisites.md) and ensure you have:
- Docker or Podman installed
- Python 3.8+ 
- 8GB RAM minimum (16GB recommended)
- 10GB disk space

### 2. Setup Environment
```bash
# Clone repository (if not already done)
git clone https://github.com/nellaivijay/spark-code-practice.git
cd spark-code-practice

# Run setup script
./scripts/setup.sh
```

### 3. Start Services
```bash
./scripts/start.sh
```

### 4. Access Jupyter Notebook
Open your browser and go to: http://localhost:8888

### 5. Begin Learning
Start with [Lab 1: Spark Fundamentals](notebooks/chapter-01-spark-fundamentals.ipynb)

## Lab Progression

Labs are designed to be completed in order:

- **Labs 1-2 (Foundation)**: Architecture, data I/O, basic operations
- **Labs 3-5 (Core Skills)**: Advanced DataFrame operations, SQL optimization, streaming
- **Labs 6-7 (Advanced)**: Machine learning with MLlib, production deployment

## Supporting Materials

### Cheatsheets
Quick reference notebooks for key concepts:
- [DataFrame API Cheatsheet](cheatsheets/dataframe-api-cheatsheet.ipynb)
- [Spark SQL Cheatsheet](cheatsheets/spark-sql-cheatsheet.ipynb)
- [Streaming & Performance Cheatsheet](cheatsheets/streaming-performance-cheatsheet.ipynb)

### Documentation
- [Prerequisites](prerequisites.md) - Setup requirements and installation guide
- [Installation Guide](wiki/Installation-Guide.md) - Detailed setup instructions
- [Quick Start](wiki/Quick-Start.md) - Get started in 5 minutes
- [Troubleshooting](wiki/Troubleshooting.md) - Common issues and solutions

## Architecture

![Architecture Overview](assets/diagrams/architecture-overview.mmd)

### Components
- **Jupyter Notebook**: Interactive learning environment
- **PySpark**: Python API for Spark
- **Spark SQL**: SQL interface for structured queries
- **Spark MLlib**: Machine learning library
- **Spark Streaming**: Real-time data processing
- **MinIO**: S3-compatible object storage
- **Docker Compose**: Container orchestration

## Target Audience

Developers, data engineers, and data scientists who want to:
- Learn Apache Spark from fundamentals to advanced concepts
- Gain hands-on experience with real-world data processing
- Understand Spark architecture and optimization techniques
- Build production-ready Spark applications

## Requirements

- Docker or Podman
- 8GB RAM minimum (16GB recommended for MLlib and streaming)
- 10GB disk space
- Python 3.8+ (for PySpark and scripts)
- Java 11+ (optional, for Scala Spark)

## Cleanup

When done, clean up the environment:

```bash
# Stop services
./scripts/stop.sh

# Full cleanup (removes data, logs, volumes)
./scripts/cleanup.sh
```

## License

Apache License 2.0

## Related Practice Repositories

Continue your learning journey:

### AI/ML Practice
- [🤖 DSPy Code Practice](https://github.com/nellaivijay/dspy-code-practice) - Declarative LLM programming
- [🧠 LLM Fine-Tuning Practice](https://github.com/nellaivijay/llm-fine-tuning-practice) - Model fine-tuning techniques

### Data Engineering Practice
- [🦆 DuckDB Code Practice](https://github.com/nellaivijay/duckdb-code-practice) - Analytics & SQL optimization
- [🏔️ Apache Iceberg Code Practice](https://github.com/nellaivijay/iceberg-code-practice) - Lakehouse architecture
- [🔧 Apache Beam Code Practice](https://github.com/nellaivijay/beam-code-practice) - Data pipelines

### Programming Practice
- [⚙️ Scala Data Analysis Practice](https://github.com/nellaivijay/scala-dataanalysis-code-practice) - Functional programming

### Resource Hub
- [📚 Awesome My Notes](https://github.com/nellaivijay/awesome-my-notes) - Comprehensive technical notes
