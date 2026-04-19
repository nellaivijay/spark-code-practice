<!--
SEO Metadata
Title: Apache Spark Code Practice - Free Hands-on Labs for Big Data Learning
Description: Master Apache Spark with free, hands-on labs. Practice Spark SQL, DataFrames, MLlib, streaming, and big data patterns with real-world exercises and tutorials.
Keywords: apache spark, spark code practice, spark tutorial, big data spark, spark dataframes, spark mllib, spark streaming, pyspark, scala spark
Author: Spark Code Practice Community
-->

# Apache Spark Code Practice

## 🎯 Educational Mission

A comprehensive Apache Spark learning environment designed for developers, data engineers, and data scientists who want to master modern big data processing concepts through hands-on practice with Spark.

**7 comprehensive chapters with hands-on exercises. Completely free and open source. Built for learners, by learners.**

## 🎓 Why This Repository?

This educational resource fills the gap between theoretical Spark knowledge and practical skills in big data processing:

- **🎓 Learn by Doing**: Progressive hands-on labs build real Spark skills
- **🔧 Vendor Independent**: Master Spark concepts applicable across all platforms
- **🏭 Production Patterns**: Learn best practices used in real data engineering
- **⚡ Multi-Language Experience**: Work with Python (PySpark), SQL, and Scala concepts
- **👥 Community Driven**: Built and improved by the big data community

## 🎓 Learning Approach

### Progressive Complexity

Our chapters are designed to build knowledge progressively:

- **Beginner (Chapters 1-2)**: Foundation and basic operations
- **Intermediate (Chapters 3-5)**: Advanced features and optimization
- **Advanced (Chapters 6-7)**: Machine learning and production deployment

### Hands-On Learning

Each chapter includes:
- **Clear Learning Objectives**: Know what you'll achieve
- **Step-by-Step Instructions**: Guided exercises
- **Real-World Scenarios**: Practical use cases
- **Solution Notebooks**: Reference implementations
- **Conceptual Guides**: Deep-dive explanations

### Multi-Language Experience

Gain experience with different Spark APIs:
- **PySpark**: Python API for Spark
- **Spark SQL**: SQL and DataFrame operations
- **Scala Spark**: Native Spark concepts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Apache Spark Code Practice               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Spark Core & SQL                             │  │
│  │         - Apache Spark 3.5.0                        │  │
│  │         - PySpark (Python)                          │  │
│  │         - Spark SQL (Structured Querying)           │  │
│  │         - Spark Master UI (port 8080)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Spark MLlib (Machine Learning)              │  │
│  │         - Classification & Regression             │  │
│  │         - Clustering (K-Means)                     │  │
│  │         - Pipeline API                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Spark Streaming (Real-time)                 │  │
│  │         - Structured Streaming                    │  │
│  │         - Window Operations                        │  │
│  │         - Event-time Processing                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Storage Layer (S3-Compatible)              │  │
│  │         - MinIO (Default)                          │  │
│  │         - Local File System                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Core Stack

### Spark Components
- **Apache Spark 3.5.0**: Unified analytics engine
- **Spark SQL**: Structured data processing
- **Spark MLlib**: Scalable machine learning
- **Spark Streaming**: Real-time data processing

### Storage Options
- **MinIO**: S3-compatible object storage (default)
- **Local File System**: For development and testing

### Query Engines
- **PySpark (Python)**: Python API for Spark
- **Spark SQL**: SQL interface for Spark

### Orchestration
- **Docker Compose**: Container orchestration
- **Kubernetes**: Container orchestration (optional)
- **Standalone Spark**: Simple cluster manager

## 🎓 Chapter Structure

### Chapter Difficulty & Time Estimates

| Level | Chapters | Time per Chapter | What It Tests |
|-------|----------|------------------|---------------|
| Beginner | Chapters 1-2 | 60-90 min | Basic setup, DataFrames, SQL operations |
| Intermediate | Chapters 3-5 | 90-120 min | Advanced features, optimization, streaming |
| Advanced | Chapters 6-7 | 90-120 min | Machine learning, production deployment |

### Chapter 1: Spark Fundamentals
- Spark architecture and components
- Creating and manipulating DataFrames
- Basic transformations and actions
- Understanding RDDs vs DataFrames
- Spark SQL basics

### Chapter 2: Data Loading and Transformation
- Loading data from CSV, JSON, Parquet
- Schema inference and explicit schemas
- Data cleaning and validation
- Handling missing values
- String and numeric transformations

### Chapter 3: Advanced DataFrame Operations
- Different types of joins (inner, outer, left, right, semi, anti)
- Window functions for analytics
- Complex data types (arrays, maps, structs)
- User Defined Functions (UDFs)
- Performance optimization

### Chapter 4: Spark SQL and Optimization
- Spark SQL fundamentals
- Catalyst optimizer
- Query hints for manual optimization
- Adaptive query execution
- Performance tuning strategies

### Chapter 5: Spark Streaming Fundamentals
- Structured Streaming concepts
- Streaming DataFrames
- Windowed operations
- Event-time processing
- Watermarking and late data

### Chapter 6: Machine Learning with MLlib
- Data preparation for ML
- Building ML pipelines
- Classification models
- Regression models
- Clustering algorithms
- Model evaluation

### Chapter 7: Production Deployment
- Docker deployment
- Kubernetes deployment
- Monitoring and logging
- Security configuration
- CI/CD pipelines
- Health checks and recovery

## 🚀 Quick Start

### 🎓 New to Apache Spark?

Follow our recommended learning path:

1. **Start with Fundamentals**: Read [Chapter 1](labs/chapter-01-spark-fundamentals.md)
2. **Set Up Environment**: Run `./scripts/setup.sh`
3. **Begin Learning**: Open Jupyter Notebook and start with Chapter 1
4. **Progress Through Chapters**: Follow the learning path sequentially

### 📋 Setup Options

### Option 1: Docker Compose (Recommended)
```bash
cd spark-code-practice
./scripts/setup.sh
```

### Option 2: Manual Setup
```bash
cd spark-code-practice
cp .env.example .env
docker-compose up -d
```

### Option 3: Kubernetes
```bash
cd spark-code-practice
kubectl apply -f k8s/
```

## 📋 Requirements

- Docker or Podman
- 8GB RAM minimum (16GB recommended for MLlib and streaming)
- 10GB disk space
- Python 3.8+ (for PySpark and scripts)
- Java 11+ (for Scala Spark, optional)

## 🔧 Configuration

### Spark Configuration
```bash
# Spark master URL
export SPARK_MASTER_URL=spark://localhost:7077

# Spark memory allocation
export SPARK_DRIVER_MEMORY=2g
export SPARK_EXECUTOR_MEMORY=4g

# Event logs location
export SPARK_EVENT_LOG_DIR=file:///tmp/spark-events/
```

### Storage Backend Selection
```bash
# Use MinIO (default)
export STORAGE_BACKEND=minio

# Use local file system
export STORAGE_BACKEND=local
```

## 📚 Documentation

### 🎓 Educational Resources

**Wiki Guides** (Comprehensive learning materials):
- [Wiki Home](wiki) - Main wiki page with all guides
- [Installation Guide](wiki/Installation-Guide.md) - Complete setup instructions
- [Quick Start](wiki/Quick-Start.md) - Get started in 5 minutes
- [Troubleshooting](wiki/Troubleshooting.md) - Common issues and solutions

### Core Documentation
- [README](README.md) - Project overview and quick start
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policies
- [LICENSE](LICENSE) - Apache License 2.0

### Lab Materials
- [Chapter 1: Spark Fundamentals](labs/chapter-01-spark-fundamentals.md) - RDDs, DataFrames, and transformations
- [Chapter 2: Data Loading and Transformation](labs/chapter-02-data-loading-transformation.md) - Data ingestion and preparation
- [Chapter 3: Advanced DataFrame Operations](labs/chapter-03-advanced-dataframe-operations.md) - Joins, window functions, UDFs
- [Chapter 4: Spark SQL and Optimization](labs/chapter-04-spark-sql-optimization.md) - SQL operations and performance
- [Chapter 5: Spark Streaming Fundamentals](labs/chapter-05-spark-streaming-fundamentals.md) - Real-time processing
- [Chapter 6: Machine Learning with MLlib](labs/chapter-06-machine-learning-mllib.md) - ML pipelines and models
- [Chapter 7: Production Deployment](labs/chapter-07-production-deployment.md) - Cluster setup and deployment

### 💡 Jupyter Notebooks
Interactive Jupyter notebooks for hands-on learning:

- [Chapter Notebooks](notebooks/) - Student notebooks with exercises
- [Solution Notebooks](solutions/) - Complete solution notebooks for reference

### 🔧 Automation Scripts
- [Setup Script](scripts/setup.sh) - Automated environment setup
- [Start Script](scripts/start.sh) - Start Spark services
- [Stop Script](scripts/stop.sh) - Stop Spark services
- [Health Check Script](scripts/health-check.sh) - Check service health
- [Cleanup Script](scripts/cleanup.sh) - Clean up environment
- [Job Submission Script](scripts/submit-job.sh) - Submit Spark jobs

## 🆘 Vendor Independence

This environment uses only open-source tools:
- Apache Spark (Apache 2.0)
- MinIO (Apache 2.0)
- Docker (Apache 2.0)
- Python (PSF License)
- Java (GPL)

No proprietary cloud services or consoles required.

## 🤝 Contributing

This is a practice environment for learning. Feel free to extend chapters, add examples, or improve the setup process.

> **Disclaimer**: This is an independent educational resource for learning Apache Spark and big data concepts. It is not affiliated with, endorsed by, or sponsored by Apache Spark or any vendor.

## 👥 Community and Learning

This repository is an open educational resource built for the big data community. We believe in learning together and sharing knowledge.

### 🤝 Learning Together

- **📖 Comprehensive Wiki**: Detailed guides and tutorials for all skill levels
- **💬 GitHub Discussions**: Ask questions and share insights with fellow learners
- **🐛 Issue Tracking**: Report bugs and suggest improvements
- **🔄 Pull Requests**: Contribute chapters, fixes, and enhancements
- **⭐ Star the Repo**: Show your support and help others discover this resource

### 🎓 Contributing to Learning

We welcome contributions that improve the educational value:
- **New Chapters**: Suggest new chapter topics and exercises
- **Better Explanations**: Improve clarity of existing content
- **Additional Examples**: Add more practical examples
- **Translation**: Help translate content for global learners
- **Bug Fixes**: Report and fix issues in chapters or documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### 📚 Additional Learning Resources

- **Official Apache Spark Documentation**: [https://spark.apache.org/docs/latest/](https://spark.apache.org/docs/latest/)
- **Apache Spark Slack Community**: [Join the conversation](https://apache-spark.slack.com/)
- **Spark Blog**: Latest updates and articles
- **Conference Talks**: Learn from industry experts

## 🔗 Related Practice Repositories

Continue your learning journey with these related repositories:

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
- [📚 Awesome My Notes](https://github.com/nellaivijay/awesome-my-notes) - Comprehensive technical notes and learning resources

## 📄 License

Apache License 2.0