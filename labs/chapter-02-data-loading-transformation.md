# Chapter 2: Data Loading and Transformation

## Overview

This lab focuses on data loading from various sources and performing transformations in Apache Spark. Data loading and transformation are fundamental operations in any data pipeline, and Spark provides powerful APIs to handle these tasks efficiently at scale.

### Why Data Loading and Transformation Matter

In real-world data engineering, you'll work with data from diverse sources in various formats. Understanding how to:
- Load data efficiently from different sources (CSV, JSON, Parquet, Avro, databases)
- Handle different data formats and schemas
- Transform data to meet business requirements
- Optimize data loading for performance

These skills are essential for building robust data pipelines and data warehouses.

### Real-World Applications

- **Data Ingestion**: Loading data from APIs, databases, and file systems
- **ETL Pipelines**: Extract, transform, and load data for analytics
- **Data Cleaning**: Handling missing values, duplicates, and inconsistent data
- **Data Enrichment**: Joining data from multiple sources
- **Data Validation**: Ensuring data quality before analysis

## Learning Objectives

By the end of this lab, you will be able to:
- Load data from various file formats (CSV, JSON, Parquet, Avro)
- Read data from databases using JDBC
- Handle schema evolution and schema inference
- Perform data cleaning and validation
- Transform data using built-in functions
- Handle missing values and nulls
- Optimize data loading performance

## Prerequisites

- Completion of Chapter 1: Spark Fundamentals
- Understanding of Spark DataFrames
- Basic SQL knowledge
- Docker environment running

## Estimated Time

90-120 minutes

## Lab Environment

This lab uses the same Docker-based Spark environment as Chapter 1.

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
from pyspark.sql.functions import col, lit, when, coalesce, regexp_replace
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

spark = SparkSession.builder \
    .appName("DataLoadingTransformation") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()
```

## Exercise 1: Loading CSV Data

### Task

Load CSV data with various configurations and handle common CSV issues.

### Steps

1. **Create sample CSV files**

```python
# Create a complex CSV with different data types
csv_data = """id,name,age,salary,department,hire_date
1,Alice Johnson,28,75000,Engineering,2020-01-15
2,Bob Smith,35,85000,Marketing,2019-03-22
3,Charlie Brown,42,95000,Engineering,2018-06-10
4,Diana Prince,31,72000,Sales,2021-02-28
5,Eve Davis,29,68000,Marketing,2020-11-05
6,Frank Miller,38,90000,Engineering,2017-09-15
7,Grace Lee,26,65000,Sales,2022-04-10
8,Henry Wilson,33,78000,Marketing,2019-08-20
9,Ivy Chen,30,82000,Engineering,2020-05-18
10,Jack Turner,27,69000,Sales,2021-12-01"""

with open("/opt/spark/data/employees.csv", "w") as f:
    f.write(csv_data)
```

2. **Load CSV with different options**

```python
# Basic CSV loading
df_csv = spark.read.csv(
    "/opt/spark/data/employees.csv",
    header=True,
    inferSchema=True
)

df_csv.show()
df_csv.printSchema()
```

3. **Load CSV with explicit schema**

```python
# Define schema explicitly
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True),
    StructField("department", StringType(), True),
    StructField("hire_date", DateType(), True)
])

df_csv_schema = spark.read.csv(
    "/opt/spark/data/employees.csv",
    header=True,
    schema=schema
)

df_csv_schema.printSchema()
```

### Verification

- [ ] CSV files are created successfully
- [ ] Data is loaded with correct schema
- [ ] Custom delimiters work correctly

## Exercise 2: Loading JSON Data

### Task

Load JSON data and handle nested structures.

### Steps

1. **Create JSON files**

```python
# Simple JSON
json_simple = """[
    {"id": 1, "name": "Alice", "age": 28, "department": "Engineering"},
    {"id": 2, "name": "Bob", "age": 35, "department": "Marketing"},
    {"id": 3, "name": "Charlie", "age": 42, "department": "Engineering"}
]"""

with open("/opt/spark/data/employees_simple.json", "w") as f:
    f.write(json_simple)

# Nested JSON
json_nested = """[
    {
        "id": 1,
        "name": "Alice",
        "contact": {
            "email": "alice@example.com",
            "phone": "555-0100"
        },
        "skills": ["Python", "Spark", "SQL"]
    },
    {
        "id": 2,
        "name": "Bob",
        "contact": {
            "email": "bob@example.com",
            "phone": "555-0101"
        },
        "skills": ["Java", "Hadoop", "SQL"]
    }
]"""

with open("/opt/spark/data/employees_nested.json", "w") as f:
    f.write(json_nested)
```

2. **Load simple JSON**

```python
df_json_simple = spark.read.json("/opt/spark/data/employees_simple.json")
df_json_simple.show()
df_json_simple.printSchema()
```

3. **Load and flatten nested JSON**

```python
df_json_nested = spark.read.json("/opt/spark/data/employees_nested.json")
df_json_nested.show()
df_json_nested.printSchema()

# Flatten nested structure
from pyspark.sql.functions import col

df_flattened = df_json_nested.select(
    col("id"),
    col("name"),
    col("contact.email").alias("email"),
    col("contact.phone").alias("phone"),
    col("skills")
)

df_flattened.show()
```

### Verification

- [ ] JSON files are created successfully
- [ ] Nested structures are handled correctly
- [ ] Array explosion works as expected

## Exercise 3: Data Cleaning and Validation

### Task

Clean and validate data to ensure quality.

### Steps

1. **Handle missing values**

```python
# Create data with missing values
data_with_nulls = [
    (1, "Alice", 28, 75000, "Engineering"),
    (2, "Bob", None, 85000, "Marketing"),
    (3, None, 42, 95000, "Engineering"),
    (4, "Diana", 31, None, "Sales"),
    (5, "Eve", 29, 68000, None)
]

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True),
    StructField("department", StringType(), True)
])

df_nulls = spark.createDataFrame(data_with_nulls, schema)
df_nulls.show()
```

2. **Drop rows with nulls**

```python
# Drop any row with nulls
df_no_nulls = df_nulls.na.drop()
df_no_nulls.show()

# Drop rows where specific columns are null
df_no_nulls_subset = df_nulls.na.drop(subset=["name", "department"])
df_no_nulls_subset.show()
```

3. **Fill missing values**

```python
# Fill all nulls with default value
df_filled = df_nulls.na.fill("Unknown")
df_filled.show()

# Fill specific columns
df_filled_specific = df_nulls.na.fill({
    "name": "Unknown",
    "age": 0,
    "salary": 0,
    "department": "Unassigned"
})
df_filled_specific.show()
```

### Verification

- [ ] Missing values are handled correctly
- [ ] Null filling works as expected
- [ ] Duplicates are removed successfully

## Exercise 4: Data Transformation

### Task

Transform data using various built-in functions.

### Steps

1. **String transformations**

```python
# Create sample data
data_string = [
    ("alice johnson", "alice@example.com"),
    ("bob smith", "bob.smith@example.com"),
    ("charlie brown", "charlie_brown@example.com")
]

schema_string = StructType([
    StructField("name", StringType(), True),
    StructField("email", StringType(), True)
])

df_string = spark.createDataFrame(data_string, schema_string)
df_string.show()

# Transformations
from pyspark.sql.functions import upper, lower, trim, split, regexp_replace

df_transformed = df_string.select(
    upper(col("name")).alias("name_upper"),
    lower(col("name")).alias("name_lower"),
    trim(col("name")).alias("name_trimmed"),
    split(col("name"), " ")[0].alias("first_name"),
    regexp_replace(col("email"), "@example.com", "").alias("username")
)

df_transformed.show()
```

2. **Numeric transformations**

```python
from pyspark.sql.functions import round, abs, pow, floor, ceil

df_numeric = df_csv.select(
    col("salary"),
    round(col("salary") / 12, 2).alias("monthly_salary"),
    (col("salary") * 0.1).alias("bonus"),
    abs(col("age") - 30).alias("age_diff_from_30"),
    pow(col("age"), 2).alias("age_squared"),
    floor(col("salary") / 1000).alias("salary_thousands"),
    ceil(col("salary") / 1000).alias("salary_thousands_ceil")
)

df_numeric.show()
```

3. **Conditional transformations**

```python
df_conditional = df_csv.select(
    col("name"),
    col("salary"),
    when(col("salary") > 80000, "High")
    .when(col("salary") > 70000, "Medium")
    .otherwise("Low")
    .alias("salary_level"),
    
    when(col("department") == "Engineering", "Tech")
    .otherwise("Non-Tech")
    .alias("dept_category")
)

df_conditional.show()
```

### Verification

- [ ] String transformations work correctly
- [ ] Numeric calculations are accurate
- [ ] Date operations produce correct results
- [ ] Conditional logic works as expected

## Exercise 5: Data Aggregation and Grouping

### Task

Perform aggregations and grouping operations.

### Steps

1. **Basic aggregations**

```python
from pyspark.sql.functions import sum, avg, count, min, max

df_aggregation = df_csv.agg(
    count("*").alias("total_employees"),
    avg("salary").alias("avg_salary"),
    sum("salary").alias("total_salary"),
    min("salary").alias("min_salary"),
    max("salary").alias("max_salary")
)

df_aggregation.show()
```

2. **Group by aggregations**

```python
df_grouped = df_csv.groupBy("department").agg(
    count("*").alias("employee_count"),
    avg("salary").alias("avg_salary"),
    min("age").alias("min_age"),
    max("age").alias("max_age")
)

df_grouped.show()
```

3. **Multiple group by**

```python
# Add a new column for grouping
df_with_year = df_csv.withColumn("hire_year", year(col("hire_date")))

df_multi_group = df_with_year.groupBy("department", "hire_year").agg(
    count("*").alias("employee_count"),
    avg("salary").alias("avg_salary")
)

df_multi_group.orderBy("department", "hire_year").show()
```

### Verification

- [ ] Basic aggregations produce correct results
- [ ] Group by operations work correctly
- [ ] Multiple group by functions as expected

## Cleanup

```python
# Stop Spark session
spark.stop()

# Stop Docker containers
docker-compose down
```

## Troubleshooting

### Issue: Schema inference fails
**Solution**: Define schema explicitly using StructType

### Issue: Out of memory when loading large files
**Solution**: Use partitioning and increase memory allocation

### Issue: Date parsing errors
**Solution**: Use explicit date format with `dateFormat` option

## Expected Outcomes

By the end of this lab, you should:
- Be able to load data from various formats
- Handle different data types and schemas
- Clean and validate data effectively
- Transform data using built-in functions
- Perform aggregations and grouping
- Understand performance considerations

## Next Steps

- Chapter 3: Advanced DataFrame Operations
- Chapter 4: Spark SQL and Optimization
- Chapter 5: Spark Streaming Fundamentals

## Additional Resources

- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Data Sources Documentation](https://spark.apache.org/docs/latest/sql-data-sources.html)
- [Built-in Functions](https://spark.apache.org/docs/latest/api/sql/)