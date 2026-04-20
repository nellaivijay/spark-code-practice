# Additional Practice Exercises

This document contains additional practice exercises for each lab to reinforce learning.

## Lab 1: Spark Fundamentals - Practice Exercises

### Exercise 1.1: DataFrame Creation
**Task**: Create a DataFrame from the following data with explicit schema:
```python
data = [
    ("Product A", 100, 25.50),
    ("Product B", 200, 15.75),
    ("Product C", 150, 30.00),
    ("Product D", 75, 45.25)
]
```
Schema: product_name (String), quantity (Integer), price (Double)

**Challenge**: Calculate the total value for each product (quantity * price)

### Exercise 1.2: Spark SQL Operations
**Task**: Register the DataFrame as a temporary view and write SQL queries to:
1. Find products with quantity > 100
2. Calculate average price across all products
3. Find the most expensive product

### Exercise 1.3: Transformations vs Actions
**Task**: Given a DataFrame, identify which operations are transformations and which are actions:
- `df.filter(col("price") > 20)`
- `df.count()`
- `df.select("product_name")`
- `df.show()`
- `df.withColumn("discounted_price", col("price") * 0.9)`

### Exercise 1.4: Performance Analysis
**Task**: Create a DataFrame with 1 million rows and compare the performance of:
1. `filter()` followed by `count()`
2. `count()` on the filtered DataFrame
Use `time.time()` to measure execution time.

## Lab 2: Data Loading & Transformation - Practice Exercises

### Exercise 2.1: Multi-Format Loading
**Task**: Create sample data in CSV, JSON, and Parquet formats. Load each format and:
1. Compare schema inference vs explicit schema
2. Measure load time for each format
3. Compare file sizes

### Exercise 2.2: Advanced Data Cleaning
**Task**: Create a DataFrame with various data quality issues:
- Duplicate rows
- Null values in different columns
- Invalid data types
- Out of range values

Write a comprehensive cleaning pipeline that addresses all issues.

### Exercise 2.3: Complex Transformations
**Task**: Given sales data with columns: date, product, category, quantity, revenue
1. Add a column for revenue per unit
2. Add a column for month and year from date
3. Filter out sales with quantity < 0
4. Round revenue to 2 decimal places

### Exercise 2.4: Partitioning Strategies
**Task**: Write the same DataFrame to Parquet using different partitioning strategies:
1. Partition by category
2. Partition by year
3. Partition by category and year
Compare query performance for different filtering patterns.

## Lab 3: Advanced DataFrame Operations - Practice Exercises

### Exercise 3.1: Join Performance Comparison
**Task**: Create two DataFrames (1M rows and 100 rows). Compare performance of:
1. Regular join
2. Broadcast join
3. Different join types (inner, left, right, outer)

### Exercise 3.2: Advanced Window Functions
**Task**: Given sales data, use window functions to:
1. Calculate running total of revenue by date
2. Find top 3 products by revenue in each category
3. Calculate percentage of total revenue per product
4. Find products with revenue above category average

### Exercise 3.3: Complex Data Types
**Task**: Create a DataFrame with:
- Array column for product tags
- Map column for product attributes
- Struct column for product details

Perform operations:
1. Filter products by array contains
2. Extract specific map values
3. Access struct fields
4. Explode array to rows

### Exercise 3.4: UDF Performance
**Task**: Compare performance of:
1. Regular Python UDF
2. Pandas UDF (vectorized)
3. Built-in Spark functions

Use the same transformation and measure execution time.

## Lab 4: Spark SQL & Optimization - Practice Exercises

### Exercise 4.1: Query Optimization
**Task**: Write the same query in three ways:
1. Using DataFrame API
2. Using Spark SQL
3. Using a combination

Compare execution plans and performance.

### Exercise 4.2: CTE vs Subquery
**Task**: Write a complex query using:
1. Common Table Expressions (CTE)
2. Subqueries
3. Temporary views

Compare readability and performance.

### Exercise 4.3: Catalyst Optimizer Analysis
**Task**: Write queries that trigger different optimizations:
1. Predicate pushdown
2. Column pruning
3. Constant folding
4. Join reordering

Use `explain()` to verify optimizations.

### Exercise 4.4: AQE Comparison
**Task**: Run the same query with:
1. AQE enabled
2. AQE disabled

Compare execution time and resource utilization.

## Lab 5: Spark Streaming - Practice Exercises

### Exercise 5.1: Window Comparison
**Task**: Create a streaming application with:
1. Tumbling windows (5 minutes)
2. Sliding windows (5 minutes, 1 minute slide)
3. Session windows (5 minutes gap)

Compare results for the same input data.

### Exercise 5.2: Watermarking Impact
**Task**: Test different watermarking strategies:
1. No watermark
2. 1 minute watermark
3. 10 minute watermark

Observe how late data is handled in each case.

### Exercise 5.3: Output Modes
**Task**: Create a streaming aggregation and test:
1. Append mode
2. Complete mode
3. Update mode

Document the differences in output.

### Exercise 5.4: State Management
**Task**: Create a streaming query with state and:
1. Monitor state size over time
2. Test state recovery after failure
3. Implement state cleanup

## Lab 6: MLlib - Practice Exercises

### Exercise 6.1: Feature Engineering Pipeline
**Task**: Create a comprehensive feature engineering pipeline with:
1. Missing value imputation
2. Feature scaling
3. One-hot encoding
4. Feature selection

### Exercise 6.2: Model Comparison
**Task**: Train and compare multiple classification models:
1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Gradient Boosted Trees

Compare accuracy, precision, recall, and F1 score.

### Exercise 6.3: Hyperparameter Tuning
**Task**: Implement hyperparameter tuning using:
1. Grid search with CrossValidator
2. TrainValidationSplit
3. Manual parameter search

Compare results and tuning time.

### Exercise 6.4: Clustering Evaluation
**Task**: Apply K-Means clustering with different k values:
1. Use elbow method to find optimal k
2. Evaluate silhouette scores
3. Visualize clusters (if possible)

## Lab 7: Production Deployment - Practice Exercises

### Exercise 7.1: Docker Optimization
**Task**: Optimize a Docker image for Spark:
1. Use multi-stage builds
2. Minimize image size
3. Optimize layer caching

### Exercise 7.2: Kubernetes Configuration
**Task**: Create Kubernetes manifests for:
1. Spark master deployment
2. Spark worker deployment
3. ConfigMap for Spark configuration
4. Secret for sensitive data

### Exercise 7.3: Monitoring Setup
**Task**: Set up monitoring with:
1. Prometheus metrics exporter
2. Grafana dashboard for Spark metrics
3. Alert rules for common failures

### Exercise 7.4: CI/CD Pipeline
**Task**: Create a GitHub Actions workflow that:
1. Builds Spark application
2. Runs tests
3. Creates Docker image
4. Deploys to Kubernetes
5. Runs smoke tests

## Challenge Exercises

### Challenge 1: End-to-End Pipeline
**Task**: Build a complete pipeline that:
1. Ingests data from multiple sources
2. Performs data cleaning and validation
3. Applies machine learning model
4. Writes results to multiple sinks
5. Includes monitoring and alerting

### Challenge 2: Performance Optimization
**Task**: Take a slow Spark job and optimize it:
1. Analyze execution plan
2. Identify bottlenecks
3. Apply optimizations
4. Measure improvement

### Challenge 3: Real-Time Analytics
**Task**: Build a real-time analytics system:
1. Stream data from Kafka
2. Apply windowed aggregations
3. Train/update ML model online
4. Serve predictions via API

### Challenge 4: Fault Tolerance
**Task**: Make a Spark application fault-tolerant:
1. Implement checkpointing
2. Handle driver failures
3. Handle executor failures
4. Implement retry logic

## Solutions

Solutions to these exercises are available in the `solutions/` directory. Each exercise has a corresponding solution notebook with detailed explanations.

## Tips for Success

1. **Start Simple**: Begin with basic exercises and gradually increase complexity
2. **Experiment**: Try different approaches and compare results
3. **Monitor**: Always check Spark UI for performance insights
4. **Document**: Keep notes on what works and what doesn't
5. **Collaborate**: Discuss solutions with peers and learn from each other
6. **Iterate**: Refine your solutions based on feedback and results

## Additional Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark Performance Tuning Guide](https://spark.apache.org/docs/latest/tuning.html)
- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
