# Installation Guide

This guide will help you set up the Spark Code Practice environment on your local machine.

## Prerequisites

### Required Software

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: Minimum 10GB free space
- **CPU**: Multi-core processor recommended

## Installation Steps

### 1. Install Docker

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### macOS
```bash
brew install --cask docker
```

#### Windows
Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

### 2. Clone the Repository

```bash
git clone https://github.com/nellaivijay/spark-code-practice.git
cd spark-code-practice
```

### 3. Run Setup Script

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The setup script will:
- Create necessary directories
- Copy environment configuration
- Pull Docker images
- Start Spark services
- Display access URLs

## Manual Setup

If you prefer manual setup:

```bash
# Create directories
mkdir -p data logs checkpoint notebooks solutions config/hive

# Copy environment template
cp .env.example .env

# Start services
docker-compose up -d
```

## Verify Installation

### Check Services

```bash
docker-compose ps
```

Expected output should show:
- spark-master: Up
- spark-worker-1: Up
- spark-worker-2: Up
- jupyter: Up
- minio: Up
- postgres: Up
- hive-metastore: Up

### Access Services

- **Jupyter Notebook**: http://localhost:8888
- **Spark Master UI**: http://localhost:8080
- **MinIO Console**: http://localhost:9001

## Troubleshooting

### Docker Issues

#### Docker daemon not running
```bash
sudo systemctl start docker
sudo systemctl status docker
```

#### Permission denied
```bash
sudo usermod -aG docker $user
# Log out and log back in
```

### Port Conflicts

If ports are already in use, edit `docker-compose.yaml` to change port mappings.

### Memory Issues

If you encounter out-of-memory errors:

1. Increase Docker memory allocation in Docker Desktop settings
2. Reduce Spark memory in `.env`:
   ```
   SPARK_DRIVER_MEMORY=1g
   SPARK_EXECUTOR_MEMORY=1g
   ```

## Uninstallation

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes data)
docker-compose down -v

# Remove project directory
cd ..
rm -rf spark-code-practice
```

## Next Steps

After successful installation:

1. Read the [Quick Start](Quick-Start.md) guide
2. Start with [Chapter 1: Spark Fundamentals](../labs/chapter-01-spark-fundamentals.md)
3. Explore the Jupyter notebooks in `notebooks/` directory

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)