# Lab 4: Spark SQL & Optimization - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 4: Spark SQL & Optimization.

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
- Open `notebooks/chapter-04-spark-sql-optimization.ipynb`

## Lab Walkthrough

### Section A: Creating Sample Data for SQL Operations

#### Step 1: Import Required Libraries
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, max, min, when, lit
from pyspark.sql.functions import broadcast
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
```

**Explanation**: Import PySpark libraries for SQL operations and optimization techniques.

#### Step 2: Create SparkSession with Optimization Configurations
```python
spark = SparkSession.builder \
    .appName("SparkSQLOptimization") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print(f"AQE enabled: {spark.conf.get('spark.sql.adaptive.enabled')}")
```

**Key Concept**: Enable Adaptive Query Execution (AQE) for runtime optimization based on actual data statistics.

**Expected Output**: 
```
Spark version: 3.5.0
AQE enabled: true
```

#### Step 3: Create Sample Data
```python
# Create employees data
employees_data = [
    (1, "Alice Johnson", 28, 75000, 101, "Engineering"),
    (2, "Bob Smith", 35, 85000, 102, "Marketing"),
    (3, "Charlie Brown", 42, 95000, 101, "Engineering"),
    (4, "Diana Prince", 31, 80000, 103, "Sales"),
    (5, "Eve Williams", 29, 72000, 102, "Marketing"),
    (6, "Frank Davis", 38, 88000, 101, "Engineering"),
    (7, "Grace Miller", 33, 78000, 103, "Sales"),
    (8, "Henry Wilson", 45, 105000, 104, "Executive"),
    (9, "Ivy Chen", 27, 68000, 102, "Marketing"),
    (10, "Jack Taylor", 40, 92000, 101, "Engineering")
]

df_employees = spark.createDataFrame(employees_data, 
    ["id", "name", "age", "salary", "dept_id", "department"])
df_employees.createOrReplaceTempView("employees")

# Create departments data
departments_data = [
    (101, "Engineering", "Building A", 500000),
    (102, "Marketing", "Building B", 300000),
    (103, "Sales", "Building C", 400000),
    (104, "Executive", "Building D", 200000)
]

df_departments = spark.createDataFrame(departments_data,
    ["dept_id", "dept_name", "location", "budget"])
df_departments.createOrReplaceTempView("departments")

# Create sales data
sales_data = [
    ("2024-01-01", "Product A", "Electronics", 5, 500.00),
    ("2024-01-01", "Product B", "Electronics", 3, 300.00),
    ("2024-01-02", "Product C", "Furniture", 2, 400.00),
    ("2024-01-02", "Product D", "Furniture", 4, 800.00),
    ("2024-01-03", "Product A", "Electronics", 6, 600.00),
    ("2024-01-03", "Product E", "Office", 10, 200.00),
    ("2024-01-04", "Product B", "Electronics", 2, 200.00),
    ("2024-01-04", "Product C", "Furniture", 3, 600.00)
]

df_sales = spark.createDataFrame(sales_data,
    ["date", "product", "category", "quantity", "revenue"])
df_sales.createOrReplaceTempView("sales")

print("Sample data created and registered as temp views")
df_employees.show(5)
df_departments.show()
df_sales.show(5)
```

**Explanation**: Create comprehensive sample data for employees, departments, and sales, and register them as temporary views for SQL operations.

### Section B: Basic SQL Operations

#### Step 4: SELECT with Filtering
```python
print("Employees with salary > 80000:")
spark.sql("""
    SELECT name, salary 
    FROM employees 
    WHERE salary > 80000
    ORDER BY salary DESC
""").show()

print("\nEngineering employees aged 30-40:")
spark.sql("""
    SELECT name, age, department
    FROM employees
    WHERE department = 'Engineering' 
      AND age BETWEEN 30 AND 40
""").show()
```

**Practice**: Try different filter conditions and operators (IN, LIKE, IS NULL).

#### Step 5: Aggregations
```python
print("Average salary by department:")
spark.sql("""
    SELECT department, 
           COUNT(*) as employee_count,
           AVG(salary) as avg_salary,
           SUM(salary) as total_salary,
           MAX(salary) as max_salary,
           MIN(salary) as min_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""").show()

print("\nDepartments with average salary > 75000:")
spark.sql("""
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    HAVING AVG(salary) > 75000
""").show()
```

**Key Concept**: HAVING filters aggregated results, while WHERE filters individual rows.

### Section C: Advanced SQL Features

#### Step 6: Common Table Expression (CTE)
```python
print("Using CTE for department statistics:")
spark.sql("""
    WITH dept_stats AS (
        SELECT department, 
               AVG(salary) as avg_salary,
               COUNT(*) as emp_count
        FROM employees
        GROUP BY department
    )
    SELECT e.name, e.salary, d.avg_salary, d.emp_count
    FROM employees e
    JOIN dept_stats d ON e.department = d.department
    WHERE e.salary > d.avg_salary
    ORDER BY e.salary DESC
""").show()
```

**Key Concept**: CTEs improve query readability and allow you to reuse subqueries. They're often more readable than nested subqueries.

#### Step 7: CASE Statement
```python
print("Salary categorization:")
spark.sql("""
    SELECT name, salary,
           CASE 
               WHEN salary < 70000 THEN 'Junior'
               WHEN salary < 90000 THEN 'Mid-Level'
               ELSE 'Senior'
           END as salary_level
    FROM employees
    ORDER BY salary DESC
""").show()
```

**Practice**: Use CASE for conditional logic, data categorization, and handling null values.

#### Step 8: Window Functions in SQL
```python
print("Employee ranking within department:")
spark.sql("""
    SELECT name, department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank_num,
           DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dense_rank
    FROM employees
    ORDER BY department, salary DESC
""").show()
```

**Key Concept**: Window functions in SQL use the same syntax as DataFrame API but with SQL syntax.

### Section D: Query Execution Plans

#### Step 9: Simple Query Plan
```python
print("Simple query plan:")
spark.sql("SELECT * FROM employees WHERE salary > 80000").explain()
```

**Key Concept**: The `explain()` method shows the physical execution plan. Look for operations like Filter, Scan, and Exchange.

#### Step 10: Complex Query Plan with Join
```python
print("\nComplex query plan with join:")
complex_query = spark.sql("""
    SELECT e.name, e.salary, d.dept_name, d.location
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
    WHERE e.salary > 75000
    ORDER BY e.salary DESC
""")
complex_query.explain()
```

**Practice**: Identify the join strategy (SortMergeJoin, BroadcastHashJoin, etc.) in the plan.

#### Step 11: Extended Explain
```python
print("Extended query plan:")
complex_query.explain(extended=True)
```

**Key Concept**: Extended explain shows both logical and physical plans, providing more insight into the optimization process.

### Section E: Query Hints

#### Step 12: Broadcast Join Hint
```python
print("Broadcast join hint:")
broadcast_query = spark.sql("""
    SELECT /*+ BROADCAST(d) */ e.name, e.salary, d.dept_name
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
""")
broadcast_query.explain()
broadcast_query.show()
```

**Key Concept**: Query hints manually guide the optimizer. Use `/*+ BROADCAST(table) */` to force a broadcast join.

#### Step 13: Repartition Hint
```python
print("Repartition hint:")
repartition_query = spark.sql("""
    SELECT /*+ REPARTITION(10) */ * FROM employees
""")
repartition_query.explain()
```

**Practice**: Try other hints like `COALESCE`, `REPARTITION_BY_RANGE`, and `SHUFFLE_HASH`.

### Section F: Performance Optimization Techniques

#### Step 14: Predicate Pushdown
```python
print("Predicate pushdown optimization:")

# Bad: Filter after join
bad_query = spark.sql("""
    SELECT e.name, e.salary
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
    WHERE e.salary > 80000
""")

# Good: Filter before join
good_query = spark.sql("""
    SELECT e.name, e.salary
    FROM (SELECT * FROM employees WHERE salary > 80000) e
    JOIN departments d ON e.dept_id = d.dept_id
""")

print("Bad query plan:")
bad_query.explain()
print("\nGood query plan:")
good_query.explain()
```

**Key Concept**: Predicate pushdown moves filters closer to the data source, reducing the amount of data processed.

#### Step 15: Column Pruning
```python
print("Column pruning optimization:")

# Bad: SELECT *
bad_query = spark.sql("SELECT * FROM employees")

# Good: SELECT specific columns
good_query = spark.sql("SELECT name, salary FROM employees")

print("Bad query plan:")
bad_query.explain()
print("\nGood query plan:")
good_query.explain()
```

**Key Concept**: Column pruning selects only needed columns, reducing data transfer and memory usage.

#### Step 16: Caching
```python
print("Caching optimization:")

# Cache the employees DataFrame
spark.sql("CACHE TABLE employees")

# Check cached tables
print("\nCached tables:")
spark.sql("SHOW TABLES").show()

# Run query on cached table
spark.sql("SELECT COUNT(*) FROM employees").show()

# Uncache when done
spark.sql("UNCACHE TABLE employees")
print("\nTable uncached")
```

**Key Concept**: Caching stores frequently used DataFrames in memory for faster access. Use for tables queried multiple times.

### Section G: Adaptive Query Execution (AQE)

#### Step 17: Check AQE Configuration
```python
print("AQE Configuration:")
print(f"AQE enabled: {spark.conf.get('spark.sql.adaptive.enabled')}")
print(f"Coalesce partitions: {spark.conf.get('spark.sql.adaptive.coalescePartitions.enabled')}")
print(f"Skew join optimization: {spark.conf.get('spark.sql.adaptive.skewJoin.enabled')}")
```

**Key Concept**: AQE features:
- Coalesce partitions: Reduces number of partitions after shuffle
- Skew join optimization: Handles data skew in joins
- Dynamic coalescing: Adjusts partition count based on data size

#### Step 18: Demonstrate AQE Benefits
```python
# Create skewed data
skewed_data = [(i, f"product_{i}", i % 5, 100.0 * (i % 10 + 1)) for i in range(1000)]
df_skewed = spark.createDataFrame(skewed_data, ["id", "name", "category", "price"])
df_skewed.createOrReplaceTempView("skewed_products")

# Query that benefits from AQE
aqe_query = spark.sql("""
    SELECT category, AVG(price) as avg_price
    FROM skewed_products
    GROUP BY category
""")

print("AQE optimized query:")
aqe_query.explain()
aqe_query.show()
```

**Practice**: Compare query execution with AQE enabled vs disabled using `spark.conf.set("spark.sql.adaptive.enabled", "false")`.

### Section H: Catalog Operations

#### Step 19: List Databases and Tables
```python
print("Databases:")
spark.sql("SHOW DATABASES").show()

print("\nCurrent database:")
spark.sql("SELECT current_database()").show()

print("\nTables in current database:")
spark.sql("SHOW TABLES").show()
```

**Key Concept**: Catalog operations help you manage databases, tables, and views in Spark SQL.

#### Step 20: Describe Table
```python
print("Table structure:")
spark.sql("DESCRIBE employees").show()

# Drop temp view
spark.sql("DROP VIEW IF EXISTS skewed_products")
print("\nTemp view dropped")
```

**Practice**: Use catalog operations to explore your data structures and manage temporary views.

## Troubleshooting Tips

### Issue: Query Performance is Poor
**Solution**:
- Use `explain()` to analyze the query plan
- Apply predicate pushdown and column pruning
- Cache frequently used tables
- Consider query hints for specific optimizations
- Enable and tune AQE settings

### Issue: Broadcast Join Not Used
**Solution**:
- Check if the table size is below `spark.sql.autoBroadcastJoinThreshold`
- Use `/*+ BROADCAST(table) */` hint to force broadcast
- Increase the broadcast threshold configuration

### Issue: Out of Memory During Query
**Solution**:
- Reduce executor memory requirements with better queries
- Use AQE to coalesce partitions
- Increase executor memory configuration
- Cache data selectively

### Issue: AQE Not Optimizing
**Solution**:
- Verify AQE is enabled in configuration
- Check Spark version (AQE requires Spark 3.0+)
- Review AQE-specific configurations
- Monitor query execution in Spark UI

### Issue: Complex Query Plan
**Solution**:
- Break down complex queries into simpler steps
- Use CTEs for better readability and optimization
- Consider materializing intermediate results
- Use query hints to guide the optimizer

## Check Your Understanding

1. What is the purpose of the Catalyst optimizer in Spark SQL?
2. How does Adaptive Query Execution (AQE) improve performance?
3. When should you use query hints?
4. What is predicate pushdown and why is it important?
5. How does caching improve query performance?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-04-spark-sql-optimization-solution.ipynb`
4. Proceed to Lab 5: Spark Streaming Fundamentals

## Additional Resources

- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Catalyst Optimizer Documentation](https://databricks.com/glossary/what-is-catalyst-optimizer)
- [AQE Documentation](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)
- [Query Hints Reference](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html)
- [Spark SQL Cheatsheet](cheatsheets/spark-sql-cheatsheet.ipynb)
