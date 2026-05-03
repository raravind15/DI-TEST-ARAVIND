import logging
from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig,SourceFormat,WriteDisposition

logger=logging.getLogger("__name__")

def load_bigquery_table(project_id,bucket_name,dataset,table,file_name,loadtype):
    logger.info("Loading process started")
    client=bigquery.Client(project_id)
    table=client.dataset(dataset).table(table)
    job_config=LoadJobConfig(source_format=SourceFormat.PARQUET,write_disposition=WriteDisposition.WRITE_APPEND if "load_type"=="write_append" else WriteDisposition.WRITE_TRUNCATE)
    uri=f"gs://{bucket_name}/{file_name}"
    load_job=client.load_table_from_uri(uri,table,job_config=job_config)
    load_job.result()
    rows_loaded=load_job.output_rows
    logger.info("Load Completed")
    return rows_loaded
