# Chapter 3: Advanced DataFrame Operations

## Overview

This lab covers advanced DataFrame operations in Apache Spark, including joins, window functions, complex data types, and performance optimization techniques. These operations are essential for building sophisticated data pipelines and performing complex analytics at scale.

### Why Advanced Operations Matter

Real-world data engineering often requires:
- **Complex joins** between multiple datasets
- **Window functions** for time-series and ranking operations
- **Complex data types** (arrays, maps, structs) for nested data
- **Performance optimization** to handle large datasets efficiently
- **UDFs (User Defined Functions)** for custom business logic

Mastering these advanced operations enables you to solve complex business problems and build scalable data solutions.

### Real-World Applications

- **Customer Analytics**: Calculating running totals, moving averages, and rankings
- **Financial Analysis**: Computing year-over-year growth, rolling aggregations
- **Log Analysis**: Processing nested JSON logs and extracting insights
- **Recommendation Systems**: Building collaborative filtering models
- **Data Warehousing**: Building complex ETL pipelines with multiple data sources

## Learning Objectives

By the end of this lab, you will be able to:
- Perform different types of joins (inner, outer, left, right, semi, anti)
- Use window functions for advanced analytics
- Work with complex data types (arrays, maps, structs)
- Create and use UDFs (User Defined Functions)
- Optimize DataFrame operations for performance
- Handle broadcast joins and partitioning strategies

## Prerequisites

- Completion of Chapter 1: Spark Fundamentals
- Completion of Chapter 2: Data Loading and Transformation
- Understanding of SQL joins and aggregations
- Docker environment running

## Estimated Time

90-120 minutes

## Lab Environment

This lab uses the same Docker-based Spark environment.

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
from pyspark.sql.functions import col, lit, when, count, sum, avg, max, min
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType, ArrayType, MapType
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead, first, last

spark = SparkSession.builder \
    .appName("AdvancedDataFrameOperations") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.autoBroadcastJoinThreshold", "10m") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

## Exercise 1: DataFrame Joins

### Task

Perform various types of joins between DataFrames.

### Steps

1. **Create sample datasets**

```python
# Employees dataset
employees_data = [
    (1, "Alice", 28, 101),
    (2, "Bob", 35, 102),
    (3, "Charlie", 42, 101),
    (4, "Diana", 31, 103),
    (5, "Eve", 29, 102)
]

employees_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("dept_id", IntegerType(), True)
])

df_employees = spark.createDataFrame(employees_data, employees_schema)
df_employees.show()

# Departments dataset
departments_data = [
    (101, "Engineering", "Building A"),
    (102, "Marketing", "Building B"),
    (103, "Sales", "Building C"),
    (104, "HR", "Building D")
]

departments_schema = StructType([
    StructField("dept_id", IntegerType(), True),
    StructField("dept_name", StringType(), True),
    StructField("location", StringType(), True)
])

df_departments = spark.createDataFrame(departments_data, departments_schema)
df_departments.show()
```

2. **Inner Join**

```python
# Inner join - only matching records
df_inner = df_employees.join(
    df_departments,
    df_employees.dept_id == df_departments.dept_id,
    "inner"
)

df_inner.show()
```

3. **Left Join**

```python
# Left join - all employees, matching departments
df_left = df_employees.join(
    df_departments,
    df_employees.dept_id == df_departments.dept_id,
    "left"
)

df_left.show()
```

4. **Self Join**

```python
# Self join - find employees in same department
df_self = df_employees.alias("e1").join(
    df_employees.alias("e2"),
    (col("e1.dept_id") == col("e2.dept_id")) & (col("e1.id") != col("e2.id")),
    "inner"
).select(
    col("e1.name").alias("employee"),
    col("e2.name").alias("colleague"),
    col("e1.dept_id")
)

df_self.show()
```

### Verification

- [ ] All join types work correctly
- [ ] Results match expected behavior for each join type
- [ ] Self join produces correct colleague relationships

## Exercise 2: Window Functions

### Task

Use window functions for advanced analytics.

### Steps

1. **Create sample sales data**

```python
sales_data = [
    ("Alice", "2023-01-01", 1000),
    ("Alice", "2023-01-02", 1500),
    ("Alice", "2023-01-03", 1200),
    ("Bob", "2023-01-01", 800),
    ("Bob", "2023-01-02", 900),
    ("Bob", "2023-01-03", 1100)
]

sales_schema = StructType([
    StructField("salesperson", StringType(), True),
    StructField("date", StringType(), True),
    StructField("amount", IntegerType(), True)
])

df_sales = spark.createDataFrame(sales_data, sales_schema)
df_sales.show()
```

2. **Ranking functions**

```python
# Define window specification
window_spec = Window.partitionBy("salesperson").orderBy(col("date"))

# Row number
df_with_row_num = df_sales.withColumn(
    "row_num",
    row_number().over(window_spec)
)

# Rank
df_with_rank = df_sales.withColumn(
    "rank",
    rank().over(window_spec)
)

# Dense rank
df_with_dense_rank = df_sales.withColumn(
    "dense_rank",
    dense_rank().over(window_spec)
)

df_with_ranking = df_sales.withColumn(
    "row_num",
    row_number().over(window_spec)
).withColumn(
    "rank",
    rank().over(window_spec)
).withColumn(
    "dense_rank",
    dense_rank().over(window_spec)
)

df_with_ranking.show()
```

3. **Lead and Lag functions**

```python
# Previous day's amount
df_lag = df_sales.withColumn(
    "prev_amount",
    lag("amount", 1).over(window_spec)
)

# Next day's amount
df_lead = df_sales.withColumn(
    "next_amount",
    lead("amount", 1).over(window_spec)
)

df_lead_lag = df_sales.withColumn(
    "prev_amount",
    lag("amount", 1).over(window_spec)
).withColumn(
    "next_amount",
    lead("amount", 1).over(window_spec)
)

df_lead_lag.show()
```

### Verification

- [ ] Ranking functions work correctly
- [ ] Window aggregations produce correct results
- [ ] Lead and lag functions work as expected

## Exercise 3: Complex Data Types

### Task

Work with arrays, maps, and structs.

### Steps

1. **Array operations**

```python
# Create data with arrays
array_data = [
    (1, "Alice", ["Python", "Spark", "SQL"]),
    (2, "Bob", ["Java", "Hadoop"]),
    (3, "Charlie", ["Scala", "Spark", "Kafka", "SQL"])
]

array_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("skills", ArrayType(StringType()), True)
])

df_arrays = spark.createDataFrame(array_data, array_schema)
df_arrays.show()

# Array operations
from pyspark.sql.functions import size, array_contains, explode

df_array_ops = df_arrays.select(
    col("name"),
    size(col("skills")).alias("skill_count"),
    array_contains(col("skills"), "Spark").alias("knows_spark")
)

df_array_ops.show()

# Explode arrays
df_exploded = df_arrays.select(
    col("name"),
    explode(col("skills")).alias("skill")
)

df_exploded.show()
```

### Verification

- [ ] Array operations work correctly
- [ ] Map operations work as expected
- [ ] Struct field access works correctly

## Exercise 4: User Defined Functions

### Task

Create and use UDFs for custom transformations.

### Steps

1. **Create a simple UDF**

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

# Define a Python function
def categorize_age(age):
    if age < 30:
        return "Young"
    elif age < 40:
        return "Middle"
    else:
        return "Senior"

# Register as UDF
categorize_age_udf = udf(categorize_age, StringType())

# Use UDF
df_employees_with_category = df_employees.withColumn(
    "age_category",
    categorize_age_udf(col("age"))
)

df_employees_with_category.show()
```

### Verification

- [ ] Simple UDF works correctly
- [ ] Multi-parameter UDF works as expected
- [ ] Pandas UDF improves performance

## Exercise 5: Performance Optimization

### Task

Optimize DataFrame operations for better performance.

### Steps

1. **Broadcast join optimization**

```python
# Small table (departments) should be broadcasted
df_broadcast = df_employees.join(
    df_departments.hint("broadcast"),
    df_employees.dept_id == df_departments.dept_id,
    "inner"
)

df_broadcast.show()
```

2. **Cache and persist**

```python
# Cache frequently used DataFrame
df_employees.cache()

# First access (computes)
df_employees.count()

# Second access (uses cache)
df_employees.count()

# Un cache when done
df_employees.unpersist()
```

### Verification

- [ ] Broadcast join works correctly
- [ ] Caching improves performance
- [ ] Repartitioning works as expected

## Cleanup

```python
# Stop Spark session
spark.stop()

# Stop Docker containers
docker-compose down
```

## Troubleshooting

### Issue: Out of memory during joins
**Solution**: Use broadcast joins for small tables or increase memory allocation

### Issue: Slow performance with UDFs
**Solution**: Use Pandas UDFs or built-in functions when possible

### Issue: Skewed data causing slow joins
**Solution**: Use salting or repartitioning strategies

## Expected Outcomes

By the end of this lab, you should:
- Be able to perform various types of joins
- Understand and use window functions effectively
- Work with complex data types (arrays, maps, structs)
- Create and use UDFs for custom logic
- Optimize DataFrame operations for performance
- Build complex queries combining multiple operations

## Next Steps

- Chapter 4: Spark SQL and Query Optimization
- Chapter 5: Spark Streaming Fundamentals
- Chapter 6: Machine Learning with MLlib

## Additional Resources

- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Window Functions](https://spark.apache.org/docs/latest/api/sql/index.html#window-functions)
- [Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)