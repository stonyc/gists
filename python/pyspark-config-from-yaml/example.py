#/usr/bin/env python

"""Example PySpark script using loaded configuration file.

Usage:
    example.py (-d DATE) [options]

Options:
    -d, --date=DATE		Target date in yyyyMMdd format

"""

from datetime import datetime
from docopt import docopt
from common import spark_conf, logger

import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession

def main()

    # Enter code here.
    pass


if __name__ == "__main__":

    # Extract input arguments:
    args = docopt(__doc__)

    conf = SparkConf()
    conf.setAppName(f"pyspark-job-name")
    conf.getAll()
    # Iteratively add pre-configured parameters to the SparkSession:
    for parameter, value in spark_conf.items():
        conf.set(parameter, value)

    conf.set("spark.sql.pivotMaxValues", "100000")
    conf.set("javax.jdo.option.ConnectionURL", "<METASTORE>"")
    conf.set("spark.sql.warehouse.dir", "<WAREHOUSE_HDFS_PATH>")

    # Define number of executors instances and partitioning:
    NUM_INSTANCES = ...  # Replace with number of required workers.
    conf.set("spark.executor.instances", f"{NUM_INSTANCES}")

    spark = SparkSession.builder.enableHiveSupport().config(conf=conf).getOrCreate()
    sc = spark._sc

    main()
