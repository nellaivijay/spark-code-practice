# Chapter 7: Production Deployment

## Overview

This lab covers deploying Apache Spark applications to production environments, including Docker, Kubernetes, and cloud platforms. Understanding production deployment is essential for taking Spark applications from development to real-world use.

### Why Production Deployment Matters

Production deployment is critical because:
- **Scalability**: Handle real workloads with proper resource allocation
- **Reliability**: Ensure applications run consistently and recover from failures
- **Security**: Implement proper authentication, authorization, and data protection
- **Monitoring**: Track application health and performance
- **Cost Optimization**: Use resources efficiently to minimize costs

### Real-World Applications

- **Data Pipelines**: Production ETL pipelines for data warehousing
- **Real-time Processing**: Streaming applications for fraud detection
- **Batch Analytics**: Daily/weekly analytical jobs
- **ML Serving**: Deploying trained models for inference
- **Data Processing**: Large-scale data transformation jobs

## Learning Objectives

By the end of this lab, you will be able to:
- Deploy Spark applications using Docker
- Deploy Spark on Kubernetes
- Configure production-ready Spark clusters
- Implement monitoring and logging
- Handle security and authentication
- Optimize for cost and performance
- Implement CI/CD for Spark applications

## Prerequisites

- Completion of previous chapters
- Understanding of Docker basics
- Basic knowledge of Kubernetes (optional)
- Docker environment running

## Estimated Time

90-120 minutes

## Lab Environment

This lab uses Docker and optional Kubernetes for deployment scenarios.

## Exercise 1: Docker Deployment

### Task

Deploy Spark applications using Docker Compose.

### Steps

1. **Review Docker Compose configuration**

```bash
# Navigate to project directory
cd spark-code-practice

# Review docker-compose.yaml
cat docker-compose.yaml
```

2. **Start the Spark cluster**

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs spark-master
```

3. **Access Spark UI**

```bash
# Spark Master UI
# Open browser: http://localhost:8080

# Spark Worker UIs
# Available from Master UI
```

4. **Submit a Spark job**

```bash
# Submit a simple job
docker-compose exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --class org.apache.spark.examples.SparkPi \
  /opt/spark/examples/jars/spark-examples_2.12-3.5.0.jar \
  10
```

5. **Monitor job execution**

```bash
# Monitor through Spark UI
# Check job status, stages, and tasks

# View logs
docker-compose logs spark-worker-1
```

### Verification

- [ ] Docker Compose starts all services
- [ ] Spark Master and Workers are running
- [ ] Spark UI is accessible
- [ ] Spark job executes successfully

## Exercise 2: Kubernetes Deployment

### Task

Deploy Spark on Kubernetes (if Kubernetes is available).

### Steps

1. **Create Kubernetes manifests**

```bash
# Create Kubernetes directory
mkdir -p k8s

# Create Spark Master deployment
cat > k8s/spark-master.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-master
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-master
  template:
    metadata:
      labels:
        app: spark-master
    spec:
      containers:
      - name: spark-master
        image: apache/spark:3.5.0
        command: ["/opt/spark/sbin/start-master.sh"]
        ports:
        - containerPort: 8080
        - containerPort: 7077
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: spark-master
spec:
  selector:
    app: spark-master
  ports:
  - port: 8080
    targetPort: 8080
    name: web-ui
  - port: 7077
    targetPort: 7077
    name: spark-port
  type: LoadBalancer
EOF
```

2. **Deploy to Kubernetes**

```bash
# Apply manifests
kubectl apply -f k8s/spark-master.yaml

# Check status
kubectl get pods
kubectl get services
```

### Verification

- [ ] Kubernetes manifests are created
- [ ] Pods are deployed successfully
- [ ] Services are accessible
- [ ] Spark job executes on Kubernetes

## Exercise 3: Configuration Management

### Task

Manage Spark configuration for production.

### Steps

1. **Create production configuration**

```bash
# Create config directory
mkdir -p config

# Create spark-defaults.conf
cat > config/spark-defaults.conf <<EOF
# Spark Configuration
spark.master                     spark://spark-master:7077
spark.app.name                   production-spark-app
spark.driver.memory              2g
spark.executor.memory            2g
spark.executor.cores             2
spark.dynamicAllocation.enabled  true
spark.dynamicAllocation.minExecutors 1
spark.dynamicAllocation.maxExecutors 4

# Performance
spark.sql.shuffle.partitions     4
spark.sql.adaptive.enabled       true
spark.serializer                 org.apache.spark.serializer.KryoSerializer

# Logging
spark.eventLog.enabled           true
spark.eventLog.dir               hdfs://namenode:9001/spark-logs
spark.history.fs.logDirectory    hdfs://namenode:9001/spark-logs

# Security
spark.authenticate              true
spark.network.crypto.enabled      true
spark.rpc.crypto.enabled         true
EOF
```

2. **Use configuration in applications**

```python
# In Python applications
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ProductionApp") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

### Verification

- [ ] Configuration files are created
- [ ] Environment-specific configs are defined
- [ ] Configuration is loaded in applications

## Exercise 4: Monitoring and Logging

### Task

Set up monitoring and logging for Spark applications.

### Steps

1. **Configure Spark logging**

```bash
# Create log4j configuration
cat > config/log4j.properties <<EOF
# Set everything to be logged to the console
log4j.rootCategory=INFO, console
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.err
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n

# Settings to quiet third-party loggers
log4j.logger.org.eclipse.jetty=WARN
log4j.logger.org.apache.spark.repl.SparkIMain$exprWatches=INFO
log4j.logger.org.apache.spark.internal.Logging=INFO
EOF
```

2. **Enable Spark History Server**

```bash
# Add to docker-compose.yaml
cat >> docker-compose.yaml <<EOF

  spark-history-server:
    image: apache/spark:3.5.0
    container_name: spark-history-server
    ports:
      - "18080:18080"
    environment:
      - SPARK_HISTORY_OPTS=-Dspark.history.fs.logDirectory=hdfs://namenode:9001/spark-logs
    volumes:
      - ./config:/opt/spark/conf
    networks:
      - spark-practice-network
    command: /opt/spark/sbin/start-history-server.sh
EOF
```

3. **Monitor using Spark UI**

```bash
# Access Spark History Server
# Open browser: http://localhost:18080

# View completed applications
# Check application metrics
# Analyze job timelines
```

### Verification

- [ ] Logging is configured
- [ ] Spark History Server is accessible
- [ ] Application metrics are visible

## Exercise 5: Security Configuration

### Task

Configure security for production Spark deployment.

### Steps

1. **Enable authentication**

```bash
# Update spark-defaults.conf
cat >> config/spark-defaults.conf <<EOF

# Authentication
spark.authenticate              true
spark.authenticate.secret      your-secret-key
spark.network.crypto.enabled   true
spark.rpc.crypto.enabled       true
EOF
```

2. **Configure network security**

```bash
# Update docker-compose.yaml with network policies
# Use Docker secrets for sensitive data
# Implement firewall rules
```

### Verification

- [ ] Authentication is enabled
- [ ] SSL/TLS is configured
- [ ] Network security is implemented

## Exercise 6: Resource Optimization

### Task

Optimize resource allocation for cost and performance.

### Steps

1. **Configure dynamic allocation**

```bash
# Add to spark-defaults.conf
cat >> config/spark-defaults.conf <<EOF

# Dynamic Allocation
spark.dynamicAllocation.enabled          true
spark.dynamicAllocation.minExecutors    1
spark.dynamicAllocation.maxExecutors    10
spark.dynamicAllocation.initialExecutors 2
spark.dynamicAllocation.executorIdleTimeout 60s
spark.dynamicAllocation.cachedExecutorIdleTimeout 120s
EOF
```

2. **Configure memory and CPU**

```bash
# Optimize memory allocation
cat >> config/spark-defaults.conf <<EOF

# Memory
spark.driver.memory                    4g
spark.driver.memoryOverhead             1g
spark.executor.memory                   4g
spark.executor.memoryOverhead           1g
spark.memory.fraction                  0.8
spark.memory.storageFraction           0.5

# CPU
spark.executor.cores                    4
spark.task.cpus                         1
EOF
```

### Verification

- [ ] Dynamic allocation is configured
- [ ] Memory and CPU are optimized
- [ ] Partitioning is implemented
- [ ] Caching is used strategically

## Exercise 7: CI/CD Pipeline

### Task

Set up CI/CD for Spark applications.

### Steps

1. **Create build script**

```bash
# Create scripts/build.sh
cat > scripts/build.sh <<EOF
#!/bin/bash

# Build Spark application
echo "Building Spark application..."

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Build package
python setup.py sdist

echo "Build complete"
EOF

chmod +x scripts/build.sh
```

2. **Create deployment script**

```bash
# Create scripts/deploy.sh
cat > scripts/deploy.sh <<EOF
#!/bin/bash

# Deploy Spark application
echo "Deploying Spark application..."

# Stop existing job
spark-submit --kill <app-id>

# Submit new job
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode cluster \
  --py-files dist/myapp-0.1.0.tar.gz \
  --name production-app \
  main.py

echo "Deployment complete"
EOF

chmod +x scripts/deploy.sh
```

3. **Create GitHub Actions workflow**

```bash
# Create .github/workflows/deploy.yml
cat > .github/workflows/deploy.yml <<EOF
name: Deploy Spark Application

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/
      
      - name: Build package
        run: |
          python setup.py sdist
      
      - name: Deploy to production
        run: |
          # Add deployment commands here
          echo "Deploying to production"
EOF
```

### Verification

- [ ] Build script works correctly
- [ ] Deployment script executes successfully
- [ ] CI/CD pipeline is configured
- [ ] Automated deployment works

## Exercise 8: Health Checks and Recovery

### Task

Implement health checks and recovery mechanisms.

### Steps

1. **Create health check script**

```bash
# Create scripts/health-check.sh
cat > scripts/health-check.sh <<EOF
#!/bin/bash

# Check Spark Master health
MASTER_URL="http://localhost:8080"

if curl -f $MASTER_URL > /dev/null 2>&1; then
    echo "Spark Master is healthy"
    exit 0
else
    echo "Spark Master is unhealthy"
    exit 1
fi
EOF

chmod +x scripts/health-check.sh
```

2. **Implement automatic recovery**

```bash
# Create scripts/recover.sh
cat > scripts/recover.sh <<EOF
#!/bin/bash

# Recover Spark cluster
echo "Recovering Spark cluster..."

# Restart services
docker-compose restart

# Verify health
./scripts/health-check.sh

echo "Recovery complete"
EOF

chmod +x scripts/recover.sh
```

### Verification

- [ ] Health check script works
- [ ] Recovery mechanism functions
- [ ] Alerts are configured

## Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes
docker-compose down -v

# Clean up
rm -rf logs/
rm -rf checkpoint/
```

## Troubleshooting

### Issue: Spark Master not starting
**Solution**: Check logs, verify port availability, check resource limits

### Issue: Workers not connecting to Master
**Solution**: Verify network configuration, check firewall rules

### Issue: Out of memory errors
**Solution**: Increase memory allocation, reduce data size, optimize queries

### Issue: Slow job execution
**Solution**: Check resource allocation, optimize code, use caching

## Expected Outcomes

By the end of this lab, you should:
- Be able to deploy Spark using Docker
- Understand Kubernetes deployment
- Configure production Spark clusters
- Implement monitoring and logging
- Configure security
- Optimize resource allocation
- Set up CI/CD pipelines
- Implement health checks and recovery

## Additional Resources

- [Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [Spark Configuration](https://spark.apache.org/docs/latest/configuration.html)
- [Spark Monitoring](https://spark.apache.org/docs/latest/monitoring.html)
- [Spark Security](https://spark.apache.org/docs/latest/security.html)

## Summary

This completes the Spark Code Practice labs. You've learned:
- Spark fundamentals and architecture
- Data loading and transformation
- Advanced DataFrame operations
- Spark SQL and optimization
- Spark streaming fundamentals
- Machine learning with MLlib
- Production deployment strategies

You're now ready to build production-ready Spark applications!