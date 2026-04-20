# Prerequisites

This guide outlines the requirements and setup steps for the Spark Code Practice repository.

## System Requirements

### Hardware
- **CPU**: 2+ cores (4+ recommended)
- **RAM**: 8GB minimum (16GB recommended for MLlib and streaming labs)
- **Disk**: 10GB free space

### Software
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Docker**: 20.10+ or Podman 3.0+
- **Python**: 3.8+ (for PySpark and scripts)
- **Java**: 11+ (optional, for Scala Spark)

## Docker Installation

### Linux
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker-compose --version
```

### macOS
```bash
# Install Docker Desktop
brew install --cask docker

# Or using Homebrew
brew install docker docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Windows (WSL2)
```bash
# Install WSL2
wsl --install

# Install Docker Desktop for Windows
# Download from https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker-compose --version
```

## Python Setup

### Install Python
```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS
brew install python3

# Windows (WSL2)
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Create Virtual Environment
```bash
cd spark-code-practice
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Java Setup (Optional)

Required only if you want to use Scala Spark or compile Spark applications.

```bash
# Linux
sudo apt install openjdk-11-jdk

# macOS
brew install openjdk@11

# Windows (WSL2)
sudo apt install openjdk-11-jdk

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

## Network Requirements

### Ports
Ensure the following ports are available:
- **8080**: Spark Master UI
- **8081**: Spark Worker UI
- **4040**: Spark Application UI (dynamic)
- **9000**: MinIO Console
- **9001**: MinIO API
- **8888**: Jupyter Notebook

### Firewall
If you have a firewall, ensure Docker containers can communicate:
```bash
# Linux (ufw)
sudo ufw allow from 172.16.0.0/12
sudo ufw allow from 192.168.0.0/16

# Or disable firewall for development (not recommended for production)
sudo ufw disable
```

## Storage Requirements

### MinIO Setup (Default)
The repository uses MinIO as an S3-compatible storage backend by default. This is automatically configured in Docker Compose.

### Local File System
You can also use local file system storage by setting:
```bash
export STORAGE_BACKEND=local
```

## Verification

### Check Docker
```bash
docker ps
docker images
```

### Check Python
```bash
python --version
pip --version
```

### Check Spark Installation
```bash
python -c "import pyspark; print(pyspark.__version__)"
```

## Troubleshooting

### Docker Issues
**Problem**: Cannot connect to Docker daemon
```bash
# Solution: Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

**Problem**: Permission denied
```bash
# Solution: Add user to docker group and relogin
sudo usermod -aG docker $USER
newgrp docker
```

### Python Issues
**Problem**: pip not found
```bash
# Solution: Install pip
sudo apt install python3-pip
# or
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### Port Conflicts
**Problem**: Port already in use
```bash
# Solution: Find and kill process using the port
sudo lsof -i :8080
sudo kill -9 <PID>

# Or change ports in docker-compose.yaml
```

### Memory Issues
**Problem**: Out of memory errors
```bash
# Solution: Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory
# Set to at least 8GB
```

## IDE Setup (Optional)

### VS Code
```bash
# Install extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-azuretools.vscode-docker
```

### PyCharm
- Install Python plugin
- Configure Python interpreter to use virtual environment
- Install Jupyter plugin

## Next Steps

Once prerequisites are installed:

1. **Clone the repository** (if not already done)
2. **Run setup script**: `./scripts/setup.sh`
3. **Start services**: `./scripts/start.sh`
4. **Open Jupyter**: Access at http://localhost:8888
5. **Begin with Lab 1**: Open `notebooks/chapter-01-spark-fundamentals.ipynb`

## Additional Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Docker Documentation](https://docs.docker.com/)
- [MinIO Documentation](https://docs.min.io/)
