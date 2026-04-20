# Lab 5: Spark Streaming Fundamentals - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 5: Spark Streaming Fundamentals.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Spark environment set up (run `./scripts/setup.sh`)
- Jupyter Notebook accessible at http://localhost:8888
- Completion of Lab 1: Spark Fundamentals
- Completion of Lab 2: Data Loading & Transformation

## Setup Instructions

### 1. Start the Environment
```bash
cd spark-code-practice
./scripts/start.sh
```

### 2. Open Jupyter Notebook
- Navigate to http://localhost:8888 in your browser
- Open `notebooks/chapter-05-spark-streaming-fundamentals.ipynb`

## Lab Walkthrough

### Section A: Structured Streaming Concepts

#### Step 1: Import Required Libraries
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, count, avg, sum
from pyspark.sql.functions import current_timestamp, expr
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
import os
import time
```

**Explanation**: Import PySpark libraries for streaming operations, window functions, and data types.

#### Step 2: Create SparkSession for Streaming
```python
spark = SparkSession.builder \
    .appName("SparkStreamingFundamentals") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.streaming.checkpointLocation", "checkpoint/streaming") \
    .config("spark.sql.shuffle.partitions", "10") \
    .getOrCreate()

# Create checkpoint directory
os.makedirs("checkpoint/streaming", exist_ok=True)

print(f"Spark version: {spark.version}")
print(f"Streaming checkpoint location: checkpoint/streaming")
```

**Key Concept**: Checkpoint locations enable fault tolerance by saving query state. Essential for production streaming applications.

**Expected Output**: 
```
Spark version: 3.5.0
Streaming checkpoint location: checkpoint/streaming
```

#### Step 3: Understand Structured Streaming Concepts
```python
print("""Structured Streaming Key Concepts:

1. Input Table: Unbounded stream of data treated as a table
2. Query: Standard batch query on the input table
3. Result Table: Continuously updated as new data arrives
4. Output: External sink where results are written
5. Output Mode: How results are written (append, complete, update)
6. Trigger: When to execute the query (processing time, once, continuous)
7. Checkpoint: Fault tolerance through state recovery
""")
```

**Key Concept**: Structured Streaming treats streaming as a continuous series of batch operations, making it easier to reason about and debug.

### Section B: Creating Streaming Sources

#### Step 4: Create Rate Source
```python
# Rate source (for testing)
# Generates data continuously with timestamp and value
rate_stream = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 10) \
    .option("numPartitions", 2) \
    .load()

print("Rate source created (generates 10 rows per second)")
print(f"Schema: {rate_stream.schema}")
```

**Explanation**: The rate source is useful for testing as it generates data at a consistent rate with timestamps.

**Practice**: Try different `rowsPerSecond` values and observe the effect.

#### Step 5: Create File Source
```python
# File source (monitor directory for new files)
# Create streaming directory
streaming_dir = "data/streaming/input"
os.makedirs(streaming_dir, exist_ok=True)

# Define schema for file data
schema = StructType([
    StructField("event_time", TimestampType(), True),
    StructField("event_type", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("value", DoubleType(), True)
])

# Create file streaming source
file_stream = spark.readStream \
    .schema(schema) \
    .option("maxFilesPerTrigger", 1) \
    .csv(streaming_dir)

print(f"File source created monitoring: {streaming_dir}")
```

**Key Concept**: File sources monitor directories for new files. Use `maxFilesPerTrigger` to control processing rate.

**Practice**: Create test files in the streaming directory and observe how they're processed.

### Section C: Basic Streaming Transformations

#### Step 6: Apply Simple Transformations
```python
# Simple transformation on rate stream
transformed_stream = rate_stream \
    .withColumn("doubled", col("value") * 2) \
    .withColumn("is_even", (col("value") % 2) == 0)

print("Transformed stream created with doubled values and even/odd flag")
```

**Key Concept**: Streaming transformations work exactly like batch transformations. Spark handles the incremental execution.

#### Step 7: Filter Streaming Data
```python
# Filter streaming data
filtered_stream = rate_stream.filter(col("value") > 50)

print("Filtered stream created (values > 50)")
```

**Practice**: Combine transformations and filters to create more complex processing logic.

### Section D: Window Operations

#### Step 8: Create Tumbling Window
```python
# Tumbling window (non-overlapping)
windowed_stream = rate_stream \
    .groupBy(window(col("timestamp"), "5 seconds")) \
    .agg(count("*").alias("count"), avg("value").alias("avg_value"))

print("Tumbling window stream created (5-second windows)")
```

**Key Concept**: Tumbling windows are non-overlapping, fixed-size time windows. Each event belongs to exactly one window.

#### Step 9: Create Sliding Window
```python
# Sliding window (overlapping)
sliding_stream = rate_stream \
    .groupBy(window(col("timestamp"), "5 seconds", "2 seconds")) \
    .agg(count("*").alias("count"), sum("value").alias("total_value"))

print("Sliding window stream created (5-second windows, 2-second slide)")
```

**Key Concept**: Sliding windows overlap, with events potentially belonging to multiple windows. Useful for smoothing aggregations.

**Practice**: Compare tumbling vs sliding window results to understand the difference.

### Section E: Watermarking

#### Step 10: Add Watermark for Late Data Handling
```python
# Add watermark to handle late data
watermarked_stream = rate_stream \
    .withWatermark("timestamp", "10 seconds") \
    .groupBy(window(col("timestamp"), "5 seconds")) \
    .agg(count("*").alias("count"))

print("Watermarked stream created (10-second watermark)")
print("Late data arriving within 10 seconds will be included")
```

**Key Concept**: Watermarking allows Spark to handle late data while controlling state size. Data arriving after the watermark is dropped.

**Practice**: Experiment with different watermark durations and observe the effect on late data handling.

### Section F: Output Modes

#### Step 11: Understand Output Modes
```python
print("""Output Modes:

1. Append Mode (default): Only new rows are added
   - Use with: Simple aggregations, filters
   - Not for: Stateful aggregations

2. Complete Mode: All rows are output
   - Use with: Global aggregations
   - Not for: Unbounded streams

3. Update Mode: Only changed rows are output
   - Use with: Stateful aggregations
   - Requires: Result table with unique keys
""")
```

**Key Concept**: Output modes determine how results are written to sinks. Choose based on your use case and aggregation type.

### Section G: Writing Streaming Queries

#### Step 12: Write to Console Sink
```python
# Write to console (for debugging)
console_query = transformed_stream \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="5 seconds") \
    .start()

print("Console query started (will output every 5 seconds)")
print("Query ID:", console_query.id)
print("Query status:", console_query.status)
```

**Key Concept**: Console sink is useful for debugging and development. Output appears in the Spark driver logs.

**Expected Output**: Console output showing streaming results every 5 seconds.

#### Step 13: Write to Memory Sink
```python
# Write to memory (for testing and queries)
memory_query = windowed_stream \
    .writeStream \
    .outputMode("complete") \
    .format("memory") \
    .queryName("windowed_counts") \
    .trigger(processingTime="5 seconds") \
    .start()

print("Memory query started")
print("Query ID:", memory_query.id)
```

**Key Concept**: Memory sink stores results in an in-memory table that can be queried with SQL. Useful for testing.

#### Step 14: Query In-Memory Table
```python
# Query the in-memory table
time.sleep(10)  # Wait for some data to be processed

print("Querying in-memory table:")
spark.sql("SELECT * FROM windowed_counts ORDER BY window DESC").show()
```

**Practice**: Query the in-memory table at different times to see how results accumulate.

#### Step 15: Write to File Sink
```python
# Write to file (for persistence)
output_dir = "data/streaming/output"
os.makedirs(output_dir, exist_ok=True)

file_query = filtered_stream \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", output_dir) \
    .option("checkpointLocation", "checkpoint/file_sink") \
    .trigger(processingTime="10 seconds") \
    .start()

print(f"File query started writing to: {output_dir}")
print("Query ID:", file_query.id)
```

**Key Concept**: File sinks write results to persistent storage. Essential for production applications requiring data retention.

### Section H: Query Management

#### Step 16: List Active Queries
```python
# List active queries
print("Active streaming queries:")
for query in spark.streams.active:
    print(f"  ID: {query.id}")
    print(f"  Name: {query.name}")
    print(f"  Status: {query.status}")
    print(f"  Progress: {query.progress}")
    print()

# Get query by ID
if spark.streams.active:
    query = spark.streams.active[0]
    print(f"Query details for ID {query.id}:")
    print(f"Last progress: {query.lastProgress}")
    print(f"Recent progress: {query.recentProgress}")
```

**Key Concept**: Query management allows you to monitor and control running streaming queries programmatically.

#### Step 17: Stop All Queries
```python
# Stop all queries
print("Stopping all streaming queries...")
for query in spark.streams.active:
    print(f"Stopping query {query.id}...")
    query.stop()
    print(f"Query {query.id} stopped")

print("\nAll queries stopped")
```

**Key Concept**: Always stop queries when done to free resources. In production, use graceful shutdown procedures.

### Section I: Advanced Streaming Features

#### Step 18: Session Windows
```python
# Session windows (dynamic windows based on activity gaps)
from pyspark.sql.functions import session_window

session_stream = rate_stream \
    .withWatermark("timestamp", "10 seconds") \
    .groupBy(session_window(col("timestamp"), "5 seconds")) \
    .agg(count("*").alias("count"))

print("Session window stream created (5-second inactivity gap)")
```

**Key Concept**: Session windows are dynamic windows based on periods of activity followed by inactivity gaps.

**Practice**: Compare session windows with tumbling/sliding windows for different use cases.

#### Step 19: Multiple Sinks Strategy
```python
print("""Multiple Sinks Strategy:

1. Create multiple queries from the same source
2. Each query can have different transformations
3. Each query writes to a different sink
4. Useful for: Different aggregations, different output formats
""")
```

**Key Concept**: You can create multiple queries from the same source for different processing needs, each writing to different sinks.

## Troubleshooting Tips

### Issue: Streaming Query Not Starting
**Solution**:
- Verify checkpoint directory exists and is writable
- Check that output directory doesn't already exist
- Ensure Spark configuration is correct
- Check for conflicting query names

### Issue: Late Data Being Dropped
**Solution**:
- Increase watermark duration
- Check timestamp column is correct
- Verify data timestamps are in expected format
- Monitor query metrics for late data statistics

### Issue: Out of Memory in Streaming
**Solution**:
- Reduce window sizes
- Increase watermark to drop old state faster
- Reduce state retention period
- Increase executor memory
- Use session windows instead of sliding windows

### Issue: File Source Not Processing New Files
**Solution**:
- Verify files are being written to the correct directory
- Check file permissions
- Ensure files are complete (not being written)
- Use `maxFilesPerTrigger` to control processing rate
- Check Spark logs for errors

### Issue: Query Performance Issues
**Solution**:
- Monitor query metrics in Spark UI
- Optimize transformations (filter early, select needed columns)
- Adjust trigger interval
- Use appropriate output mode
- Consider partitioning for file sinks

## Check Your Understanding

1. What is the difference between tumbling and sliding windows?
2. What is the purpose of watermarking in Structured Streaming?
3. When should you use each output mode (append, complete, update)?
4. Why are checkpoint locations important in streaming?
5. How do session windows differ from fixed-size windows?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-05-spark-streaming-fundamentals-solution.ipynb`
4. Proceed to Lab 6: Machine Learning with MLlib

## Additional Resources

- [Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Streaming Performance Tuning](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#performance-considerations)
- [Streaming Cheatsheet](cheatsheets/streaming-performance-cheatsheet.ipynb)
- [Watermarking Documentation](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#handling-late-data-with-watermarking)
