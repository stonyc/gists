# Execute PySpark script with cluster configuration loaded form configuration file:

```bash
SPARK_PYTHON_FILE="example.py"
SPARK_MASTER="yarn"
SPARK_OPTIONS="--master ${SPARK_MASTER} \
--queue=${QUEUE_NAME} \
--conf spark.executorEnv.PEX_ROOT=./.pex \
--executor-cores ${SPARK_EXECUTOR_CORES} \
--driver-memory ${SPARK_DRIVER_MEMORY} \
--executor-memory ${SPARK_EXECUTOR_MEMORY} \
--files ${PEX_FILE},common.py,config.yml"

spark-submit ${SPARK_OPTIONS} ${SPARK_PYTHON_FILE} -d 20230201
