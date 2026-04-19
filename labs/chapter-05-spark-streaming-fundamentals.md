# Chapter 5: Spark Streaming Fundamentals

## Overview

This lab introduces Apache Spark Structured Streaming, a scalable and fault-tolerant stream processing engine built on Spark SQL. Understanding streaming fundamentals is essential for building real-time data pipelines and processing continuous data streams.

### Why Spark Streaming Matters

Spark Structured Streaming is crucial because:
- **Real-time Processing**: Process data as it arrives, enabling real-time analytics
- **Unified API**: Uses the same DataFrame/Dataset API as batch processing
- **Fault Tolerance**: Exactly-once processing guarantees with checkpointing
- **Scalability**: Handles millions of events per second across clusters
- **Integration**: Works seamlessly with various data sources and sinks

### Real-World Applications

- **Real-time Analytics**: Live dashboards and monitoring
- **Fraud Detection**: Identifying suspicious transactions in real-time
- **IoT Processing**: Processing sensor data from connected devices
- **Log Analysis**: Real-time log monitoring and alerting
- **Social Media**: Analyzing social media streams for trends

## Learning Objectives

By the end of this lab, you will be able to:
- Understand Spark Structured Streaming concepts
- Create streaming DataFrames from various sources
- Apply transformations to streaming data
- Write streaming data to various sinks
- Handle event-time and watermarking
- Implement windowed operations
- Monitor and debug streaming queries

## Prerequisites

- Completion of Chapter 1: Spark Fundamentals
- Understanding of Spark DataFrames
- Basic knowledge of streaming concepts
- Docker environment running

## Estimated Time

90-120 minutes

## Lab Environment

This lab uses the same Docker-based Spark environment with additional streaming capabilities.

## Setup

```bash
# Ensure Docker environment is running
docker-compose up -d

# Access Jupyter Notebook
# Navigate to http://localhost:8888
```

Initialize Spark session:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when, count, sum, avg, window, current_timestamp, expr
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("SparkStreamingFundamentals") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.streaming.checkpointLocation", "/opt/spark/checkpoint") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

## Exercise 1: Basic Streaming Concepts

### Task

Understand the fundamental concepts of Structured Streaming.

### Steps

1. **Streaming vs Batch Processing**

```python
# Batch processing (static data)
batch_data = [
    ("Alice", 100, "2023-01-01 10:00:00"),
    ("Bob", 200, "2023-01-01 10:01:00"),
    ("Charlie", 150, "2023-01-01 10:02:00")
]

batch_schema = StructType([
    StructField("name", StringType(), True),
    StructField("amount", IntegerType(), True),
    StructField("timestamp", StringType(), True)
])

df_batch = spark.createDataFrame(batch_data, batch_schema)
df_batch.show()
```

2. **Streaming Processing Model**

```python
# Understand the streaming model:
# - Input: Unbounded data stream
# - Processing: Continuous queries on the stream
# - Output: Incremental results
```

3. **Output Modes**

```python
# Output modes in Structured Streaming:
# - Append: Only new rows added to the result table
# - Complete: Entire result table updated on each trigger
# - Update: Only rows that changed since last trigger
```

### Verification

- [ ] You understand the difference between batch and streaming
- [ ] You understand the streaming processing model
- [ ] You know the different output modes

## Exercise 2: Creating a Streaming Source

### Task

Create a streaming DataFrame from a file source.

### Steps

1. **Create a directory for streaming data**

```python
import os

# Create directory for streaming data
streaming_dir = "/opt/spark/data/streaming"
os.makedirs(streaming_dir, exist_ok=True)
```

2. **Write initial data**

```python
# Write initial batch of data
initial_data = """name,amount,timestamp
Alice,100,2023-01-01 10:00:00
Bob,200,2023-01-01 10:01:00"""

with open(f"{streaming_dir}/batch1.csv", "w") as f:
    f.write(initial_data)
```

3. **Create streaming DataFrame**

```python
# Read streaming data from directory
streaming_schema = StructType([
    StructField("name", StringType(), True),
    StructField("amount", IntegerType(), True),
    StructField("timestamp", StringType(), True)
])

df_streaming = spark.readStream \
    .schema(streaming_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

# Is this a streaming DataFrame?
print(f"Is streaming: {df_streaming.isStreaming}")
```

4. **Query the streaming DataFrame**

```python
# Simple aggregation on streaming data
df_counts = df_streaming.groupBy("name").count()

# Start the streaming query
query = df_counts.writeStream \
    .outputMode("complete") \
    .format("memory") \
    .queryName("streaming_counts") \
    .start()

# Wait for some data to be processed
import time
time.sleep(5)

# Query the in-memory table
result = spark.sql("SELECT * FROM streaming_counts")
result.show()

# Stop the query
query.stop()
```

### Verification

- [ ] Streaming directory is created
- [ ] Initial data is written
- [ ] Streaming DataFrame is created successfully
- [ ] Streaming query executes and produces results

## Exercise 3: Streaming Transformations

### Task

Apply transformations to streaming data.

### Steps

1. **Add more streaming data**

```python
# Write second batch
second_batch = """name,amount,timestamp
Charlie,150,2023-01-01 10:02:00
Diana,300,2023-01-01 10:03:00
Eve,250,2023-01-01 10:04:00"""

with open(f"{streaming_dir}/batch2.csv", "w") as f:
    f.write(second_batch)
```

2. **Apply transformations**

```python
# Read streaming data
df_streaming = spark.readStream \
    .schema(streaming_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

# Apply transformations
from pyspark.sql.functions import upper, col

df_transformed = df_streaming.select(
    upper(col("name")).alias("name_upper"),
    col("amount"),
    col("timestamp")
).filter(col("amount") > 100)

# Start query
query = df_transformed.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("streaming_transformed") \
    .start()

# Wait for processing
time.sleep(5)

# Check results
result = spark.sql("SELECT * FROM streaming_transformed")
result.show()

# Stop query
query.stop()
```

### Verification

- [ ] Additional streaming data is processed
- [ ] Transformations work correctly on streaming data
- [ ] Complex aggregations produce expected results

## Exercise 4: Windowed Operations

### Task

Perform windowed aggregations on streaming data.

### Steps

1. **Create data with timestamps**

```python
# Write data with proper timestamps
windowed_data = """name,amount,timestamp
Alice,100,2023-01-01 10:00:00
Bob,200,2023-01-01 10:01:00
Charlie,150,2023-01-01 10:02:00
Diana,300,2023-01-01 10:05:00
Eve,250,2023-01-01 10:06:00"""

with open(f"{streaming_dir}/windowed_batch1.csv", "w") as f:
    f.write(windowed_data)
```

2. **Tumbling window aggregation**

```python
# Read streaming data
df_streaming = spark.readStream \
    .schema(streaming_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

# Convert timestamp to timestamp type
from pyspark.sql.functions import to_timestamp

df_with_timestamp = df_streaming.withColumn(
    "event_time",
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

# Tumbling window (5-minute windows)
df_tumbling = df_with_timestamp.groupBy(
    window(col("event_time"), "5 minutes")
).agg(
    count("*").alias("count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount")
)

# Start query
query = df_tumbling.writeStream \
    .outputMode("complete") \
    .format("memory") \
    .queryName("streaming_tumbling") \
    .start()

# Wait for processing
time.sleep(10)

# Check results
result = spark.sql("SELECT * FROM streaming_tumbling ORDER BY window")
result.show(truncate=False)

# Stop query
query.stop()
```

### Verification

- [ ] Tumbling window aggregation works correctly
- [ ] Sliding window aggregation produces expected overlapping windows
- [ ] Window boundaries are calculated correctly

## Exercise 5: Watermarking and Late Data

### Task

Handle late data using watermarking.

### Steps

1. **Create data with event time**

```python
# Write data with event times
watermark_data = """name,amount,timestamp
Alice,100,2023-01-01 10:00:00
Bob,200,2023-01-01 10:01:00
Charlie,150,2023-01-01 10:02:00"""

with open(f"{streaming_dir}/watermark_batch1.csv", "w") as f:
    f.write(watermark_data)
```

2. **Apply watermark**

```python
# Read streaming data
df_streaming = spark.readStream \
    .schema(streaming_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

# Convert timestamp
df_with_timestamp = df_streaming.withColumn(
    "event_time",
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

# Apply watermark (10 minutes)
df_watermarked = df_with_timestamp.withWatermark("event_time", "10 minutes")

# Windowed aggregation with watermark
df_window_watermarked = df_watermarked.groupBy(
    window(col("event_time"), "5 minutes")
).agg(
    count("*").alias("count"),
    sum("amount").alias("total_amount")
)

# Start query
query = df_window_watermarked.writeStream \
    .outputMode("update") \
    .format("memory") \
    .queryName("streaming_watermark") \
    .start()

# Wait for processing
time.sleep(5)

# Check results
result = spark.sql("SELECT * FROM streaming_watermark ORDER BY window")
result.show(truncate=False)

# Stop query
query.stop()
```

### Verification

- [ ] Watermark is applied correctly
- [ ] Late data is handled according to watermark policy
- [ ] Window aggregation updates correctly

## Exercise 6: Streaming Sinks

### Task

Write streaming data to various sinks.

### Steps

1. **Write to memory sink**

```python
# Memory sink (for testing)
df_streaming = spark.readStream \
    .schema(streaming_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

query = df_streaming.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("memory_sink") \
    .start()

time.sleep(5)
spark.sql("SELECT * FROM memory_sink").show()
query.stop()
```

### Verification

- [ ] Memory sink works correctly
- [ ] File sink writes data successfully
- [ ] Console sink displays output

## Exercise 7: Monitoring Streaming Queries

### Task

Monitor and manage streaming queries.

### Steps

1. **Query active streaming queries**

```python
# Start a streaming query
df_streaming = spark.readStream \
    .schema(streaming_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

query = df_streaming.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("monitoring_query") \
    .start()

# Get query status
print(f"Query name: {query.name}")
print(f"Query id: {query.id}")
print(f"Is active: {query.isActive}")
print(f"Status: {query.status}")
```

### Verification

- [ ] You can query streaming query status
- [ ] You can monitor query progress
- [ ] You can handle query exceptions

## Cleanup

```python
# Stop Spark session
spark.stop()

# Clean up streaming data
import shutil
shutil.rmtree("/opt/spark/data/streaming", ignore_errors=True)
shutil.rmtree("/opt/spark/data/streaming_output", ignore_errors=True)
shutil.rmtree("/opt/spark/checkpoint", ignore_errors=True)

# Stop Docker containers
docker-compose down
```

## Troubleshooting

### Issue: Streaming query not processing data
**Solution**: Check if new files are being added to the streaming directory

### Issue: Out of memory in streaming
**Solution**: Increase memory allocation or reduce batch size

### Issue: Late data not being processed
**Solution**: Adjust watermark delay or use update output mode

## Expected Outcomes

By the end of this lab, you should:
- Understand Structured Streaming concepts
- Be able to create streaming DataFrames
- Apply transformations to streaming data
- Perform windowed aggregations
- Handle late data with watermarking
- Write to various streaming sinks
- Monitor and manage streaming queries

## Next Steps

- Chapter 6: Machine Learning with MLlib
- Chapter 7: Production Deployment
- Advanced Streaming: Stateful Operations, Join Streams

## Additional Resources

- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Streaming Sources and Sinks](https://spark.apache.org/docs/latest/structured-streaming-sources.html)
- [Fault Tolerance Semantics](https://spark.apache.org/docs/latest/structured-streaming-semantics.html)