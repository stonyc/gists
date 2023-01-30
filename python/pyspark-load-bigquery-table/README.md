# Load BiqQuery table into PySpark Session:

**REQUIRES:** [spark-bigquery-connector](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)

Add GCP credentials to Spark Session:

```python
conf.set("credentialsFile", "<PATH-TO>/.config/gcloud/service-account.json")
conf.set("parentProject", "<GCP-PROJECT>")
conf.set("temporaryGcsBucket", '<GCS-BUCKET>')
```

When loading table from BQ, partition filter may be required:

```python
target_date = "2023-02-01"
sdf = spark.read.format("com.google.cloud.spark.bigquery")\  # Some people have found `bigquery` to be sufficient for this parameter.
                .option("table", "<GCP-PROJECT>.<BQ_DATASET>.<TABLE>") \
                .option("filter", f"partition_date = '{target_date}') \
                .load()
```

Modify `spark-submit` with JAR:

```bash
SPARK_PYTHON_FILE="example.py"
SPARK_MASTER="yarn"
SPARK_OPTIONS="--master ${SPARK_MASTER} \
--queue=${QUEUE_NAME} \
--conf spark.executorEnv.PEX_ROOT=./.pex \
--executor-cores ${SPARK_EXECUTOR_CORES} \
--driver-memory ${SPARK_DRIVER_MEMORY} \
--executor-memory ${SPARK_EXECUTOR_MEMORY} \
--jars ${PATH_TO}/spark-bigquery-with-dependencies_2.12-0.27.1.jar \
--files ${PEX_FILE},common.py,config.yml"

spark-submit ${SPARK_OPTIONS} ${SPARK_PYTHON_FILE} -d 20230201
```
