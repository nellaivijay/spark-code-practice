# Lab 3: Advanced DataFrame Operations - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 3: Advanced DataFrame Operations.

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
- Open `notebooks/chapter-03-advanced-dataframe-operations.ipynb`

## Lab Walkthrough

### Section A: Creating Sample Data for Joins

#### Step 1: Import Required Libraries
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, max, min
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead
from pyspark.sql.functions import explode, array, struct, map_from_arrays, map_keys, map_values
from pyspark.sql.functions import udf, pandas_udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType
from pyspark.sql.types import MapType
from pyspark.sql.window import Window
import pandas as pd
```

**Explanation**: Import PySpark libraries for advanced operations including joins, window functions, complex data types, and UDFs.

#### Step 2: Create SparkSession
```python
spark = SparkSession.builder \
    .appName("AdvancedDataFrameOperations") \
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

#### Step 3: Create Employees DataFrame
```python
employees_data = [
    (1, "Alice", "Engineering", 75000),
    (2, "Bob", "Marketing", 65000),
    (3, "Charlie", "Engineering", 85000),
    (4, "Diana", "Sales", 60000),
    (5, "Eve", "Marketing", 70000),
    (6, "Frank", None, 55000)  # Employee without department
]

employees_df = spark.createDataFrame(employees_data, ["id", "name", "department", "salary"])
print("Employees DataFrame:")
employees_df.show()
```

**Explanation**: Creates an employees DataFrame with various departments and one employee (Frank) without a department for testing join behavior.

#### Step 4: Create Departments DataFrame
```python
departments_data = [
    ("Engineering", "Building A", 100),
    ("Marketing", "Building B", 50),
    ("Sales", "Building C", 75),
    ("HR", "Building D", 25),  # Department without employees
    ("Finance", "Building E", 30)  # Department without employees
]

departments_df = spark.createDataFrame(departments_data, ["department", "location", "budget"])
print("Departments DataFrame:")
departments_df.show()
```

**Explanation**: Creates a departments DataFrame with HR and Finance having no employees to test outer join behavior.

### Section B: Inner Join

#### Step 5: Perform Inner Join
```python
inner_join = employees_df.join(departments_df, "department", "inner")

print("Inner Join (only matching departments):")
inner_join.show()

print(f"\nEmployees: {employees_df.count()}")
print(f"Departments: {departments_df.count()}")
print(f"Inner join result: {inner_join.count()}")
```

**Key Concept**: Inner join returns only rows where the join key exists in both DataFrames. Frank (no department) and HR/Finance (no employees) are excluded.

**Expected Output**: 4 rows (Alice, Bob, Charlie, Diana, Eve - but Frank excluded, HR/Finance excluded)

### Section C: Left Join

#### Step 6: Perform Left Join
```python
left_join = employees_df.join(departments_df, "department", "left")

print("Left Join (all employees, matching departments):")
left_join.show()

print(f"\nLeft join result: {left_join.count()}")
```

**Key Concept**: Left join returns all rows from the left DataFrame (employees) and matching rows from the right (departments). Frank will have null values for department columns.

**Expected Output**: 6 rows (all employees including Frank with nulls for location/budget)

### Section D: Right Join

#### Step 7: Perform Right Join
```python
right_join = employees_df.join(departments_df, "department", "right")

print("Right Join (all departments, matching employees):")
right_join.show()

print(f"\nRight join result: {right_join.count()}")
```

**Key Concept**: Right join returns all rows from the right DataFrame (departments) and matching rows from the left (employees). HR and Finance will have null values for employee columns.

**Expected Output**: 5 rows (all departments including HR/Finance with nulls for employee columns)

### Section E: Outer Join

#### Step 8: Perform Outer Join
```python
outer_join = employees_df.join(departments_df, "department", "outer")

print("Outer Join (all rows from both DataFrames):")
outer_join.show()

print(f"\nOuter join result: {outer_join.count()}")
```

**Key Concept**: Outer join (full outer join) returns all rows from both DataFrames, with nulls where there's no match. This is the most comprehensive join.

**Expected Output**: 7 rows (all employees and all departments, with nulls where unmatched)

### Section F: Left Semi Join

#### Step 9: Perform Left Semi Join
```python
left_semi_join = employees_df.join(departments_df, "department", "leftsemi")

print("Left Semi Join (employees with matching departments):")
left_semi_join.show()

print(f"\nLeft semi join result: {left_semi_join.count()}")
```

**Key Concept**: Left semi join filters the left DataFrame to keep only rows with matches in the right DataFrame. It doesn't include columns from the right DataFrame.

**Expected Output**: 5 rows (employees with matching departments, no department columns included)

### Section G: Left Anti Join

#### Step 10: Perform Left Anti Join
```python
left_anti_join = employees_df.join(departments_df, "department", "leftanti")

print("Left Anti Join (employees without matching departments):")
left_anti_join.show()

print(f"\nLeft anti join result: {left_anti_join.count()}")
```

**Key Concept**: Left anti join filters the left DataFrame to keep only rows without matches in the right DataFrame. Useful for finding orphaned records.

**Expected Output**: 1 row (Frank, who has no matching department)

### Section H: Window Functions

#### Step 11: Define Window Specification
```python
window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
```

**Explanation**: Window specification defines the scope of window functions. Here we partition by department and order by salary descending.

#### Step 12: Apply Ranking Functions
```python
employees_with_rank = employees_df.withColumn("row_num", row_number().over(window_spec)) \
                                  .withColumn("rank", rank().over(window_spec)) \
                                  .withColumn("dense_rank", dense_rank().over(window_spec))

print("Window Functions - Ranking:")
employees_with_rank.show()
```

**Key Concepts**:
- `row_number()`: Unique sequential numbers (1, 2, 3, ...) without gaps
- `rank()`: Ranking with gaps for ties (1, 2, 2, 4, ...)
- `dense_rank()`: Ranking without gaps for ties (1, 2, 2, 3, ...)

**Practice**: Observe the differences between the three ranking functions, especially when salaries are equal.

#### Step 13: Apply Lag/Lead Functions
```python
employees_with_lag = employees_df.withColumn("lag_salary", lag("salary", 1).over(window_spec)) \
                                  .withColumn("lead_salary", lead("salary", 1).over(window_spec))

print("Window Functions - Lag/Lead:")
employees_with_lag.show()
```

**Key Concepts**:
- `lag()`: Access value from previous row in window
- `lead()`: Access value from next row in window

**Practice**: Use lag/lead to calculate salary differences between consecutive employees.

#### Step 14: Apply Aggregate Window Functions
```python
window_agg_spec = Window.partitionBy("department")

employees_with_agg = employees_df.withColumn("dept_avg_salary", avg("salary").over(window_agg_spec)) \
                                 .withColumn("dept_total_salary", sum("salary").over(window_agg_spec)) \
                                 .withColumn("dept_max_salary", max("salary").over(window_agg_spec))

print("Window Functions - Aggregates:")
employees_with_agg.show()
```

**Key Concept**: Window aggregates allow you to add aggregate values to each row without reducing the row count, unlike regular groupBy operations.

### Section I: Complex Data Types

#### Step 15: Array Operations
```python
employees_with_skills = employees_df.withColumn("skills", array("Python", "Spark", "SQL"))

print("Array column added:")
employees_with_skills.select("name", "skills").show(truncate=False)

# Explode array to rows
exploded_skills = employees_with_skills.withColumn("skill", explode(col("skills")))

print("\nExploded array to rows:")
exploded_skills.select("name", "skill").show()
```

**Key Concept**: Arrays store multiple values in a single column. `explode()` converts arrays to rows, one row per array element.

**Practice**: Try array functions like `size()`, `array_contains()`, and `slice()`.

#### Step 16: Map Operations
```python
employees_with_map = employees_df.withColumn(
    "metadata",
    map_from_arrays(array("hire_date", "manager"), array("2020-01-01", "Alice"))
)

print("Map column added:")
employees_with_map.select("name", "metadata").show(truncate=False)

# Access map keys and values
map_ops = employees_with_map.withColumn("map_keys", map_keys(col("metadata"))) \
                              .withColumn("map_values", map_values(col("metadata")))

print("\nMap keys and values:")
map_ops.select("name", "map_keys", "map_values").show(truncate=False)
```

**Key Concept**: Maps store key-value pairs. Use `map_from_arrays()` to create maps from parallel arrays.

**Practice**: Access specific map values using `col("metadata")["hire_date"]`.

#### Step 17: Struct Operations
```python
employees_with_struct = employees_df.withColumn(
    "address",
    struct("name", "department").alias("address")
)

print("Struct column added:")
employees_with_struct.select("name", "address").show(truncate=False)

# Access struct fields
struct_ops = employees_with_struct.select(col("name"), col("address.department"))

print("\nAccess struct fields:")
struct_ops.show(truncate=False)
```

**Key Concept**: Structs group multiple fields into a single column. Access nested fields using dot notation.

**Practice**: Create more complex structs with multiple nested levels.

### Section J: User Defined Functions (UDFs)

#### Step 18: Create Python UDF
```python
def salary_category(salary):
    if salary < 60000:
        return "Low"
    elif salary < 80000:
        return "Medium"
    else:
        return "High"

# Register UDF
salary_category_udf = udf(salary_category, StringType())

# Apply UDF
employees_with_category = employees_df.withColumn(
    "salary_category",
    salary_category_udf(col("salary"))
)

print("Python UDF applied:")
employees_with_category.select("name", "salary", "salary_category").show()
```

**Key Concept**: UDFs allow custom transformations using Python functions. Note that Python UDFs can be slow due to serialization overhead.

#### Step 19: Create Pandas UDF
```python
@pandas_udf(DoubleType())
def calculate_bonus_pandas(salary: pd.Series) -> pd.Series:
    return salary * 0.10

# Apply Pandas UDF
employees_with_pandas_bonus = employees_df.withColumn(
    "bonus",
    calculate_bonus_pandas(col("salary"))
)

print("Pandas UDF applied:")
employees_with_pandas_bonus.select("name", "salary", "bonus").show()
```

**Key Concept**: Pandas UDFs use Apache Arrow for vectorized operations, providing much better performance than regular Python UDFs.

**Practice**: Compare performance between Python UDFs and Pandas UDFs on larger datasets.

### Section K: Join Performance Optimization

#### Step 20: Use Broadcast Join
```python
from pyspark.sql.functions import broadcast

# Broadcast join (for small tables)
broadcast_join = employees_df.join(broadcast(departments_df), "department")

print("Broadcast join completed:")
broadcast_join.show()

# Explain the plan to see broadcast
print("\nQuery plan (look for BroadcastHashJoin):")
broadcast_join.explain()
```

**Key Concept**: Broadcast joins send the smaller table to all executors, avoiding expensive shuffle operations. Use when one table is small enough to fit in memory.

**Practice**: Compare the query plans of regular join vs broadcast join using `explain()`.

## Troubleshooting Tips

### Issue: Join Performance is Slow
**Solution**: 
- Use broadcast joins for small tables
- Ensure join columns have the same data type
- Consider partitioning data before joining
- Use `spark.sql.autoBroadcastJoinThreshold` to control broadcast behavior

### Issue: Window Functions Out of Memory
**Solution**: 
- Reduce partition count with `repartition()`
- Use simpler window specifications
- Filter data before applying window functions

### Issue: UDF Performance Issues
**Solution**: 
- Use Pandas UDFs instead of Python UDFs
- Consider using built-in Spark functions instead of UDFs
- Cache data before applying UDFs

### Issue: Array/Map Operations Failing
**Solution**: 
- Ensure data types are correct (ArrayType, MapType)
- Use proper schema definitions
- Check for null values in complex columns

### Issue: Join Producing Unexpected Results
**Solution**: 
- Verify join keys match exactly
- Check for null values in join columns
- Use `explain()` to understand the join strategy
- Test with sample data first

## Check Your Understanding

1. What is the difference between left semi join and left anti join?
2. When would you use an outer join instead of an inner join?
3. How does `row_number()` differ from `rank()` and `dense_rank()`?
4. What are the performance implications of using Python UDFs vs Pandas UDFs?
5. When should you use a broadcast join?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-03-advanced-dataframe-operations-solution.ipynb`
4. Proceed to Lab 4: Spark SQL & Optimization

## Additional Resources

- [Spark Join Strategies](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-and-dataset-apis)
- [Window Functions Documentation](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/window.html)
- [Complex Types Documentation](https://spark.apache.org/docs/latest/sql-ref-datatypes.html)
- [UDF Performance Guide](https://databricks.com/blog/2017/10/31/introducing-vectorized-udfs-for-pyspark.html)
- [DataFrame API Cheatsheet](cheatsheets/dataframe-api-cheatsheet.ipynb)
