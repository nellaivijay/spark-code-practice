# Chapter 1: Spark Fundamentals

## Overview

This lab introduces the fundamentals of Apache Spark, a unified analytics engine for large-scale data processing. Understanding Spark fundamentals is essential for any data engineer or data scientist working with big data. Spark provides a powerful framework for distributed computing that enables processing of massive datasets across clusters of computers.

### Why Spark Fundamentals Matter

Apache Spark has become the de facto standard for big data processing due to its:
- **Speed**: In-memory processing that is 100x faster than Hadoop MapReduce
- **Ease of Use**: Simple APIs in Scala, Python, Java, and R
- **Generality**: Combines SQL, streaming, machine learning, and graph processing
- **Runs Everywhere**: Runs on Hadoop, Kubernetes, standalone, or in the cloud

### Real-World Applications

- **Data Processing Pipeline**: ETL processes for data warehousing
- **Real-time Analytics**: Processing streaming data from IoT devices
- **Machine Learning**: Training models on large datasets
- **Graph Processing**: Social network analysis and recommendation systems
- **Log Analysis**: Processing server logs for insights

## Learning Objectives

By the end of this lab, you will be able to:
- Understand Spark architecture and components
- Set up a Spark environment using Docker
- Create and manipulate Spark DataFrames
- Perform basic data transformations
- Understand RDDs vs DataFrames vs Datasets
- Use Spark SQL for data analysis

## Prerequisites

- Docker and Docker Compose installed
- Basic knowledge of Python or Scala
- Understanding of data structures (tables, rows, columns)
- Terminal/command line familiarity

## Estimated Time

60-90 minutes

## Lab Environment

This lab uses a Docker-based Spark environment with:
- Spark Master and Workers
- Jupyter Notebook with PySpark
- MinIO for data storage
- PostgreSQL for Hive Metastore

## Setup

### 1. Start the Environment

```bash
# Navigate to the project directory
cd spark-code-practice

# Start the Spark cluster
./scripts/setup.sh

# Verify services are running
docker-compose ps
```

### 2. Access Jupyter Notebook

Open your browser and navigate to: `http://localhost:8888`

### 3. Initialize Spark Session

In a Jupyter notebook, create a Spark session:

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("SparkFundamentals") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.executor.cores", "1") \
    .getOrCreate()

# Verify Spark session
print(f"Spark version: {spark.version}")
print(f"Spark master: {spark.conf.get('spark.master')}")
```

## Exercise 1: Understanding Spark Architecture

### Task

Explore the Spark architecture and understand its components.

### Steps

1. **Access Spark Master UI**
   - Navigate to `http://localhost:8080`
   - Observe the running workers and applications
   - Note the resource allocation (cores, memory)

2. **Access Worker UI**
   - Click on one of the workers in the Master UI
   - Observe the executor information
   - Note the allocated resources

3. **Understand Components**
   - **Driver**: The main process that runs the user's main() function
   - **Executor**: Processes that run tasks and store data in memory
   - **Cluster Manager**: Allocates resources (Standalone, YARN, Kubernetes)
   - **Worker**: Hosts that run Spark applications

### Verification

- [ ] Spark Master UI is accessible
- [ ] Workers are registered and running
- [ ] You understand the role of each component

## Exercise 2: Creating Your First DataFrame

### Task

Create a DataFrame from a sample dataset and perform basic operations.

### Steps

1. **Create a sample dataset**

```python
# Create sample data
data = [
    ("Alice", 25, "Engineering"),
    ("Bob", 30, "Marketing"),
    ("Charlie", 35, "Engineering"),
    ("Diana", 28, "Sales"),
    ("Eve", 32, "Marketing")
]

# Define schema
columns = ["name", "age", "department"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Display the DataFrame
df.show()
```

2. **Explore DataFrame schema**

```python
# Print schema
df.printSchema()

# Show column names
df.columns

# Count rows
df.count()
```

3. **Perform basic operations**

```python
# Filter data
df.filter(df.age > 30).show()

# Select columns
df.select("name", "department").show()

# Sort data
df.orderBy("age").show()

# Group by and count
df.groupBy("department").count().show()
```

### Verification

- [ ] DataFrame is created successfully
- [ ] Schema is displayed correctly
- [ ] Basic operations produce expected results

## Exercise 3: Working with Different Data Sources

### Task

Load data from different sources and understand how Spark handles various file formats.

### Steps

1. **Create a CSV file**

```python
# Create sample CSV data
csv_data = """name,age,department,salary
Alice,25,Engineering,75000
Bob,30,Marketing,65000
Charlie,35,Engineering,95000
Diana,28,Sales,70000
Eve,32,Marketing,72000"""

# Write to CSV
with open("/opt/spark/data/employees.csv", "w") as f:
    f.write(csv_data)
```

2. **Read CSV file**

```python
# Read CSV
df_csv = spark.read.csv(
    "/opt/spark/data/employees.csv",
    header=True,
    inferSchema=True
)

df_csv.show()
df_csv.printSchema()
```

3. **Create and read JSON file**

```python
# Create sample JSON data
json_data = """[
    {"id": 1, "name": "Alice", "age": 25, "department": "Engineering"},
    {"id": 2, "name": "Bob", "age": 30, "department": "Marketing"},
    {"id": 3, "name": "Charlie", "age": 35, "department": "Engineering"}
]"""

# Write to JSON
with open("/opt/spark/data/employees.json", "w") as f:
    f.write(json_data)

# Read JSON
df_json = spark.read.json("/opt/spark/data/employees.json")
df_json.show()
```

### Verification

- [ ] CSV file is created and read successfully
- [ ] JSON file is created and read successfully
- [ ] Schema inference works correctly

## Exercise 4: DataFrame Operations

### Task

Perform various DataFrame transformations and actions.

### Steps

1. **Transformations (lazy operations)**

```python
# Add a new column
df_with_salary = df.withColumn("salary", df.age * 2000)
df_with_salary.show()

# Rename columns
df_renamed = df_with_salary.withColumnRenamed("age", "years_old")
df_renamed.show()

# Drop columns
df_dropped = df_renamed.drop("age")
df_dropped.show()
```

2. **Actions (eager operations)**

```python
# Count
count = df.count()
print(f"Total rows: {count}")

# Collect
data_list = df.collect()
print(data_list)

# Take
first_rows = df.take(2)
print(first_rows)

# Show
df.show(5)
```

3. **Advanced operations**

```python
from pyspark.sql.functions import col, avg, max, min, count

# Aggregations
df.agg(
    avg("age").alias("avg_age"),
    max("age").alias("max_age"),
    min("age").alias("min_age"),
    count("*").alias("total_count")
).show()

# Window functions
from pyspark.sql.window import Window
from pyspark.sql.functions import rank

window_spec = Window.partitionBy("department").orderBy(col("age").desc())

df_with_rank = df.withColumn(
    "rank",
    rank().over(window_spec)
)
df_with_rank.show()
```

### Verification

- [ ] Transformations work correctly
- [ ] Actions trigger computation
- [ ] Aggregations produce correct results

## Exercise 5: Spark SQL

### Task

Use Spark SQL to query DataFrames using SQL syntax.

### Steps

1. **Register DataFrame as temporary view**

```python
# Register as temporary view
df.createOrReplaceTempView("employees")

# Run SQL query
result = spark.sql("""
    SELECT department,
           COUNT(*) as employee_count,
           AVG(age) as avg_age
    FROM employees
    GROUP BY department
    ORDER BY employee_count DESC
""")

result.show()
```

2. **Complex SQL queries**

```python
# Join with itself (self-join)
result = spark.sql("""
    SELECT e1.name as employee_name,
           e1.age,
           e1.department,
           e2.name as colleague_name
    FROM employees e1
    JOIN employees e2
    ON e1.department = e2.department
    WHERE e1.name != e2.name
    ORDER BY e1.department, e1.name
""")

result.show()
```

3. **Subqueries**

```python
# Find employees older than average
result = spark.sql("""
    SELECT name, age, department
    FROM employees
    WHERE age > (SELECT AVG(age) FROM employees)
    ORDER BY age DESC
""")

result.show()
```

### Verification

- [ ] Temporary view is created successfully
- [ ] SQL queries execute correctly
- [ ] Results match expected outcomes

## Exercise 6: Caching and Persistence

### Task

Understand caching and persistence for performance optimization.

### Steps

1. **Cache a DataFrame**

```python
# Cache DataFrame
df.cache()

# First action (will compute)
df.count()

# Second action (will use cached data)
df.count()

# Un cache
df.unpersist()
```

2. **Compare performance**

```python
import time

# Without cache
start = time.time()
for i in range(5):
    df.count()
end = time.time()
print(f"Without cache: {end - start:.2f} seconds")

# With cache
df.cache()
start = time.time()
for i in range(5):
    df.count()
end = time.time()
print(f"With cache: {end - start:.2f} seconds")

df.unpersist()
```

### Verification

- [ ] Caching improves performance
- [ ] Cache is cleared correctly

## Cleanup

```python
# Stop Spark session
spark.stop()

# Stop Docker containers
docker-compose down
```

## Troubleshooting

### Issue: Spark Master not accessible
**Solution**: Check if Docker containers are running: `docker-compose ps`

### Issue: Out of memory errors
**Solution**: Increase memory allocation in docker-compose.yaml

### Issue: Workers not connecting to Master
**Solution**: Check network configuration and ensure containers are on the same network

## Expected Outcomes

By the end of this lab, you should:
- Understand Spark architecture and components
- Be able to create and manipulate DataFrames
- Know how to load data from various sources
- Understand the difference between transformations and actions
- Be able to use Spark SQL for data analysis
- Understand caching and persistence

## Next Steps

- Chapter 2: Data Loading and Transformation
- Chapter 3: Advanced DataFrame Operations
- Chapter 4: Spark Streaming Fundamentals
- Chapter 5: Machine Learning with MLlib

## Additional Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark Programming Guide](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)