# Lab 6: Machine Learning with MLlib - Walkthrough Guide

## Overview
This guide provides step-by-step instructions for completing Lab 6: Machine Learning with MLlib.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Spark environment set up (run `./scripts/setup.sh`)
- Jupyter Notebook accessible at http://localhost:8888
- Completion of Lab 1: Spark Fundamentals
- Completion of Lab 2: Data Loading & Transformation
- Basic understanding of machine learning concepts

## Setup Instructions

### 1. Start the Environment
```bash
cd spark-code-practice
./scripts/start.sh
```

### 2. Open Jupyter Notebook
- Navigate to http://localhost:8888 in your browser
- Open `notebooks/chapter-06-machine-learning-mllib.ipynb`

## Lab Walkthrough

### Section A: Creating Sample Data for Machine Learning

#### Step 1: Import Required Libraries
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.feature import IndexToString
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
```

**Explanation**: Import MLlib libraries for feature engineering, model training, evaluation, and hyperparameter tuning.

#### Step 2: Create SparkSession for ML
```python
spark = SparkSession.builder \
    .appName("MLlibMachineLearning") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.shuffle.partitions", "4") \
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

#### Step 3: Create Classification Data
```python
# Create classification data (customer churn prediction)
classification_data = [
    (1, "Alice", 28, 75000, "Engineering", 5, 0, 0),
    (2, "Bob", 35, 85000, "Marketing", 3, 1, 0),
    (3, "Charlie", 42, 95000, "Engineering", 8, 0, 1),
    (4, "Diana", 31, 80000, "Sales", 4, 2, 0),
    (5, "Eve", 29, 72000, "Marketing", 2, 1, 0),
    (6, "Frank", 38, 88000, "Engineering", 6, 0, 1),
    (7, "Grace", 33, 78000, "Sales", 3, 1, 0),
    (8, "Henry", 45, 105000, "Executive", 10, 0, 1),
    (9, "Ivy", 27, 68000, "Marketing", 1, 2, 0),
    (10, "Jack", 40, 92000, "Engineering", 7, 0, 1),
    (11, "Kate", 36, 82000, "Sales", 4, 1, 0),
    (12, "Leo", 32, 77000, "Engineering", 5, 0, 0),
    (13, "Mary", 39, 90000, "Engineering", 9, 0, 1),
    (14, "Nick", 34, 83000, "Marketing", 4, 1, 0),
    (15, "Olivia", 30, 73000, "Sales", 3, 2, 0)
]

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True),
    StructField("department", StringType(), True),
    StructField("years_experience", IntegerType(), True),
    StructField("complaints", IntegerType(), True),
    StructField("churn", IntegerType(), True)  # Target variable
])

df_classification = spark.createDataFrame(classification_data, schema)
print("Classification data created:")
df_classification.show()
```

**Explanation**: Create sample data for customer churn prediction with various features and a binary target variable.

#### Step 4: Create Regression Data
```python
# Create regression data (salary prediction)
regression_data = [
    (1, 25, 50000, "Engineering", 1, 55000),
    (2, 30, 60000, "Marketing", 3, 65000),
    (3, 35, 70000, "Engineering", 5, 75000),
    (4, 40, 80000, "Sales", 7, 85000),
    (5, 28, 55000, "Marketing", 2, 60000),
    (6, 45, 95000, "Engineering", 15, 105000),
    (7, 32, 68000, "Sales", 4, 73000),
    (8, 38, 82000, "Engineering", 8, 87000),
    (9, 27, 58000, "Marketing", 2, 63000),
    (10, 42, 88000, "Engineering", 10, 93000)
]

regression_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("age", IntegerType(), True),
    StructField("education_level", IntegerType(), True),
    StructField("department", StringType(), True),
    StructField("years_experience", IntegerType(), True),
    StructField("salary", IntegerType(), True)  # Target variable
])

df_regression = spark.createDataFrame(regression_data, regression_schema)
print("\nRegression data created:")
df_regression.show()
```

**Explanation**: Create sample data for salary prediction with continuous target variable.

### Section B: Data Preparation for Classification

#### Step 5: Split Data into Train and Test
```python
# Split data into train and test
train_data, test_data = df_classification.randomSplit([0.8, 0.2], seed=42)
print(f"Training data: {train_data.count()} rows")
print(f"Test data: {test_data.count()} rows")
```

**Key Concept**: Always split data before any preprocessing to avoid data leakage. Use a fixed seed for reproducibility.

#### Step 6: Handle Categorical Features
```python
# Index categorical features
department_indexer = StringIndexer(inputCol="department", outputCol="department_index")
```

**Key Concept**: StringIndexer converts string categories to numerical indices required by ML algorithms.

**Practice**: Try OneHotEncoder after StringIndexer for better representation of categorical variables.

#### Step 7: Create Feature Vector
```python
# Create feature vector
assembler = VectorAssembler(
    inputCols=["age", "salary", "years_experience", "complaints", "department_index"],
    outputCol="features"
)
```

**Key Concept**: VectorAssembler combines multiple feature columns into a single feature vector column required by ML algorithms.

#### Step 8: Scale Features
```python
# Scale features
scaler = StandardScaler(inputCol="features", outputCol="scaled_features")

print("Data preparation components created")
```

**Key Concept**: Feature scaling ensures all features contribute equally to the model. Important for algorithms sensitive to feature scales.

### Section C: Building Classification Pipelines

#### Step 9: Logistic Regression Pipeline
```python
# Logistic Regression Pipeline
lr = LogisticRegression(featuresCol="scaled_features", labelCol="churn")

pipeline_lr = Pipeline(stages=[department_indexer, assembler, scaler, lr])

# Fit the pipeline
model_lr = pipeline_lr.fit(train_data)

# Make predictions
predictions_lr = model_lr.transform(test_data)

print("Logistic Regression predictions:")
predictions_lr.select("churn", "prediction", "probability").show(5, truncate=False)
```

**Key Concept**: Pipeline chains multiple transformers and estimators together, ensuring consistent preprocessing and training.

**Expected Output**: Predictions with actual churn values, predicted values, and probability estimates.

#### Step 10: Decision Tree Pipeline
```python
# Decision Tree Pipeline
dt = DecisionTreeClassifier(featuresCol="scaled_features", labelCol="churn")

pipeline_dt = Pipeline(stages=[department_indexer, assembler, scaler, dt])

# Fit the pipeline
model_dt = pipeline_dt.fit(train_data)

# Make predictions
predictions_dt = model_dt.transform(test_data)

print("Decision Tree predictions:")
predictions_dt.select("churn", "prediction").show(5)
```

**Key Concept**: Decision trees are non-parametric models that can capture non-linear relationships without feature scaling.

#### Step 11: Random Forest Pipeline
```python
# Random Forest Pipeline
rf = RandomForestClassifier(featuresCol="scaled_features", labelCol="churn", numTrees=10)

pipeline_rf = Pipeline(stages=[department_indexer, assembler, scaler, rf])

# Fit the pipeline
model_rf = pipeline_rf.fit(train_data)

# Make predictions
predictions_rf = model_rf.transform(test_data)

print("Random Forest predictions:")
predictions_rf.select("churn", "prediction").show(5)
```

**Key Concept**: Random Forest is an ensemble method that combines multiple decision trees for better performance and reduced overfitting.

### Section D: Model Evaluation for Classification

#### Step 12: Evaluate Models with AUC
```python
# Evaluate models
evaluator = BinaryClassificationEvaluator(labelCol="churn", metricName="areaUnderROC")

auc_lr = evaluator.evaluate(predictions_lr)
auc_dt = evaluator.evaluate(predictions_dt)
auc_rf = evaluator.evaluate(predictions_rf)

print(f"Logistic Regression AUC: {auc_lr:.4f}")
print(f"Decision Tree AUC: {auc_dt:.4f}")
print(f"Random Forest AUC: {auc_rf:.4f}")
```

**Key Concept**: AUC-ROC measures the ability of the classifier to distinguish between classes. Higher is better (0.5 = random, 1.0 = perfect).

#### Step 13: Evaluate with Accuracy
```python
# Additional metrics
evaluator_accuracy = BinaryClassificationEvaluator(labelCol="churn", metricName="accuracy")

accuracy_lr = evaluator_accuracy.evaluate(predictions_lr)
print(f"Logistic Regression Accuracy: {accuracy_lr:.4f}")
```

**Practice**: Try other metrics like precision, recall, and F1-score using appropriate evaluators.

### Section E: Regression Pipeline

#### Step 14: Build Regression Pipeline
```python
# Split regression data
train_reg, test_reg = df_regression.randomSplit([0.8, 0.2], seed=42)

# Index categorical feature
dept_indexer_reg = StringIndexer(inputCol="department", outputCol="department_index")

# Create feature vector
assembler_reg = VectorAssembler(
    inputCols=["age", "education_level", "years_experience", "department_index"],
    outputCol="features"
)

# Linear Regression
lr_reg = LinearRegression(featuresCol="features", labelCol="salary")

# Pipeline
pipeline_reg = Pipeline(stages=[dept_indexer_reg, assembler_reg, lr_reg])

# Fit pipeline
model_reg = pipeline_reg.fit(train_reg)

# Make predictions
predictions_reg = model_reg.transform(test_reg)

print("Regression predictions:")
predictions_reg.select("salary", "prediction").show(5)
```

**Key Concept**: Linear Regression predicts continuous values. The pipeline structure is similar to classification but uses regression-specific components.

### Section F: Regression Model Evaluation

#### Step 15: Evaluate Regression Model
```python
# Evaluate regression model
evaluator_reg = RegressionEvaluator(labelCol="salary", predictionCol="prediction")

rmse = evaluator_reg.setMetricName("rmse").evaluate(predictions_reg)
mae = evaluator_reg.setMetricName("mae").evaluate(predictions_reg)
r2 = evaluator_reg.setMetricName("r2").evaluate(predictions_reg)

print(f"Root Mean Square Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"R-squared (R2): {r2:.4f}")
```

**Key Concepts**:
- RMSE: Average magnitude of prediction errors (lower is better)
- MAE: Average absolute error (lower is better)
- R2: Proportion of variance explained (higher is better, max 1.0)

### Section G: Hyperparameter Tuning

#### Step 16: Create Parameter Grid
```python
# Create parameter grid for Logistic Regression
param_grid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.01, 0.1, 1.0]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
    .addGrid(lr.maxIter, [10, 50, 100]) \
    .build()
```

**Key Concept**: ParamGridBuilder defines the hyperparameter search space. More values = better search but longer runtime.

#### Step 17: Create Cross Validator
```python
# Create cross validator
crossval = CrossValidator(
    estimator=pipeline_lr,
    estimatorParamMaps=param_grid,
    evaluator=evaluator,
    numFolds=3
)

# Run cross validation
cv_model = crossval.fit(train_data)

# Best model
best_model = cv_model.bestModel
print("Best model parameters:")
print(best_model.stages[-1].extractParamMap())

# Evaluate best model
best_predictions = best_model.transform(test_data)
best_auc = evaluator.evaluate(best_predictions)
print(f"Best model AUC: {best_auc:.4f}")
```

**Key Concept**: CrossValidator performs k-fold cross-validation to find the best hyperparameter combination, preventing overfitting.

**Practice**: Try different parameter ranges and observe the impact on model performance and training time.

### Section H: Model Persistence

#### Step 18: Save and Load Model
```python
# Save model
model_lr.write().overwrite().save("models/logistic_regression")
print("Model saved to models/logistic_regression")

# Load model
from pyspark.ml.pipeline import PipelineModel
loaded_model = PipelineModel.load("models/logistic_regression")

# Use loaded model
loaded_predictions = loaded_model.transform(test_data)
print("Model loaded and predictions generated")
loaded_predictions.select("churn", "prediction").show(5)
```

**Key Concept**: Model persistence allows you to save trained models and load them later for production use, avoiding retraining.

## Troubleshooting Tips

### Issue: Model Training is Slow
**Solution**:
- Reduce number of hyperparameters in grid search
- Use fewer cross-validation folds
- Reduce training data size for experimentation
- Increase executor memory and cores
- Use caching for intermediate results

### Issue: Poor Model Performance
**Solution**:
- Check for data quality issues
- Try different feature combinations
- Experiment with different algorithms
- Perform feature engineering
- Check for class imbalance (use class weights)

### Issue: VectorAssembler Errors
**Solution**:
- Verify all input columns exist in DataFrame
- Check data types match expected types
- Handle null values before assembling
- Ensure numeric columns contain valid numbers

### Issue: StringIndexer Errors
**Solution**:
- Check that categorical columns contain strings
- Handle unseen labels in test data (use `handleInvalid` parameter)
- Ensure consistent categories across train and test
- Consider using `StringIndexerModel` for consistent indexing

### Issue: Memory Errors During Training
**Solution**:
- Reduce training data size
- Increase executor memory
- Reduce number of trees in Random Forest
- Use simpler models initially
- Enable Spark memory management optimizations

## Check Your Understanding

1. What is the purpose of VectorAssembler in MLlib?
2. What is the difference between Transformer and Estimator in MLlib?
3. Which metric would you use for evaluating a regression model?
4. What is the purpose of CrossValidator?
5. Why is it important to split data before preprocessing?

## Next Steps

After completing this lab:
1. Review the exam-style questions at the end of the notebook
2. Try the practice exercises in PRACTICE_EXERCISES.md
3. Compare your work with the solution notebook in `solutions/chapter-06-machine-learning-mllib-solution.ipynb`
4. Proceed to Lab 7: Production Deployment

## Additional Resources

- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [Pipeline API Documentation](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.Pipeline.html)
- [Model Evaluation](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.evaluation.html)
- [Hyperparameter Tuning](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.tuning.html)
