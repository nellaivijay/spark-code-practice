# Lab 2: Data Loading & Transformation - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 2: Data Loading & Transformation.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Spark environment set up (run `./scripts/setup.sh`)
- Jupyter Notebook accessible at http://localhost:8888
- Completion of Lab 1: Spark Fundamentals

## Setup Instructions

### 1. Start the Environment
```bash
cd spark-code-practice
./scripts/start.sh
```

### 2. Open Jupyter Notebook
- Navigate to http://localhost:8888 in your browser
- Open `notebooks/chapter-02-data-loading-transformation.ipynb`

## Lab Walkthrough

### Section A: Loading CSV Data

#### Step 1: Import Required Libraries
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when, coalesce, regexp_replace, upper, lower, trim
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
```

**Explanation**: Import PySpark libraries for data loading, transformations, and type definitions.

#### Step 2: Create SparkSession
```python
spark = SparkSession.builder \
    .appName("DataLoadingTransformation") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print(f"Spark master: {spark.conf.get('spark.master')}")
```

**Expected Output**: 
```
Spark version: 3.5.0
Spark master: spark://spark-master:7077
```

#### Step 3: Load CSV with Schema Inference
```python
df_csv = spark.read.csv("data/sample/employees.csv", header=True, inferSchema=True)

print("CSV loaded with schema inference:")
df_csv.printSchema()
df_csv.show()
```

**Explanation**: Spark automatically infers the schema by reading a sample of the data. This is convenient but can be slower for large files.

**Expected Output**: Schema showing inferred types and table with employee data.

#### Step 4: Load CSV with Explicit Schema
```python
explicit_schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("department", StringType(), True),
    StructField("salary", DoubleType(), True)
])

df_csv_explicit = spark.read.csv("data/sample/employees.csv", header=True, schema=explicit_schema)

print("CSV loaded with explicit schema:")
df_csv_explicit.printSchema()
```

**Key Concept**: Explicit schema definition gives you control over data types and avoids the overhead of schema inference.

### Section B: Loading JSON Data

#### Step 5: Load JSON Data
```python
df_json = spark.read.json("data/sample/employees.json")

print("JSON data loaded:")
df_json.printSchema()
df_json.show(truncate=False)
```

**Explanation**: JSON is semi-structured and can handle nested data. Spark automatically infers the schema including nested structures.

#### Step 6: Handle Nested Arrays in JSON
```python
from pyspark.sql.functions import explode

df_exploded = df_json.withColumn("skill", explode(col("skills")))
df_exploded.select("name", "skill").show()
```

**Key Concept**: The `explode` function flattens nested arrays, creating one row per array element.

**Practice**: Try different JSON structures and observe how Spark handles them.

### Section C: Loading Parquet Data

#### Step 7: Write Data to Parquet First
```python
df_csv.write.mode("overwrite").parquet("data/parquet/employees.parquet")
```

**Explanation**: Parquet is a columnar storage format optimized for Spark workloads with better compression and query performance.

#### Step 8: Load Parquet Data
```python
df_parquet = spark.read.parquet("data/parquet/employees.parquet")

print("Parquet data loaded:")
df_parquet.printSchema()
df_parquet.show()
```

**Practice**: Compare the file sizes and read performance between CSV, JSON, and Parquet formats.

### Section D: Data Cleaning and Validation

#### Step 9: Create DataFrame with Null Values
```python
data_with_nulls = [
    ("Alice", 25, "Engineering", 75000),
    ("Bob", None, "Marketing", None),
    ("Charlie", 35, None, 85000),
    (None, 28, "Sales", 60000),
    ("Eve", 32, "Marketing", 70000)
]

df_nulls = spark.createDataFrame(data_with_nulls, ["name", "age", "department", "salary"])
print("DataFrame with null values:")
df_nulls.show()
```

**Explanation**: Real-world data often contains null values that need to be handled properly.

#### Step 10: Drop Rows with Null Values
```python
df_no_nulls = df_nulls.na.drop()
print("Drop rows with any nulls:")
df_no_nulls.show()
```

**Key Concept**: `na.drop()` removes rows containing any null values. Use `how='all'` to drop only rows where all values are null.

#### Step 11: Fill Null Values with Defaults
```python
df_filled = df_nulls.na.fill({"age": 0, "salary": 50000, "department": "Unknown", "name": "Anonymous"})
print("\nFill null values with defaults:")
df_filled.show()
```

**Key Concept**: `na.fill()` replaces null values with specified defaults. Use different strategies for different columns based on business logic.

#### Step 12: Use Coalesce for Conditional Null Handling
```python
df_coalesce = df_nulls.withColumn(
    "clean_salary",
    coalesce(col("salary"), lit(50000))
)
print("Using coalesce for conditional null handling:")
df_coalesce.show()
```

**Key Concept**: `coalesce()` returns the first non-null value, useful for conditional logic in transformations.

### Section E: Data Transformation

#### Step 13: String Transformations
```python
df_string = df_csv.withColumn("name_upper", upper(col("name"))) \
                   .withColumn("name_lower", lower(col("name"))) \
                   .withColumn("name_trimmed", trim(col("name")))

print("String transformations:")
df_string.select("name", "name_upper", "name_lower", "name_trimmed").show()
```

**Practice**: Try other string functions like `substring`, `concat`, and `length`.

#### Step 14: Numeric Transformations
```python
df_numeric = df_csv.withColumn("salary_annual", col("salary") * 12) \
                   .withColumn("salary_with_bonus", col("salary") * 1.10) \
                   .withColumn("age_squared", col("age") ** 2)

print("Numeric transformations:")
df_numeric.select("name", "salary", "salary_annual", "salary_with_bonus", "age_squared").show()
```

**Practice**: Calculate additional metrics like salary per year of experience or age-based categories.

#### Step 15: Regular Expression Replacements
```python
messy_data = [("Alice-123", "Engineering"), ("Bob_456", "Marketing"), ("Charlie 789", "Sales")]
df_messy = spark.createDataFrame(messy_data, ["name_id", "department"])

# Remove digits from name
df_clean = df_messy.withColumn("name_clean", regexp_replace(col("name_id"), "\\d", "")) \
                      .withColumn("name_clean", regexp_replace(col("name_clean"), "[-_]", " "))

print("Regular expression cleaning:")
df_clean.show()
```

**Key Concept**: Regular expressions are powerful for cleaning messy text data. Use them for pattern matching and replacement.

### Section F: Data Validation

#### Step 16: Check for Null Values
```python
print("Data validation checks:")

print(f"\nNull values per column:")
for column in df_csv.columns:
    null_count = df_csv.filter(col(column).isNull()).count()
    print(f"{column}: {null_count}")
```

**Practice**: Create a function that generates a data quality report with various validation checks.

#### Step 17: Check for Duplicates
```python
total_rows = df_csv.count()
distinct_rows = df_csv.distinct().count()
print(f"\nTotal rows: {total_rows}")
print(f"Distinct rows: {distinct_rows}")
print(f"Duplicates: {total_rows - distinct_rows}")
```

**Practice**: Use `dropDuplicates()` to remove duplicate rows based on specific columns.

#### Step 18: Filter Invalid Data
```python
df_valid = df_csv.filter((col("age") > 0) & (col("age") < 100))
df_valid = df_valid.filter(col("salary") > 0)

print(f"Original rows: {df_csv.count()}")
print(f"Valid rows: {df_valid.count()}")
```

**Key Concept**: Always validate data ranges and business rules. Invalid data can skew analysis results.

### Section G: Writing Data

#### Step 19: Write to Different Formats
```python
df_valid.write.mode("overwrite").csv("data/csv/employees_clean.csv")
df_valid.write.mode("overwrite").json("data/json/employees_clean.json")
df_valid.write.mode("overwrite").parquet("data/parquet/employees_clean.parquet")

print("Data written to CSV, JSON, and Parquet formats")
```

**Practice**: Compare the file sizes of different formats. Parquet should be significantly smaller due to compression.

#### Step 20: Demonstrate Different Write Modes
```python
# Append mode
df_valid.write.mode("append").parquet("data/parquet/employees_append.parquet")

# Ignore mode (don't write if data exists)
df_valid.write.mode("ignore").parquet("data/parquet/employees_append.parquet")

# Error if exists mode
try:
    df_valid.write.mode("errorifexists").parquet("data/parquet/employees_append.parquet")
except Exception as e:
    print(f"Expected error with errorifexists mode: {type(e).__name__}")

print("\nWrite modes demonstrated")
```

**Key Concept**: Write modes control how Spark handles existing data:
- `overwrite`: Replace existing data
- `append`: Add to existing data
- `ignore`: Skip write if data exists
- `errorifexists`: Fail if data exists

### Section H: Partitioning Data

#### Step 21: Write Partitioned by Department
```python
df_valid.write.mode("overwrite") \
       .partitionBy("department") \
       .parquet("data/parquet/employees_partitioned")

print("Data partitioned by department")

df_partitioned = spark.read.parquet("data/parquet/employees_partitioned")
print(f"\nPartitioned data rows: {df_partitioned.count()}")
df_partitioned.show()
```

**Key Concept**: Partitioning improves query performance by organizing data on disk based on column values. Queries filtering on partition columns can skip reading irrelevant data.

**Practice**: Try partitioning by different columns and observe the directory structure created.

## Troubleshooting Tips

### Issue: Schema Inference Fails
**Solution**: Use explicit schema definition or increase the sampling size with `option("samplingRatio", "1.0")`.

### Issue: JSON Parsing Errors
**Solution**: Enable multi-line mode with `option("multiLine", "true")` for complex JSON structures.

### Issue: Parquet Schema Mismatch
**Solution**: Use `mergeSchema` option when reading: `spark.read.option("mergeSchema", "true").parquet(...)`.

### Issue: Out of Memory During Write
**Solution**: Increase executor memory or reduce partition count with `coalesce()` before writing.

### Issue: Slow Performance on Large Files
**Solution**: Use Parquet format with appropriate partitioning and compression settings.

## Check Your Understanding

1. What are the advantages of using explicit schema over schema inference?
2. How does the `explode` function handle nested arrays in JSON?
3. What is the difference between `na.drop()` and `na.fill()`?
4. Why is Parquet format preferred over CSV for Spark workloads?
5. How does data partitioning improve query performance?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-02-data-loading-transformation-solution.ipynb`
4. Proceed to Lab 3: Advanced DataFrame Operations

## Additional Resources

- [Spark Data Sources Documentation](https://spark.apache.org/docs/latest/sql-data-sources.html)
- [PySpark Functions Reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Data Loading Cheatsheet](cheatsheets/dataframe-api-cheatsheet.ipynb)
- [Data Format Comparison](https://databricks.com/blog/2017/02/23/working-with-apache-parquet-files-in-spark.html)
