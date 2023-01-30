# -*- coding: utf-8 -*-

import yaml
import os

from os.path import isfile


# Define logger format:
LOG_FORMAT = "[%(asctime)s %(name)s %(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("MAIN")
logger.setLevel(logging.DEBUG)


# Load default Spark configuration from YAML:
if isfile('config.yml'):
    spark_config_file = 'config.yml'
else:
    spark_config_file = f"{os.getenv('ROOT')}/conf/config.yml"  # Replace with hard path to configuration file.
logger.info(f"Read in default spark configuration : {spark_config_file}")
with open(spark_config_file) as f:
    spark_conf = yaml.load(f, Loader=yaml.SafeLoader)

