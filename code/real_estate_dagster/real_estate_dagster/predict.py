from dagster import job, op, OpExecutionContext
from pyspark.sql.types import StructType, StructField, DateType, DecimalType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor

@op(required_resource_keys={"pyspark"})
def predict_prices_op(context: OpExecutionContext, dependent_job=None):
    # Get SparkSession from the context
    spark = context.resources.pyspark.spark_session
    
    # Load data from the silver table
    silver_df = spark.sql("""
        SELECT
            area,
            rooms,
            size,
            type,
            FROM_UNIXTIME(list_time / 1000) AS date,
            price
        FROM warehouse.silver.silver_defined_data
    """)
    
    # Drop rows with null values, if any
    silver_df = silver_df.dropna()
    
    # Create features vector
    assembler = VectorAssembler(inputCols=["area", "rooms", "size", "type"], outputCol="features")
    silver_df = assembler.transform(silver_df)
    
    # Select features and target variable
    selected_features = ["features", "date"]
    target_variable = "price"
    
    # Split data into training and test sets
    (training_data, test_data) = silver_df.randomSplit([0.8, 0.2])
    
    # Train a Random Forest Regressor model
    rf = RandomForestRegressor(featuresCol="features", labelCol=target_variable)
    model = rf.fit(training_data)
    
    # Make predictions on the test data
    predictions = model.transform(test_data)
    
    # Select relevant columns for prediction results
    result_data = predictions.select("date", "prediction").collect()
    
    # Define schema for the result DataFrame
    schema = StructType([
        StructField('dt', DateType(), True),
        StructField('price_predicted', DecimalType(32,16), True)
    ])
    
    # Create DataFrame with specified schema
    result_df = spark.createDataFrame(result_data, schema)
    
    # Write DataFrame to Iceberg table
    result_df.writeTo("warehouse.silver.predicted_price_data") \
        .using("iceberg") \
        .tableProperty("write.format.default", "parquet") \
        .createOrReplace()
    
@job
def predict():
  predict_prices_op()