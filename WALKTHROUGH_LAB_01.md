# Lab 1: Spark Fundamentals - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 1: Spark Fundamentals.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Spark environment set up (run `./scripts/setup.sh`)
- Jupyter Notebook accessible at http://localhost:8888

## Setup Instructions

### 1. Start the Environment
```bash
cd spark-code-practice
./scripts/start.sh
```

### 2. Open Jupyter Notebook
- Navigate to http://localhost:8888 in your browser
- Open `notebooks/chapter-01-spark-fundamentals.ipynb`

## Lab Walkthrough

### Section A: SparkSession Setup

#### Step 1: Import Libraries
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
```

**Explanation**: Import the required PySpark libraries for DataFrame operations and type definitions.

#### Step 2: Create SparkSession
```python
spark = SparkSession.builder \
    .appName("SparkFundamentals") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.executor.cores", "1") \
    .getOrCreate()
```

**Explanation**: Creates a SparkSession connected to the Spark master. The configuration sets executor memory and cores.

**Expected Output**: 
```
Spark version: 3.5.0
Spark master: spark://spark-master:7077
App name: SparkFundamentals
```

### Section B: Creating DataFrames

#### Step 3: Create Sample Data
```python
data = [
    ("Alice", 25, "Engineering", 75000),
    ("Bob", 30, "Marketing", 65000),
    ("Charlie", 35, "Engineering", 85000),
    ("Diana", 28, "Sales", 60000),
    ("Eve", 32, "Marketing", 70000)
]

columns = ["name", "age", "department", "salary"]
df = spark.createDataFrame(data, columns)
df.show()
```

**Explanation**: Creates a DataFrame from Python data. The DataFrame represents distributed data organized into named columns.

**Expected Output**: A table showing the employee data with 5 rows.

### Section C: Understanding Transformations vs Actions

#### Step 4: Transformations (Lazy)
```python
filtered_df = df.filter(col("age") > 30)
selected_df = df.select("name", "department")
```

**Key Concept**: Transformations are lazy - they don't execute immediately but build up a computation plan.

#### Step 5: Actions (Eager)
```python
df.count()  # Triggers execution
df.show()   # Triggers execution
```

**Key Concept**: Actions trigger actual computation and return results.

### Section D: Basic DataFrame Operations

#### Step 6: Filter Operations
```python
df.filter(col("age") > 30).show()
df.filter(col("department") == "Engineering").show()
```

**Practice**: Try different filter conditions and observe the results.

#### Step 7: Select Operations
```python
df.select("name", "salary").show()
df.select(col("name"), col("salary") * 1.1).show()
```

**Practice**: Select specific columns and perform calculations.

### Section E: Spark SQL Operations

#### Step 8: Register DataFrame as Temp View
```python
df.createOrReplaceTempView("employees")
```

**Explanation**: Registers the DataFrame as a temporary view for SQL queries.

#### Step 9: Run SQL Queries
```python
spark.sql("SELECT * FROM employees").show()
spark.sql("""
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""").show()
```

**Practice**: Write your own SQL queries to explore the data.

### Section F: Reading and Writing Data

#### Step 10: Write to Different Formats
```python
df.write.mode("overwrite").csv("data/csv/employees.csv")
df.write.mode("overwrite").json("data/json/employees.json")
df.write.mode("overwrite").parquet("data/parquet/employees.parquet")
```

**Explanation**: Writes the DataFrame to different file formats for persistence.

#### Step 11: Read Back Data
```python
df_csv = spark.read.csv("data/csv/employees.csv", header=True, inferSchema=True)
df_parquet = spark.read.parquet("data/parquet/employees.parquet")
```

**Practice**: Compare the performance of reading different formats.

### Section G: Navigating the Spark UI

#### Step 12: Access Spark UI
- Open http://localhost:4040 in your browser
- Explore the different tabs: Jobs, Stages, Storage, Environment, Executors, SQL

#### Step 13: Trigger a Job and Observe
```python
complex_query = df.filter(col("age") > 25) \
    .filter(col("salary") > 65000) \
    .groupBy("department") \
    .agg(count("*").alias("employee_count")) \
    .orderBy(col("employee_count").desc())

complex_query.show()
complex_query.explain()
```

**Practice**: Observe the job execution in the Spark UI and analyze the query plan.

## Troubleshooting Tips

### Issue: Spark Master Connection Failed
**Solution**: Ensure Docker containers are running with `docker-compose ps` and restart if needed.

### Issue: Out of Memory Errors
**Solution**: Reduce executor memory in SparkSession configuration or increase Docker memory limits.

### Issue: File Not Found Errors
**Solution**: Ensure data directories exist with proper permissions.

## Check Your Understanding

1. What is the difference between transformations and actions?
2. How do you register a DataFrame for SQL operations?
3. What are the benefits of using Parquet format over CSV?
4. How can you monitor Spark job execution?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-01-spark-fundamentals-solution.ipynb`
4. Proceed to Lab 2: Data Loading & Transformation

## Additional Resources

- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [DataFrame API Cheatsheet](cheatsheets/dataframe-api-cheatsheet.ipynb)
