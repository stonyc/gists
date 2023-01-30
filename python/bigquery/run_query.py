from datetime import datetime
from string import Template
from typing import NamedTuple, Optional, Any, Dict, Callable, NoReturn
from google.cloud import bigquery


# Define logger format:
LOG_FORMAT = "[%(asctime)s %(name)s %(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("MAIN")
logger.setLevel(logging.DEBUG)


QueryString = str

# Replace with user-defined parameters:
_JobLabels = {
    "team": "<team_name>",
    "job_type": "<job_type>",
    "component_group": "<component_group>",
    "component": "<script_name>",
}


class ConnectInfo(NamedTuple):
    host: str
    port: int = 10000


def read_sql(sql_file) -> Optional[str]:
    try:
        logger.info(f"Read raw sql query file : {sql_file}")
        with open(sql_file, 'r') as file:
            query = file.read()
        return query
    except IOError:
        return None


def substitute_query_with_dict(raw_query: str, query_variables: Dict[str, Any], safe_substitute: bool = False) -> str:
    logger.info(f"Substitute Variables in raw sql query... (Safe_substitute : {safe_substitute})")
    if safe_substitute:
        query = Template(raw_query).safe_substitute(query_variables)
    else:
        query = Template(raw_query).substitute(query_variables)
    return query


def bigquery_runner(config: Optional[Dict[str, Any]] = None):
    client = bigquery.Client()
    query_config: Optional[bigquery.QueryJobConfig] = None
    if config:
        query_config = bigquery.QueryJobConfig(labels=_JobLabels, **config)
    else:
        query_config = bigquery.QueryJobConfig(labels=_JobLabels)

    logger.debug(f"Query Config : {query_config.to_api_repr()}")

    def _run_query(query: QueryString):
        logger.info(f"Run Query : \n{query}")
        start_time = datetime.now()
        query_job = client.query(query, job_config=query_config)

        # wait for job finish
        res = query_job.result()

        elapsed = (datetime.now() - start_time).total_seconds() / 60
        logger.debug(f"Query Processed: {elapsed:.2f} min elapsed. "
                     f"{query_job.total_bytes_processed} bytes Processed "
                     f"({query_job.total_bytes_billed} bytes billed)")
        return res

    return _run_query

