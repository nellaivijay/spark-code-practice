# Chapter 6: Machine Learning with MLlib

## Overview

This lab introduces Apache Spark's Machine Learning Library (MLlib), a scalable machine learning library built on top of Spark. MLlib provides a wide range of algorithms and utilities for building scalable machine learning pipelines.

### Why MLlib Matters

MLlib is essential because:
- **Scalability**: Train models on massive datasets that don't fit in memory
- **Speed**: Distributed training across clusters for faster results
- **Integration**: Seamlessly integrates with Spark's data processing capabilities
- **Production Ready**: Battle-tested algorithms used in production at scale
- **Unified API**: Consistent API across different algorithms

### Real-World Applications

- **Predictive Analytics**: Customer churn prediction, sales forecasting
- **Recommendation Systems**: Product recommendations, content personalization
- **Fraud Detection**: Identifying fraudulent transactions
- **Classification**: Spam detection, sentiment analysis
- **Clustering**: Customer segmentation, anomaly detection

## Learning Objectives

By the end of this lab, you will be able to:
- Understand MLlib's architecture and components
- Prepare data for machine learning
- Build machine learning pipelines
- Train classification models
- Train regression models
- Perform clustering
- Evaluate model performance
- Save and load models

## Prerequisites

- Completion of Chapter 1: Spark Fundamentals
- Completion of Chapter 2: Data Loading and Transformation
- Basic understanding of machine learning concepts
- Docker environment running

## Estimated Time

90-120 minutes

## Lab Environment

This lab uses the same Docker-based Spark environment with MLlib capabilities.

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
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor, RandomForestRegressor
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator, RegressionEvaluator, ClusteringEvaluator
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

spark = SparkSession.builder \
    .appName("MLlibMachineLearning") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

## Exercise 1: Data Preparation for ML

### Task

Prepare data for machine learning using MLlib's feature transformers.

### Steps

1. **Create sample dataset**

```python
# Create sample customer data
customer_data = [
    (1, "Alice", 28, 75000, "Engineering", 5, 0),
    (2, "Bob", 35, 85000, "Marketing", 3, 0),
    (3, "Charlie", 42, 95000, "Engineering", 8, 1),
    (4, "Diana", 31, 72000, "Sales", 2, 0),
    (5, "Eve", 29, 68000, "Marketing", 4, 0),
    (6, "Frank", 38, 90000, "Engineering", 6, 1),
    (7, "Grace", 26, 65000, "Sales", 1, 0),
    (8, "Henry", 33, 78000, "Marketing", 5, 0),
    (9, "Ivy", 30, 82000, "Engineering", 7, 1),
    (10, "Jack", 27, 69000, "Sales", 2, 0)
]

customer_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True),
    StructField("department", StringType(), True),
    StructField("years_at_company", IntegerType(), True),
    StructField("churned", IntegerType(), True)
])

df_customers = spark.createDataFrame(customer_data, customer_schema)
df_customers.show()
```

2. **Handle categorical variables**

```python
# String indexer for department
department_indexer = StringIndexer(
    inputCol="department",
    outputCol="department_index"
)

# Fit and transform
department_indexer_model = department_indexer.fit(df_customers)
df_indexed = department_indexer_model.transform(df_customers)
df_indexed.show()
```

3. **Assemble features into vector**

```python
# Assemble features into a single vector column
assembler = VectorAssembler(
    inputCols=["age", "salary", "department_index", "years_at_company"],
    outputCol="features"
)

df_features = assembler.transform(df_indexed)
df_features.show(truncate=False)
```

4. **Scale features**

```python
# Standardize features
scaler = StandardScaler(
    inputCol="features",
    outputCol="scaled_features",
    withStd=True,
    withMean=False
)

scaler_model = scaler.fit(df_features)
df_scaled = scaler_model.transform(df_features)

df_scaled.select("features", "scaled_features").show(truncate=False)
```

### Verification

- [ ] Categorical variables are indexed correctly
- [ ] Features are assembled into vectors
- [ ] Features are scaled appropriately

## Exercise 2: Building a Classification Pipeline

### Task

Build a complete machine learning pipeline for classification.

### Steps

1. **Create pipeline**

```python
# Define pipeline stages
indexer = StringIndexer(inputCol="department", outputCol="department_index")
assembler = VectorAssembler(
    inputCols=["age", "salary", "department_index", "years_at_company"],
    outputCol="features"
)
scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
lr = LogisticRegression(featuresCol="scaled_features", labelCol="churned", maxIter=10)

# Create pipeline
pipeline = Pipeline(stages=[indexer, assembler, scaler, lr])
```

2. **Split data into train and test sets**

```python
# Split data
train_data, test_data = df_customers.randomSplit([0.8, 0.2], seed=42)

print(f"Training data count: {train_data.count()}")
print(f"Test data count: {test_data.count()}")
```

3. **Train the model**

```python
# Fit the pipeline
model = pipeline.fit(train_data)

# Make predictions
predictions = model.transform(test_data)
predictions.select("id", "churned", "prediction", "probability").show()
```

4. **Evaluate the model**

```python
# Evaluate model
evaluator = BinaryClassificationEvaluator(
    labelCol="churned",
    predictionCol="prediction",
    metricName="areaUnderROC"
)

auc = evaluator.evaluate(predictions)
print(f"Area Under ROC: {auc:.4f}")

# Accuracy
from pyspark.sql.functions import col
accuracy = predictions.filter(col("churned") == col("prediction")).count() / predictions.count()
print(f"Accuracy: {accuracy:.4f}")
```

### Verification

- [ ] Pipeline is created successfully
- [ ] Model is trained on training data
- [ ] Predictions are made on test data
- [ ] Model is evaluated with appropriate metrics

## Exercise 3: Comparing Classification Algorithms

### Task

Compare different classification algorithms.

### Steps

1. **Logistic Regression**

```python
# Logistic Regression
lr = LogisticRegression(featuresCol="scaled_features", labelCol="churned", maxIter=10)
pipeline_lr = Pipeline(stages=[indexer, assembler, scaler, lr])

model_lr = pipeline_lr.fit(train_data)
predictions_lr = model_lr.transform(test_data)

evaluator = BinaryClassificationEvaluator(labelCol="churned", metricName="areaUnderROC")
auc_lr = evaluator.evaluate(predictions_lr)
print(f"Logistic Regression AUC: {auc_lr:.4f}")
```

2. **Decision Tree**

```python
# Decision Tree
dt = DecisionTreeClassifier(featuresCol="scaled_features", labelCol="churned")
pipeline_dt = Pipeline(stages=[indexer, assembler, scaler, dt])

model_dt = pipeline_dt.fit(train_data)
predictions_dt = model_dt.transform(test_data)

auc_dt = evaluator.evaluate(predictions_dt)
print(f"Decision Tree AUC: {auc_dt:.4f}")
```

3. **Random Forest**

```python
# Random Forest
rf = RandomForestClassifier(featuresCol="scaled_features", labelCol="churned", numTrees=10)
pipeline_rf = Pipeline(stages=[indexer, assembler, scaler, rf])

model_rf = pipeline_rf.fit(train_data)
predictions_rf = model_rf.transform(test_data)

auc_rf = evaluator.evaluate(predictions_rf)
print(f"Random Forest AUC: {auc_rf:.4f}")
```

### Verification

- [ ] All classification algorithms train successfully
- [ ] Models are evaluated consistently
- [ ] Best model is identified based on metrics

## Exercise 4: Regression Models

### Task

Build regression models for predicting continuous values.

### Steps

1. **Create regression dataset**

```python
# Create dataset for salary prediction
salary_data = [
    (28, 5, 75000),
    (35, 8, 85000),
    (42, 12, 95000),
    (31, 4, 72000),
    (29, 6, 68000),
    (38, 10, 90000),
    (26, 3, 65000),
    (33, 7, 78000),
    (30, 8, 82000),
    (27, 4, 69000)
]

salary_schema = StructType([
    StructField("age", IntegerType(), True),
    StructField("years_experience", IntegerType(), True),
    StructField("salary", IntegerType(), True)
])

df_salary = spark.createDataFrame(salary_data, salary_schema)
df_salary.show()
```

2. **Prepare features**

```python
# Assemble features
assembler = VectorAssembler(
    inputCols=["age", "years_experience"],
    outputCol="features"
)

df_salary_features = assembler.transform(df_salary)
df_salary_features.show()
```

3. **Linear Regression**

```python
# Split data
train_salary, test_salary = df_salary_features.randomSplit([0.8, 0.2], seed=42)

# Linear Regression
lr = LinearRegression(featuresCol="features", labelCol="salary", maxIter=10)
lr_model = lr.fit(train_salary)

# Make predictions
predictions_salary = lr_model.transform(test_salary)
predictions_salary.select("age", "years_experience", "salary", "prediction").show()

# Evaluate
evaluator = RegressionEvaluator(labelCol="salary", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions_salary)
print(f"RMSE: {rmse:.2f}")

# R-squared
r2 = evaluator.setMetricName("r2").evaluate(predictions_salary)
print(f"R-squared: {r2:.4f}")
```

### Verification

- [ ] Regression models are trained successfully
- [ ] Predictions are made on test data
- [ ] Models are evaluated with appropriate metrics

## Exercise 5: Clustering

### Task

Perform clustering to discover patterns in data.

### Steps

1. **Create dataset for clustering**

```python
# Create customer behavior data
behavior_data = [
    (100, 5, 2000),
    (150, 8, 3500),
    (80, 3, 1500),
    (200, 12, 5000),
    (120, 6, 2500),
    (90, 4, 1800),
    (180, 10, 4500),
    (70, 2, 1200),
    (160, 9, 4000),
    (110, 5, 2200)
]

behavior_schema = StructType([
    StructField("annual_spend", IntegerType(), True),
    StructField("visits_per_month", IntegerType(), True),
    StructField("total_purchases", IntegerType(), True)
])

df_behavior = spark.createDataFrame(behavior_data, behavior_schema)
df_behavior.show()
```

2. **Prepare features**

```python
# Assemble features
assembler = VectorAssembler(
    inputCols=["annual_spend", "visits_per_month", "total_purchases"],
    outputCol="features"
)

df_behavior_features = assembler.transform(df_behavior)

# Scale features
scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
scaler_model = scaler.fit(df_behavior_features)
df_behavior_scaled = scaler_model.transform(df_behavior_features)
```

3. **K-Means Clustering**

```python
# K-Means clustering
kmeans = KMeans(featuresCol="scaled_features", k=3, seed=42)
kmeans_model = kmeans.fit(df_behavior_scaled)

# Make predictions
predictions_kmeans = kmeans_model.transform(df_behavior_scaled)
predictions_kmeans.select("annual_spend", "visits_per_month", "prediction").show()
```

4. **Evaluate clustering**

```python
# Show cluster centers
centers = kmeans_model.clusterCenters()
print("Cluster Centers:")
for i, center in enumerate(centers):
    print(f"Cluster {i}: {center}")
```

### Verification

- [ ] Features are prepared correctly
- [ ] K-Means clustering runs successfully
- [ ] Cluster centers are computed
- [ ] Clustering is evaluated

## Exercise 6: Model Persistence

### Task

Save and load trained models.

### Steps

1. **Save the model**

```python
# Save the best classification model
model_path = "/opt/spark/models/churn_model"
best_pipeline_model = model_rf  # Using Random Forest from earlier

best_pipeline_model.write().overwrite().save(model_path)
print(f"Model saved to {model_path}")
```

2. **Load the model**

```python
from pyspark.ml.pipeline import PipelineModel

# Load the model
loaded_model = PipelineModel.load(model_path)

# Use loaded model for predictions
loaded_predictions = loaded_model.transform(test_data)
loaded_predictions.select("id", "churned", "prediction").show()
```

### Verification

- [ ] Model is saved successfully
- [ ] Model is loaded correctly
- [ ] Loaded model produces same predictions

## Cleanup

```python
# Stop Spark session
spark.stop()

# Stop Docker containers
docker-compose down
```

## Troubleshooting

### Issue: Model training is slow
**Solution**: Increase cluster resources or reduce dataset size

### Issue: Poor model performance
**Solution**: Try feature engineering, different algorithms, or hyperparameter tuning

### Issue: Out of memory during training
**Solution**: Increase memory allocation or use smaller batch sizes

## Expected Outcomes

By the end of this lab, you should:
- Be able to prepare data for machine learning
- Build machine learning pipelines
- Train classification models
- Train regression models
- Perform clustering
- Evaluate model performance
- Save and load models

## Next Steps

- Chapter 7: Production Deployment
- Advanced MLlib: Deep Learning with TensorFlow on Spark
- Real-time ML: Streaming Machine Learning

## Additional Resources

- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [Classification and Regression](https://spark.apache.org/docs/latest/ml-classification-regression.html)
- [Clustering](https://spark.apache.org/docs/latest/ml-clustering.html)
- [Model Selection and Tuning](https://spark.apache.org/docs/latest/ml-tuning.html)