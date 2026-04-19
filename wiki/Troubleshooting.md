# Troubleshooting

Common issues and solutions for Spark Code Practice.

## Docker Issues

### Docker Daemon Not Running

**Symptoms**: `Cannot connect to the Docker daemon` error

**Solution**:
```bash
sudo systemctl start docker
sudo systemctl status docker
```

### Permission Denied

**Symptoms**: `permission denied` when running Docker commands

**Solution**:
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

### Out of Disk Space

**Symptoms**: `no space left on device` error

**Solution**:
```bash
docker system prune -a
docker volume prune
```

## Spark Services Issues

### Spark Master Not Starting

**Symptoms**: Spark Master container exits immediately

**Solution**:
```bash
# Check logs
docker-compose logs spark-master

# Restart the service
docker-compose restart spark-master

# Check for port conflicts
lsof -i :8080
```

### Workers Not Connecting to Master

**Symptoms**: Workers show as "dead" in Master UI

**Solution**:
```bash
# Check worker logs
docker-compose logs spark-worker-1

# Restart workers
docker-compose restart spark-worker-1 spark-worker-2
```

### Jupyter Notebook Not Accessible

**Symptoms**: Cannot access http://localhost:8888

**Solution**:
```bash
# Check if Jupyter is running
docker-compose ps jupyter

# Check Jupyter logs
docker-compose logs jupyter

# Restart Jupyter
docker-compose restart jupyter
```

## Memory Issues

### Out of Memory Errors

**Symptoms**: `java.lang.OutOfMemoryError` in Spark jobs

**Solution**:

1. Increase Docker memory allocation:
   - Docker Desktop → Settings → Resources → Memory
   - Increase to at least 8GB

2. Reduce Spark memory in `.env`:
   ```
   SPARK_DRIVER_MEMORY=1g
   SPARK_EXECUTOR_MEMORY=1g
   ```

### Container Exits with OOM

**Symptoms**: Container exits with `OOMKilled` status

**Solution**:

```bash
# Check container limits
docker-compose config

# Increase memory limits in docker-compose.yaml
mem_limit: 4g
mem_reservation: 2g
```

## Performance Issues

### Slow Job Execution

**Symptoms**: Jobs take longer than expected

**Solution**:

1. Enable adaptive query execution:
   ```python
   spark.conf.set("spark.sql.adaptive.enabled", "true")
   ```

2. Use caching for frequently used DataFrames:
   ```python
   df.cache()
   ```

3. Optimize shuffle partitions:
   ```python
   spark.conf.set("spark.sql.shuffle.partitions", "2")
   ```

### High CPU Usage

**Symptoms**: System becomes unresponsive during job execution

**Solution**:

1. Limit CPU cores in `.env`:
   ```
   SPARK_WORKER_CORES=2
   ```

2. Reduce parallelism:
   ```python
   spark.conf.set("spark.default.parallelism", 2)
   ```

## Data Issues

### File Not Found

**Symptoms**: `Path does not exist` error

**Solution**:

```bash
# Check if file exists in container
docker-compose exec spark-master ls /opt/spark/data

# Verify volume mounting
docker-compose config | grep -A 5 volumes
```

### Schema Inference Fails

**Symptoms**: Schema inference produces incorrect types

**Solution**:

```python
# Define schema explicitly
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df = spark.read.csv("data.csv", schema=schema)
```

## Network Issues

### Cannot Access Services

**Symptoms**: Cannot access Spark UI, Jupyter, or other services

**Solution**:

```bash
# Check if services are running
docker-compose ps

# Check network configuration
docker network ls
docker network inspect spark-practice-network

# Restart services
docker-compose restart
```

## Streaming Issues

### Streaming Query Not Processing Data

**Symptoms**: Streaming query runs but no data is processed

**Solution**:

```python
# Check if streaming source has data
# Ensure files are being written to the streaming directory

# Verify checkpoint directory exists
import os
os.makedirs("/opt/spark/checkpoint", exist_ok=True)
```

### Late Data Not Being Processed

**Symptoms**: Late data is dropped instead of being processed

**Solution**:

```python
# Increase watermark delay
df.withWatermark("event_time", "30 minutes")

# Use update output mode instead of append
query.writeStream.outputMode("update")
```

## Machine Learning Issues

### Model Training Fails

**Symptoms**: ML pipeline training throws errors

**Solution**:

```python
# Check data types match model expectations
df.printSchema()

# Ensure label column is numeric
from pyspark.sql.functions import col
df = df.withColumn("label", col("label").cast("double"))

# Handle missing values
df = df.na.fill(0)

# Increase max iterations
lr = LogisticRegression(maxIter=100)
```

## Getting Help

If you're still stuck:

1. Check the [Troubleshooting](Troubleshooting.md) page
2. Review the lab documentation
3. Search existing GitHub issues
4. Open a new issue with details

## Prevention Tips

### Regular Maintenance

```bash
# Clean up old logs
rm -rf logs/*

# Clean up checkpoint data
rm -rf checkpoint/*

# Clean up Docker
docker system prune -f
```

### Monitoring

```bash
# Regular health checks
./scripts/health-check.sh

# Monitor disk usage
df -h

# Monitor Docker resources
docker stats
```

### Backup

```bash
# Backup important data
cp -r data/ data_backup/
cp -r notebooks/ notebooks_backup/
```

---

**Still having issues? Open a GitHub issue with details!**