# Chapter 4: Spark SQL and Query Optimization

## Overview

This lab covers Spark SQL, query optimization techniques, and performance tuning strategies. Spark SQL provides a powerful SQL interface for working with structured data, while understanding query optimization is crucial for building efficient data pipelines.

### Why Spark SQL and Optimization Matter

Spark SQL is essential because:
- **SQL Familiarity**: Leverages existing SQL skills
- **Performance**: Catalyst optimizer automatically optimizes queries
- **Integration**: Works seamlessly with DataFrame API
- **Universal**: Supports various data sources through a unified interface

Query optimization is critical because:
- **Cost Efficiency**: Reduces compute costs by minimizing resource usage
- **Performance**: Faster query execution and data processing
- **Scalability**: Enables handling of larger datasets efficiently
- **User Experience**: Provides faster insights and better responsiveness

### Real-World Applications

- **Data Warehousing**: Building and optimizing data warehouses
- **Business Intelligence**: Fast analytical queries for dashboards
- **Data Lakes**: Querying massive datasets in data lakes
- **Ad-hoc Analysis**: Quick data exploration and analysis
- **ETL Pipelines**: Optimized data transformation pipelines

## Learning Objectives

By the end of this lab, you will be able to:
- Use Spark SQL for data analysis
- Understand the Catalyst optimizer
- Write optimized SQL queries
- Use query hints for manual optimization
- Analyze query execution plans
- Implement performance tuning strategies
- Use adaptive query execution

## Prerequisites

- Completion of Chapter 1: Spark Fundamentals
- Completion of Chapter 2: Data Loading and Transformation
- Understanding of SQL basics
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
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

spark = SparkSession.builder \
    .appName("SparkSQLOptimization") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.sql.inMemoryColumnarStorage.compressed", "true") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

## Exercise 1: Spark SQL Basics

### Task

Use Spark SQL for data analysis and exploration.

### Steps

1. **Create sample datasets**

```python
# Create employees table
employees_data = [
    (1, "Alice Johnson", 28, 75000, 101, "2020-01-15"),
    (2, "Bob Smith", 35, 85000, 102, "2019-03-22"),
    (3, "Charlie Brown", 42, 95000, 101, "2018-06-10"),
    (4, "Diana Prince", 31, 72000, 103, "2021-02-28"),
    (5, "Eve Davis", 29, 68000, 102, "2020-11-05")
]

employees_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True),
    StructField("dept_id", IntegerType(), True),
    StructField("hire_date", StringType(), True)
])

df_employees = spark.createDataFrame(employees_data, employees_schema)
df_employees.createOrReplaceTempView("employees")

# Create departments table
departments_data = [
    (101, "Engineering", "Building A", "John Doe"),
    (102, "Marketing", "Building B", "Jane Smith"),
    (103, "Sales", "Building C", "Bob Johnson"),
    (104, "HR", "Building D", "Alice Williams")
]

departments_schema = StructType([
    StructField("dept_id", IntegerType(), True),
    StructField("dept_name", StringType(), True),
    StructField("location", StringType(), True),
    StructField("manager", StringType(), True)
])

df_departments = spark.createDataFrame(departments_data, departments_schema)
df_departments.createOrReplaceTempView("departments")

# Create sales table
sales_data = [
    ("Alice Johnson", "2023-01-01", 1000, "Product A"),
    ("Alice Johnson", "2023-01-02", 1500, "Product B"),
    ("Alice Johnson", "2023-01-03", 1200, "Product A"),
    ("Bob Smith", "2023-01-01", 800, "Product C"),
    ("Bob Smith", "2023-01-02", 900, "Product A"),
    ("Bob Smith", "2023-01-03", 1100, "Product B")
]

sales_schema = StructType([
    StructField("salesperson", StringType(), True),
    StructField("date", StringType(), True),
    StructField("amount", IntegerType(), True),
    StructField("product", StringType(), True)
])

df_sales = spark.createDataFrame(sales_data, sales_schema)
df_sales.createOrReplaceTempView("sales")
```

2. **Basic SQL queries**

```python
# Simple SELECT
result = spark.sql("SELECT * FROM employees LIMIT 5")
result.show()

# WHERE clause
result = spark.sql("""
    SELECT name, age, salary 
    FROM employees 
    WHERE age > 30 
    ORDER BY age DESC
""")
result.show()

# GROUP BY and aggregations
result = spark.sql("""
    SELECT department, 
           COUNT(*) as employee_count,
           AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    ORDER BY employee_count DESC
""")
result.show()
```

### Verification

- [ ] Basic SQL queries work correctly
- [ ] JOIN operations produce expected results
- [ ] Subqueries and CTEs function properly

## Exercise 2: Understanding the Catalyst Optimizer

### Task

Examine query execution plans and understand optimization.

### Steps

1. **View logical and physical plans**

```python
# Simple query
query = "SELECT name, salary FROM employees WHERE age > 30"
df = spark.sql(query)

# Logical plan
df.explain(extended=False)

# Extended plan (logical + physical)
df.explain(extended=True)
```

### Verification

- [ ] You can view execution plans
- [ ] You understand the difference between logical and physical plans
- [ ] You can identify join strategies in the plan

## Exercise 3: Query Optimization Techniques

### Task

Apply optimization techniques to improve query performance.

### Steps

1. **Column pruning**

```python
# Bad: Select all columns
df_all = spark.sql("SELECT * FROM employees")
df_all.explain()

# Good: Select only needed columns
df_pruned = spark.sql("SELECT name, salary FROM employees")
df_pruned.explain()
```

2. **Filter pushdown**

```python
# Filter early in the query
df_filtered = spark.sql("""
    SELECT name, salary
    FROM employees
    WHERE age > 30
""")
df_filtered.explain()
```

### Verification

- [ ] Column pruning reduces data read
- [ ] Filter pushdown improves performance
- [ ] Appropriate join types are selected

## Exercise 4: Query Hints

### Task

Use query hints to guide the optimizer.

### Steps

1. **Broadcast join hint**

```python
# Force broadcast join
df_broadcast = spark.sql("""
    SELECT /*+ BROADCAST(d) */ 
           e.name, d.dept_name
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
""")
df_broadcast.explain()
```

### Verification

- [ ] Broadcast join hint works correctly
- [ ] Partition pruning reduces data scanned
- [ ] Coalesce and repartition hints work as expected

## Exercise 5: Adaptive Query Execution

### Task

Use adaptive query execution for automatic optimization.

### Steps

1. **Enable adaptive query execution**

```python
# Check if AQE is enabled
print(f"AQE enabled: {spark.conf.get('spark.sql.adaptive.enabled')}")

# Enable AQE if not already enabled
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

### Verification

- [ ] AQE is enabled
- [ ] AQE optimizes shuffle operations
- [ ] Coalesce partitions works automatically

## Cleanup

```python
# Stop Spark session
spark.stop()

# Stop Docker containers
docker-compose down
```

## Troubleshooting

### Issue: Query is slow despite optimization
**Solution**: Check Spark UI for bottlenecks, consider caching intermediate results

### Issue: Out of memory errors
**Solution**: Increase memory allocation, reduce shuffle partitions, use AQE

### Issue: Data skew causing slow joins
**Solution**: Use salting technique or AQE skew join optimization

## Expected Outcomes

By the end of this lab, you should:
- Be comfortable writing Spark SQL queries
- Understand the Catalyst optimizer
- Be able to analyze execution plans
- Know how to optimize queries using hints
- Understand adaptive query execution
- Be able to monitor and tune performance

## Next Steps

- Chapter 5: Spark Streaming Fundamentals
- Chapter 6: Machine Learning with MLlib
- Chapter 7: Production Deployment

## Additional Resources

- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Performance Tuning Guide](https://spark.apache.org/docs/latest/tuning.html)
- [Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)