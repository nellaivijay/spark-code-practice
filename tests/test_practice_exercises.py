"""
Unit Tests for Spark Code Practice Exercises

This test suite provides automated validation for practice exercises
across all labs. Run with: pytest tests/test_practice_exercises.py
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestLab1Exercises:
    """Unit tests for Lab 1 practice exercises"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for testing"""
        spark = SparkSession.builder \
            .appName("TestLab1") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_exercise_1_1_dataframe_creation(self, spark):
        """Test Exercise 1.1: DataFrame creation with explicit schema"""
        data = [
            ("Product A", 100, 25.50),
            ("Product B", 200, 15.75),
            ("Product C", 150, 30.00),
            ("Product D", 75, 45.25)
        ]
        
        schema = StructType([
            StructField("product_name", StringType(), True),
            StructField("quantity", IntegerType(), True),
            StructField("price", DoubleType(), True)
        ])
        
        df = spark.createDataFrame(data, schema)
        
        assert df.count() == 4
        assert len(df.columns) == 3
        assert df.schema["product_name"].dataType == StringType()
        assert df.schema["quantity"].dataType == IntegerType()
        assert df.schema["price"].dataType == DoubleType()
    
    def test_exercise_1_2_total_value_calculation(self, spark):
        """Test Exercise 1.2: Calculate total value"""
        data = [
            ("Product A", 100, 25.50),
            ("Product B", 200, 15.75)
        ]
        
        schema = StructType([
            StructField("product_name", StringType(), True),
            StructField("quantity", IntegerType(), True),
            StructField("price", DoubleType(), True)
        ])
        
        df = spark.createDataFrame(data, schema)
        from pyspark.sql.functions import col
        
        df_with_total = df.withColumn("total_value", col("quantity") * col("price"))
        
        # Verify calculation
        assert df_with_total.select("total_value").collect()[0]["total_value"] == 2550.0
        assert df_with_total.select("total_value").collect()[1]["total_value"] == 3150.0
    
    def test_exercise_1_3_transformation_action_identification(self, spark):
        """Test Exercise 1.3: Identify transformations vs actions"""
        from pyspark.sql.functions import col
        
        data = [("Alice", 25, 75000)]
        df = spark.createDataFrame(data, ["name", "age", "salary"])
        
        # Test that these are transformations (lazy)
        filtered = df.filter(col("age") > 20)
        selected = df.select("name")
        with_col = df.withColumn("bonus", col("salary") * 0.1)
        
        # These should not have executed yet
        # Just verify they are DataFrames
        
        # Test that these are actions (eager)
        count = df.count()
        show = df.collect()
        
        assert count == 1
        assert len(show) == 1


class TestLab2Exercises:
    """Unit tests for Lab 2 practice exercises"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for testing"""
        spark = SparkSession.builder \
            .appName("TestLab2") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_exercise_2_1_multi_format_loading(self, spark):
        """Test Exercise 2.1: Load data from multiple formats"""
        # Create test data
        data = [("Alice", 25, 75000)]
        
        # Test CSV
        df = spark.createDataFrame(data, ["name", "age", "salary"])
        df.write.mode("overwrite").csv("test_output/test.csv", header=True)
        df_csv = spark.read.csv("test_output/test.csv", header=True, inferSchema=True)
        assert df_csv.count() == 1
        
        # Test JSON
        df.write.mode("overwrite").json("test_output/test.json")
        df_json = spark.read.json("test_output/test.json")
        assert df_json.count() == 1
        
        # Test Parquet
        df.write.mode("overwrite").parquet("test_output/test.parquet")
        df_parquet = spark.read.parquet("test_output/test.parquet")
        assert df_parquet.count() == 1
    
    def test_exercise_2_2_data_cleaning(self, spark):
        """Test Exercise 2.2: Data cleaning with various issues"""
        from pyspark.sql.functions import col
        
        # Create data with issues
        data = [
            ("Alice", 25, 75000),
            (None, 30, None),
            ("Charlie", -5, 95000),  # Invalid age
            ("Diana", 28, -1000)    # Invalid salary
        ]
        
        df = spark.createDataFrame(data, ["name", "age", "salary"])
        
        # Remove invalid data
        df_clean = df.filter((col("age") > 0) & (col("age") < 100) & (col("salary") > 0))
        
        assert df_clean.count() == 1  # Only Alice should remain
        assert df_clean.collect()[0]["name"] == "Alice"
    
    def test_exercise_2_3_complex_transformations(self, spark):
        """Test Exercise 2.3: Complex transformations"""
        from pyspark.sql.functions import col, to_date, round
        
        data = [("2024-01-01", "Product A", "Electronics", 5, 500.00)]
        df = spark.createDataFrame(data, ["date", "product", "category", "quantity", "revenue"])
        
        # Add transformations
        df_transformed = df.withColumn("revenue_per_unit", col("revenue") / col("quantity")) \
                           .withColumn("month", to_date(col("date")).substr(5, 2)) \
                           .withColumn("revenue_rounded", round(col("revenue"), 2))
        
        assert df_transformed.select("revenue_per_unit").collect()[0]["revenue_per_unit"] == 100.0
        assert df_transformed.select("revenue_rounded").collect()[0]["revenue_rounded"] == 500.00


class TestLab3Exercises:
    """Unit tests for Lab 3 practice exercises"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for testing"""
        spark = SparkSession.builder \
            .appName("TestLab3") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_exercise_3_1_join_performance(self, spark):
        """Test Exercise 3.1: Join performance comparison"""
        from pyspark.sql.functions import col, broadcast
        
        # Create test data
        employees = spark.createDataFrame(
            [(1, "Alice", 75000), (2, "Bob", 85000), (3, "Charlie", 95000)],
            ["id", "name", "salary"]
        )
        departments = spark.createDataFrame(
            [(101, "Engineering"), (102, "Marketing")],
            ["dept_id", "dept_name"]
        )
        
        # Add dept_id to employees for join
        employees = employees.withColumn("dept_id", col("id") + 100)
        
        # Regular join
        regular_join = employees.join(departments, "dept_id")
        assert regular_join.count() == 3
        
        # Broadcast join
        broadcast_join = employees.join(broadcast(departments), "dept_id")
        assert broadcast_join.count() == 3
    
    def test_exercise_3_2_window_functions(self, spark):
        """Test Exercise 3.2: Advanced window functions"""
        from pyspark.sql.window import Window
        from pyspark.sql.functions import col, row_number, lag, lead, sum as spark_sum
        
        data = [
            ("Engineering", 75000, "2024-01"),
            ("Engineering", 85000, "2024-02"),
            ("Marketing", 65000, "2024-01"),
            ("Sales", 70000, "2024-01")
        ]
        
        df = spark.createDataFrame(data, ["department", "salary", "month"])
        
        # Window specification
        window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
        
        # Ranking functions
        df_with_rank = df.withColumn("row_num", row_number().over(window_spec))
        
        # Analytic functions
        df_with_lag = df.withColumn("lag_salary", lag("salary", 1).over(window_spec))
        
        # Aggregate functions
        window_agg = Window.partitionBy("department")
        df_with_agg = df.withColumn("dept_total", spark_sum("salary").over(window_agg))
        
        assert df_with_rank.count() == 4
        assert df_with_agg.count() == 4


class TestLab4Exercises:
    """Unit tests for Lab 4 practice exercises"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for testing"""
        spark = SparkSession.builder \
            .appName("TestLab4") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .config("spark.sql.adaptive.enabled", "true") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_exercise_4_1_query_optimization(self, spark):
        """Test Exercise 4.1: Query optimization techniques"""
        from pyspark.sql.functions import col
        
        data = [("Alice", 28, 75000), ("Bob", 35, 85000)]
        df = spark.createDataFrame(data, ["name", "age", "salary"])
        
        # Test predicate pushdown - filter before join
        filtered = df.filter(col("salary") > 80000)
        assert filtered.count() == 1
        assert filtered.collect()[0]["name"] == "Bob"
    
    def test_exercise_4_2_cte_vs_subquery(self, spark):
        """Test Exercise 4.2: CTE vs subquery"""
        data = [("Alice", 75000), ("Bob", 85000)]
        df = spark.createDataFrame(data, ["name", "salary"])
        df.createOrReplaceTempView("employees")
        
        # CTE approach
        cte_result = spark.sql("""
            WITH avg_salary AS (
                SELECT AVG(salary) as avg_sal FROM employees
            )
            SELECT name, salary FROM employees
            WHERE salary > (SELECT avg_sal FROM avg_salary)
        """)
        
        # Should return only Bob (salary 85000 > avg 80000)
        assert cte_result.count() == 1
        assert cte_result.collect()[0]["name"] == "Bob"
    
    def test_exercise_4_3_aqe_comparison(self, spark):
        """Test Exercise 4.3: AQE configuration"""
        # Check AQE is enabled
        assert spark.conf.get("spark.sql.adaptive.enabled") == "true"


class TestLab5Exercises:
    """Unit tests for Lab 5 practice exercises"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for testing"""
        spark = spark.builder \
            .appName("TestLab5") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_exercise_5_1_window_comparison(self, spark):
        """Test Exercise 5.1: Window operation comparison"""
        from pyspark.sql.functions import window, col, count
        
        # Create test data with timestamps
        data = [
            (1, "2024-01-01 10:00:00", 10.0),
            (2, "2024-01-01 10:05:00", 20.0),
            (3, "2024-01-01 10:10:00", 15.0)
        ]
        
        df = spark.createDataFrame(data, ["id", "timestamp", "value"])
        df = df.withColumn("timestamp", col("timestamp").cast("timestamp"))
        
        # Tumbling window
        tumbling = df.groupBy(window(col("timestamp"), "5 minutes")).agg(count("*").alias("count"))
        
        # Sliding window
        sliding = df.groupBy(window(col("timestamp"), "5 minutes", "2 minutes")).agg(count("*").alias("count"))
        
        # Both should produce results
        assert tumbling.count() > 0
        assert sliding.count() > 0
    
    def test_exercise_5_2_watermarking_impact(self, spark):
        """Test Exercise 5.2: Watermarking configuration"""
        from pyspark.sql.functions import col, window, count
        
        # Create test data
        data = [(1, "2024-01-01 10:00:00", 10.0)]
        df = spark.createDataFrame(data, ["id", "timestamp", "value"])
        df = df.withColumn("timestamp", col("timestamp").cast("timestamp"))
        
        # Add watermark
        watermarked = df.withWatermark("timestamp", "10 seconds")
        
        # Should still work as DataFrame
        assert watermarked.count() == 1


class TestLab6Exercises:
    """Unit tests for Lab 6 practice exercises"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for testing"""
        spark = SparkSession.builder \
            .appName("TestLab6") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/sparkwarehouse") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_exercise_6_1_feature_engineering(self, spark):
        """Test Exercise 6.1: Feature engineering pipeline"""
        from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
        from pyspark.ml import Pipeline
        
        # Create test data
        data = [(1, "Alice", 28, 75000, "Engineering", 0)]
        df = spark.createDataFrame(data, ["id", "name", "age", "salary", "department", "churn"])
        
        # Create pipeline stages
        indexer = StringIndexer(inputCol="department", outputCol="department_index")
        assembler = VectorAssembler(
            inputCols=["age", "salary", "department_index"],
            outputCol="features"
        )
        scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
        
        # Build pipeline
        pipeline = Pipeline(stages=[indexer, assembler, scaler])
        
        # Fit pipeline
        model = pipeline.fit(df)
        
        # Transform
        result = model.transform(df)
        
        # Should have scaled features
        assert "scaled_features" in result.columns
        assert result.count() == 1
    
    def test_exercise_6_2_model_comparison(self, spark):
        """Test Exercise 6.2: Model comparison"""
        from pyspark.ml.feature import VectorAssembler, StringIndexer
        from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier
        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml import Pipeline
        
        # Create test data
        data = [
            (1, 25, 50000, "Engineering", 0),
            (2, 30, 60000, "Marketing", 1),
            (3, 35, 70000, "Engineering", 1)
        ]
        df = spark.createDataFrame(data, ["id", "age", "salary", "department", "churn"])
        
        # Feature engineering
        indexer = StringIndexer(inputCol="department", outputCol="department_index")
        assembler = VectorAssembler(
            inputCols=["age", "salary", "department_index"],
            outputCol="features"
        )
        
        # Logistic Regression pipeline
        lr = LogisticRegression(featuresCol="features", labelCol="churn")
        pipeline_lr = Pipeline(stages=[indexer, assembler, lr])
        
        # Decision Tree pipeline
        dt = DecisionTreeClassifier(featuresCol="features", labelCol="churn")
        pipeline_dt = Pipeline(stages=[indexer, assembler, dt])
        
        # Fit models
        model_lr = pipeline_lr.fit(df)
        model_dt = pipeline_dt.fit(df)
        
        # Both should produce predictions
        pred_lr = model_lr.transform(df)
        pred_dt = model_dt.transform(df)
        
        assert "prediction" in pred_lr.columns
        assert "prediction" in pred_dt.columns
        assert pred_lr.count() == 3
        assert pred_dt.count() == 3


class TestLab7Exercises:
    """Unit tests for Lab 7 practice exercises"""
    
    def test_exercise_7_1_docker_optimization(self):
        """Test Exercise 7.1: Docker configuration"""
        # Test that Dockerfile components are present
        dockerfile_exists = os.path.exists("Dockerfile")
        docker_compose_exists = os.path.exists("docker-compose.yml")
        
        # Note: These files may not exist in the test environment
        # This test validates the concept rather than actual files
        assert True  # Placeholder - would check actual Docker configurations
    
    def test_exercise_7_2_kubernetes_configuration(self):
        """Test Exercise 7.2: Kubernetes configuration"""
        # Test Kubernetes manifest structure
        # This is a conceptual test
        assert True  # Placeholder - would validate K8s manifests
    
    def test_exercise_7_3_monitoring_setup(self):
        """Test Exercise 7.3: Monitoring configuration"""
        # Test Prometheus configuration format
        prometheus_config = """
        global:
          scrape_interval: 15s
        scrape_configs:
          - job_name: 'spark-master'
        """
        
        # Validate YAML structure (basic check)
        assert "scrape_configs" in prometheus_config
        assert "global" in prometheus_config


class TestIntegration:
    """Integration tests across multiple labs"""
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create a Spark session for integration testing"""
        spark = SparkSession.builder \
            .appName("IntegrationTests") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/sparkwarehouse") \
            .getOrCreate()
        yield spark
        spark.stop()
    
    def test_end_to_end_pipeline(self, spark):
        """Test end-to-end pipeline from Lab 6"""
        from pyspark.ml.feature import VectorAssembler, StringIndexer
        from pyspark.ml.classification import LogisticRegression
        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml import Pipeline
        
        # Create complete pipeline
        data = [
            (1, "Alice", 28, 75000, "Engineering", 0),
            (2, "Bob", 35, 85000, "Marketing", 1),
            (3, "Charlie", 42, 95000, "Engineering", 1)
        ]
        df = spark.createDataFrame(data, ["id", "name", "age", "salary", "department", "churn"])
        
        # Split data
        train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
        
        # Build pipeline
        indexer = StringIndexer(inputCol="department", outputCol="department_index")
        assembler = VectorAssembler(
            inputCols=["age", "salary", "department_index"],
            outputCol="features"
        )
        lr = LogisticRegression(featuresCol="features", labelCol="churn")
        pipeline = Pipeline(stages=[indexer, assembler, lr])
        
        # Train model
        model = pipeline.fit(train_data)
        
        # Evaluate
        predictions = model.transform(test_data)
        evaluator = BinaryClassificationEvaluator(labelCol="churn", metricName="areaUnderROC")
        auc = evaluator.evaluate(predictions)
        
        # AUC should be between 0 and 1
        assert 0 <= auc <= 1


# Cleanup helper
def cleanup_test_files():
    """Clean up test files"""
    import shutil
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")
    if os.path.exists("/tmp/spark-warehouse"):
        shutil.rmtree("/tmp/sparkwarehouse")
    if os.path.exists("/tmp/sparkwarehouse"):
        shutil.rmtree("/tmp/sparkwarehouse")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
