# Spark Code Practice - Comprehensive Walkthrough Guide

This guide provides step-by-step instructions for completing all 7 labs in the Spark Code Practice repository.

## Table of Contents
- [Lab 1: Spark Fundamentals](#lab-1-spark-fundamentals)
- [Lab 2: Data Loading & Transformation](#lab-2-data-loading-transformation)
- [Lab 3: Advanced DataFrame Operations](#lab-3-advanced-dataframe-operations)
- [Lab 4: Spark SQL & Optimization](#lab-4-spark-sql-optimization)
- [Lab 5: Spark Streaming Fundamentals](#lab-5-spark-streaming-fundamentals)
- [Lab 6: Machine Learning with MLlib](#lab-6-machine-learning-with-mllib)
- [Lab 7: Production Deployment](#lab-7-production-deployment)

---

## Lab 1: Spark Fundamentals

### Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Spark environment set up

### Setup
```bash
cd spark-code-practice
./scripts/setup.sh
./scripts/start.sh
```

### Key Steps
1. **Create SparkSession**: Connect to Spark master
2. **Create DataFrames**: From Python data and file formats
3. **Transformations vs Actions**: Understand lazy vs eager evaluation
4. **Basic Operations**: Filter, select, withColumn
5. **Spark SQL**: Register temp views and run SQL queries
6. **Read/Write Data**: Work with CSV, JSON, Parquet formats
7. **Spark UI**: Monitor job execution at http://localhost:4040

### Common Issues
- **Connection refused**: Check Docker containers with `docker-compose ps`
- **Memory errors**: Reduce executor memory in configuration
- **File not found**: Ensure data directories exist

### Success Criteria
- Successfully create and manipulate DataFrames
- Understand the difference between transformations and actions
- Execute Spark SQL queries
- Navigate the Spark UI

---

## Lab 2: Data Loading & Transformation

### Prerequisites
- Lab 1 completed
- Sample data created (run `python scripts/setup-data.py`)

### Key Steps
1. **Load CSV Data**: With schema inference and explicit schema
2. **Load JSON Data**: Handle nested structures with explode
3. **Load Parquet Data**: Columnar format for Spark optimization
4. **Handle Null Values**: drop, fill, coalesce operations
5. **Data Transformations**: String, numeric, regex operations
6. **Data Validation**: Check for nulls, duplicates, invalid data
7. **Write Data**: Different modes (overwrite, append, ignore)
8. **Partitioning**: Partition by columns for performance

### Common Issues
- **Schema mismatch**: Use explicit schema instead of inference
- **Null handling**: Use coalesce for conditional null handling
- **Partitioning**: Choose partition columns carefully based on query patterns

### Success Criteria
- Load data from multiple formats
- Handle null values appropriately
- Transform data using built-in functions
- Write data in different modes and partitions

---

## Lab 3: Advanced DataFrame Operations

### Prerequisites
- Labs 1-2 completed
- Understanding of basic DataFrame operations

### Key Steps
1. **Join Operations**: Inner, left, right, outer, semi, anti joins
2. **Window Functions**: Ranking (row_number, rank, dense_rank), lag/lead, aggregates
3. **Complex Data Types**: Arrays (explode), Maps (keys/values), Structs
4. **UDFs**: Python UDFs vs Pandas UDFs (vectorized)
5. **Broadcast Joins**: Optimize joins for small tables
6. **Performance**: Compare different join strategies

### Common Issues
- **Join performance**: Use broadcast joins for small tables
- **Memory issues with UDFs**: Use Pandas UDFs for better performance
- **Complex type handling**: Use proper functions (explode, map_keys, etc.)

### Success Criteria
- Perform different types of joins correctly
- Use window functions for analytics
- Work with complex data types
- Create and use UDFs effectively
- Optimize join performance

---

## Lab 4: Spark SQL & Optimization

### Prerequisites
- Labs 1-2 completed
- Understanding of DataFrame operations

### Key Steps
1. **Basic SQL Operations**: SELECT, WHERE, ORDER BY
2. **Aggregations**: GROUP BY, HAVING, aggregate functions
3. **Advanced SQL**: CTEs, CASE statements, subqueries
4. **Window Functions in SQL**: Ranking, analytical functions
5. **Query Plans**: Explain and analyze execution plans
6. **Query Hints**: Broadcast, repartition hints
7. **Optimization**: Predicate pushdown, column pruning, caching
8. **AQE**: Adaptive Query Execution configuration
9. **Catalog Operations**: Databases, tables, views management

### Common Issues
- **Slow queries**: Use explain() to analyze plans and apply optimizations
- **AQE not working**: Ensure AQE is enabled in configuration
- **Catalog errors**: Check database and view names

### Success Criteria
- Write efficient SQL queries
- Understand query execution plans
- Apply optimization techniques
- Use AQE for runtime optimization

---

## Lab 5: Spark Streaming Fundamentals

### Prerequisites
- Labs 1-2 completed
- Understanding of basic DataFrame operations

### Key Steps
1. **Streaming Concepts**: Input table, query, result table, output
2. **Streaming Sources**: Rate source (testing), file source, socket
3. **Transformations**: Apply transformations to streaming data
4. **Window Operations**: Tumbling, sliding, session windows
5. **Watermarking**: Handle late data and control state size
6. **Output Modes**: Append, complete, update
7. **Sinks**: Console, memory, file sinks
8. **Query Management**: Start, stop, monitor streaming queries

### Common Issues
- **Streaming directory not found**: Create directory before starting stream
- **Late data not handled**: Configure appropriate watermark
- **State size growing**: Tune watermark and check query logic

### Success Criteria
- Create streaming DataFrames from different sources
- Apply window operations and watermarking
- Write streaming queries to different sinks
- Manage streaming query lifecycle

---

## Lab 6: Machine Learning with MLlib

### Prerequisites
- Labs 1-2 completed
- Understanding of basic DataFrame operations

### Key Steps
1. **Data Preparation**: Train/test split, categorical handling
2. **Feature Engineering**: StringIndexer, OneHotEncoder, VectorAssembler
3. **Feature Scaling**: StandardScaler for normalization
4. **Classification Models**: Logistic Regression, Decision Trees, Random Forest
5. **Regression Models**: Linear Regression, Gradient Boosting
6. **Model Evaluation**: Classification metrics (AUC, accuracy), regression metrics (RMSE, R2)
7. **Hyperparameter Tuning**: CrossValidator with ParamGridBuilder
8. **Model Persistence**: Save and load trained models

### Common Issues
- **Feature vector errors**: Ensure all features are numeric after transformation
- **Model overfitting**: Use cross-validation and proper train/test split
- **Hyperparameter search time**: Limit parameter grid size

### Success Criteria
- Build ML pipelines with multiple stages
- Train and evaluate classification and regression models
- Perform hyperparameter tuning
- Save and load models for production use

---

## Lab 7: Production Deployment

### Prerequisites
- All previous labs completed
- Understanding of Spark architecture and optimization

### Key Steps
1. **Docker Deployment**: Create Dockerfile and docker-compose.yml
2. **Kubernetes Deployment**: Deployments, ConfigMaps, Secrets, RBAC
3. **Monitoring**: Prometheus configuration, Grafana dashboards
4. **CI/CD**: GitHub Actions workflow for build and deploy
5. **Security**: Secret management, RBAC, network policies
6. **Performance Tuning**: Production configuration optimization
7. **High Availability**: Checkpointing, master HA, fault tolerance

### Common Issues
- **Docker image size**: Use multi-stage builds to optimize
- **Kubernetes resource limits**: Adjust requests/limits based on workload
- **Secrets not accessible**: Verify RBAC permissions
- **Performance issues**: Tune Spark configuration for production

### Success Criteria
- Containerize Spark applications with Docker
- Deploy Spark on Kubernetes
- Set up monitoring with Prometheus/Grafana
- Implement CI/CD pipelines
- Apply security best practices

---

## General Tips for All Labs

### Before Starting Each Lab
1. Read the objectives and prerequisites
2. Review the relevant cheatsheet
3. Ensure the environment is running correctly
4. Check that previous labs' data is available if needed

### During the Lab
1. Run cells sequentially and understand the output
2. Read the explanations in markdown cells
3. Experiment with different parameters and options
4. Check Spark UI for job execution (for applicable labs)
5. Save your work frequently

### After Completing Each Lab
1. Answer the exam-style questions at the end
2. Review the solution notebook for comparison
3. Try the corresponding practice exercises
4. Document any issues encountered

### Troubleshooting Common Issues

#### Environment Issues
```bash
# Check Docker containers
docker-compose ps

# Restart services
./scripts/stop.sh
./scripts/start.sh

# Check Spark logs
docker-compose logs spark-master
```

#### Spark Issues
```python
# Check Spark configuration
spark.conf.getAll()

# Check Spark version
spark.version

# Clear cache if memory issues
spark.catalog.clearCache()
```

#### Data Issues
```bash
# Regenerate sample data
python scripts/setup-data.py

# Check data directories
ls -la data/
```

## Learning Path Recommendation

1. **Beginner Path**: Complete Labs 1-2 sequentially (3-4 hours)
2. **Intermediate Path**: Complete Labs 3-5 after beginner labs (6-8 hours)
3. **Advanced Path**: Complete Labs 6-7 after intermediate labs (3-4 hours)
4. **Total Time**: 12-16 hours for complete learning path

## Additional Resources

- [Cheatsheets](cheatsheets/) - Quick reference guides
- [Practice Exercises](PRACTICE_EXERCISES.md) - Additional practice problems
- [Solution Notebooks](solutions/) - Reference implementations
- [Spark Documentation](https://spark.apache.org/docs/latest/) - Official docs
- [PySpark API](https://spark.apache.org/docs/latest/api/python/) - API reference

## Getting Help

If you encounter issues:
1. Check the Troubleshooting section above
2. Review the solution notebook for comparison
3. Check the Spark documentation
4. Open an issue on GitHub if you find a bug

## Success Metrics

You have successfully completed the learning path when you can:
- Create and manipulate DataFrames confidently
- Write and optimize Spark SQL queries
- Apply advanced DataFrame operations (joins, window functions)
- Build and evaluate ML models with MLlib
- Deploy Spark applications in production
- Monitor and troubleshoot Spark applications
