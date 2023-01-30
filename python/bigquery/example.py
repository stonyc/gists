#/usr/bin/env python

"""Example query using Python Client for BigQuery.

Usage:
    example.py <sql_file> [options]

Options:
    -d, --date=DATE		Target date in yyyyMMdd format

"""

from run_query import bigquery_runner, read_sql, substitute_query_with_dict
from docopt import docopt
from json import dumps
from typing import List, Any

from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound


def list_to_value_str(l: List[Any] = []) -> str:
    s = f"({dumps(l)[1:-1]})"
    return s


def main():

    # Import SQL query from file:
    raw_query = read_sql(args['<sql_file>'])

    # Define Big Query parameters:
    project = "PROJECT"  # Replace with your GCP project.
    dataset = "DATASET"  # Replace with the BQ dataset.
    source_table = "TABLE1"  # Replace with source table name.
    target_table = "TABLE2"  # Replace with target table name.
    partition = args['--date']  # Replace with partition name.

    # Configure Big Query connection:
    client = bigquery.Client()
    bq_target_table = f"{project}.{dataset}.{target_table}${partition}"

    query_config = {
        'destination': bq_target_table,
        'write_disposition': bigquery.WriteDisposition.WRITE_TRUNCATE,
    }

    # Standardize query variables for execution:
    query_vars = {}
    query_vars.update({
        'GCP_PROJECT': project,
        'BQ_DATASET': dataset,
        'SOURCE_TABLE': source_table,
	'PARTITION': partition,
    })
    query_vars.update()
    query = substitute_query_with_dict(raw_query, query_vars, safe_substitute=True)

    try:
        table = client.get_table(bq_target_table)
    except NotFound:
        logger.warning("Target BQ table not found, configure new table.")
        query_config['time_partitioning'] = bigquery.table.TimePartitioning(
            type_=bigquery.table.TimePartitioningType.DAY,
            field=None,
            expiration_ms=None,
        )

    bq_query = bigquery_runner(config=query_config)
    bq_query(query)

if __name__ == "__main__":

    # Extract input arguments:
    args = docopt(__doc__)

    main()
