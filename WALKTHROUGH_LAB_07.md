# Lab 7: Production Deployment - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 7: Production Deployment.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Spark environment set up (run `./scripts/setup.sh`)
- Jupyter Notebook accessible at http://localhost:8888
- Completion of Lab 1: Spark Fundamentals
- Completion of Lab 2: Data Loading & Transformation
- Completion of Lab 4: Spark SQL & Optimization
- Basic understanding of containerization and orchestration

## Setup Instructions

### 1. Start the Environment
```bash
cd spark-code-practice
./scripts/start.sh
```

### 2. Open Jupyter Notebook
- Navigate to http://localhost:8888 in your browser
- Open `notebooks/chapter-07-production-deployment.ipynb`

## Lab Walkthrough

### Section A: Docker Deployment

#### Step 1: Import Required Libraries
```python
from pyspark.sql import SparkSession
import os
import subprocess
```

**Explanation**: Import libraries for Spark operations and system commands for deployment tasks.

#### Step 2: Create SparkSession with Production Configurations
```python
spark = SparkSession.builder \
    .appName("ProductionDeployment") \
    .master("spark://spark-master:7077") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.dynamicAllocation.enabled", "true") \
    .config("spark.dynamicAllocation.minExecutors", "1") \
    .config("spark.dynamicAllocation.maxExecutors", "10") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.io.compression.codec", "snappy") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print(f"Spark master: {spark.conf.get('spark.master')}")
print(f"Dynamic allocation: {spark.conf.get('spark.dynamicAllocation.enabled')}")
```

**Key Concepts**:
- **Dynamic Allocation**: Automatically scales executors based on workload
- **Kryo Serializer**: Faster serialization for better performance
- **Snappy Compression**: Efficient compression for shuffle operations
- **Increased Partitions**: Better parallelism for large datasets

**Expected Output**: 
```
Spark version: 3.5.0
Spark master: spark://spark-master:7077
Dynamic allocation: true
```

#### Step 3: Create Dockerfile
```python
# Example Dockerfile for Spark application
dockerfile_content = '''
# Multi-stage build for optimized image size
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y gcc openjdk-11-jdk

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

# Install Java runtime
RUN apt-get update && apt-get install -y openjdk-11-jre && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
COPY . /app
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV SPARK_HOME=/opt/spark

# Run the application
CMD ["python", "main.py"]
'''

print("Dockerfile example created:")
print(dockerfile_content)
```

**Key Concept**: Multi-stage builds reduce image size by separating build and runtime dependencies.

**Practice**: Save this Dockerfile and build an image with `docker build -t my-spark-app .`

#### Step 4: Create Docker Compose Configuration
```python
# Example docker-compose.yml for Spark cluster
docker_compose_content = '''
version: '3.8'

services:
  spark-master:
    image: bitnami/spark:3.5.0
    container_name: spark-master
    ports:
      - "8080:8080"  # Spark Master UI
      - "7077:7077"  # Spark Master port
    environment:
      - SPARK_MODE=master
      - SPARK_MASTER_HOST=spark-master
      - SPARK_MASTER_PORT=7077
    volumes:
      - ./data:/opt/spark/data
      - ./logs:/opt/spark/logs
    networks:
      - spark-network

  spark-worker:
    image: bitnami/spark:3.5.0
    container_name: spark-worker
    depends_on:
      - spark-master
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_HOST=spark-master
      - SPARK_MASTER_PORT=7077
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_MEMORY=4g
    volumes:
      - ./data:/opt/spark/data
      - ./logs:/opt/spark/logs
    networks:
      - spark-network

  spark-submit:
    build: .
    container_name: spark-submit
    depends_on:
      - spark-master
      - spark-worker
    environment:
      - SPARK_MASTER=spark://spark-master:7077
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - spark-network

networks:
  spark-network:
    driver: bridge
'''

print("docker-compose.yml example created:")
print(docker_compose_content)
```

**Key Concept**: Docker Compose orchestrates multi-container applications, defining services, networks, and volumes.

**Practice**: Save this configuration and run with `docker-compose up -d`

### Section B: Kubernetes Deployment

#### Step 5: Create Kubernetes Deployment
```python
# Example Kubernetes deployment for Spark application
k8s_deployment = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: spark-app
  template:
    metadata:
      labels:
        app: spark-app
    spec:
      containers:
      - name: spark-app
        image: my-spark-app:latest
        ports:
          - containerPort: 4040
        env:
          - name: SPARK_MASTER
            value: "k8s://https://kubernetes.default.svc:443"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
          - name: data
            mountPath: /data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: spark-data-pvc
'''

print("Kubernetes deployment example created:")
print(k8s_deployment)
```

**Key Concept**: Kubernetes provides container orchestration with automatic scaling, self-healing, and rolling updates.

**Practice**: Deploy to Kubernetes with `kubectl apply -f deployment.yaml`

#### Step 6: Create ConfigMap for Configuration
```python
# Example ConfigMap for Spark configuration
configmap_content = '''
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-config
data:
  spark-defaults.conf: |
    spark.driver.memory=2g
    spark.executor.memory=4g
    spark.executor.cores=2
    spark.sql.shuffle.partitions=200
    spark.dynamicAllocation.enabled=true
    spark.dynamicAllocation.minExecutors=1
    spark.dynamicAllocation.maxExecutors=10
    spark.serializer=org.apache.spark.serializer.KryoSerializer
    spark.io.compression.codec=snappy
'''

print("ConfigMap example created:")
print(configmap_content)
```

**Key Concept**: ConfigMaps decouple configuration from container images, enabling configuration changes without rebuilding.

### Section C: Monitoring and Logging

#### Step 7: Configure Prometheus
```python
# Example Prometheus configuration for Spark metrics
prometheus_config = '''
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'spark-master'
    static_configs:
      - targets: ['spark-master:8080']
    metrics_path: /metrics/prometheus/
    scrape_interval: 10s

  - job_name: 'spark-workers'
    static_configs:
      - targets: ['spark-worker-1:8081', 'spark-worker-2:8081']
    metrics_path: /metrics/prometheus/
    scrape_interval: 10s

  - job_name: 'spark-applications'
    static_configs:
      - targets: ['spark-submit:4040']
    metrics_path: /metrics/prometheus/
    scrape_interval: 10s
'''

print("Prometheus configuration example created:")
print(prometheus_config)
```

**Key Concept**: Prometheus collects and stores metrics from Spark applications for monitoring and alerting.

**Practice**: Enable Spark metrics with `spark.metrics.conf` configuration.

#### Step 8: Configure Grafana Dashboard
```python
# Example Grafana dashboard configuration
grafana_dashboard = '''
{
  "dashboard": {
    "title": "Spark Cluster Monitoring",
    "panels": [
      {
        "title": "Executor Memory Usage",
        "targets": [
          {
            "expr": "spark_executor_memory_used_bytes",
            "legendFormat": "{{executor}}"
          }
        ]
      },
      {
        "title": "Task Duration",
        "targets": [
          {
            "expr": "spark_task_duration_milliseconds",
            "legendFormat": "{{stage}}"
          }
        ]
      },
      {
        "title": "Shuffle Read/Write",
        "targets": [
          {
            "expr": "spark_shuffle_read_bytes_total",
            "legendFormat": "{{stage}}"
          }
        ]
      }
    ]
  }
}
'''

print("Grafana dashboard example created:")
print(grafana_dashboard)
```

**Key Concept**: Grafana visualizes Prometheus metrics, providing dashboards for monitoring Spark cluster health and performance.

### Section D: CI/CD Pipeline

#### Step 9: Create GitHub Actions Workflow
```python
# Example GitHub Actions workflow
github_actions = '''
name: Build and Deploy Spark Application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest

    - name: Run tests
      run: pytest tests/

    - name: Build Docker image
      run: |
        docker build -t my-spark-app:${{ github.sha }} .
        docker tag my-spark-app:${{ github.sha }} my-spark-app:latest

    - name: Login to Docker Hub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Push Docker image
      run: |
        docker push my-spark-app:${{ github.sha }}
        docker push my-spark-app:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      KUBECONFIG: ${{ secrets.KUBE_CONFIG }}

    steps:
    - uses: actions/checkout@v2

    - name: Set up kubectl
      uses: azure/setup-kubectl@v1

    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/deployment.yaml
        kubectl apply -f k8s/service.yaml
        kubectl rollout status deployment/spark-app

    - name: Run smoke tests
      run: |
        kubectl exec -it deployment/spark-app -- python /app/tests/smoke_test.py
'''

print("GitHub Actions workflow example created:")
print(github_actions)
```

**Key Concept**: CI/CD pipelines automate build, test, and deployment processes, ensuring consistent and reliable releases.

**Practice**: Create `.github/workflows/deploy.yml` with this configuration.

### Section E: Security Best Practices

#### Step 10: Create Kubernetes Secret
```python
# Example Kubernetes Secret for sensitive data
k8s_secret = '''
apiVersion: v1
kind: Secret
metadata:
  name: spark-secrets
type: Opaque
stringData:
  database-url: "jdbc:postgresql://db.example.com:5432/sparkdb"
  database-user: "spark_user"
  database-password: "secure_password"
  aws-access-key: "AKIAIOSFODNN7EXAMPLE"
  aws-secret-key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
'''

print("Kubernetes Secret example created:")
print(k8s_secret)
```

**Key Concept**: Secrets securely store sensitive information like passwords, API keys, and tokens.

**Practice**: Create secrets with `kubectl apply -f secret.yaml` and reference in deployments.

#### Step 11: Implement Network Policies
```python
# Example Network Policy for Spark cluster
network_policy = '''
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: spark-network-policy
spec:
  podSelector:
    matchLabels:
      app: spark-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: spark-master
    ports:
    - protocol: TCP
      port: 7077
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: spark-master
    ports:
    - protocol: TCP
      port: 7077
'''

print("Network Policy example created:")
print(network_policy)
```

**Key Concept**: Network policies control traffic flow between pods, enhancing security through network segmentation.

### Section F: High Availability

#### Step 12: Configure Standby Masters
```python
# Example Spark configuration for high availability
ha_config = '''
spark.deploy.recoveryMode=ZOOKEEPER
spark.deploy.zookeeper.url=zk1:2181,zk2:2181,zk3:2181
spark.deploy.zookeeper.dir=/spark-ha
'''

print("High availability configuration example:")
print(ha_config)
```

**Key Concept**: Standby masters with ZooKeeper provide automatic failover in case of master node failure.

#### Step 13: Configure Resource Requests and Limits
```python
# Example resource configuration for production
resource_config = '''
# Driver resources
spark.driver.memory=4g
spark.driver.cores=2

# Executor resources
spark.executor.memory=8g
spark.executor.cores=4

# Dynamic allocation
spark.dynamicAllocation.enabled=true
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=20
spark.dynamicAllocation.initialExecutors=4

# Shuffle service
spark.shuffle.service.enabled=true
'''

print("Resource configuration example:")
print(resource_config)
```

**Key Concept**: Proper resource allocation ensures stable performance and prevents resource starvation.

### Section G: Performance Optimization

#### Step 14: Configure Performance Tuning
```python
# Example performance tuning configuration
performance_config = '''
# Serialization
spark.serializer=org.apache.spark.serializer.KryoSerializer
spark.kryoserializer.buffer.max=512m

# Compression
spark.io.compression.codec=snappy
spark.rdd.compress=true

# Memory management
spark.memory.fraction=0.6
spark.memory.storageFraction=0.5

# Shuffle optimization
spark.shuffle.compress=true
spark.shuffle.spill.compress=true
spark.sql.shuffle.partitions=200

# AQE
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.adaptive.skewJoin.enabled=true
'''

print("Performance tuning configuration example:")
print(performance_config)
```

**Key Concept**: Performance tuning configurations optimize Spark for specific workloads and cluster characteristics.

## Troubleshooting Tips

### Issue: Container Startup Failures
**Solution**:
- Check container logs with `docker logs` or `kubectl logs`
- Verify environment variables and configuration
- Ensure all dependencies are installed
- Check resource limits and requests

### Issue: Kubernetes Deployment Not Scaling
**Solution**:
- Verify Horizontal Pod Autoscaler configuration
- Check resource metrics are being collected
- Ensure resource requests and limits are set correctly
- Verify cluster has sufficient resources

### Issue: Monitoring Data Not Appearing
**Solution**:
- Verify Prometheus scrape configuration
- Check Spark metrics are enabled
- Ensure network policies allow metrics access
- Verify Grafana dashboard queries

### Issue: CI/CD Pipeline Failures
**Solution**:
- Check GitHub Actions logs for specific errors
- Verify secrets are properly configured
- Ensure Docker Hub authentication works
- Test deployment steps locally first

### Issue: Performance Degradation in Production
**Solution**:
- Monitor resource utilization in Grafana
- Check for data skew in shuffle operations
- Verify AQE is working correctly
- Review and tune Spark configurations
- Consider increasing cluster resources

## Check Your Understanding

1. What are the benefits of using multi-stage Docker builds?
2. How does Kubernetes provide high availability for Spark applications?
3. What is the purpose of ConfigMaps and Secrets in Kubernetes?
4. How does Prometheus and Grafana enable monitoring of Spark applications?
5. What are the key components of a CI/CD pipeline for Spark applications?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-07-production-deployment-solution.ipynb`
4. Review all completed labs to prepare for the Databricks Spark Associate certification

## Additional Resources

- [Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Spark Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)
