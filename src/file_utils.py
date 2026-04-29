import logging
from datetime import datetime
from google.cloud import storage
import re
from config import CONFIG

logging.basicConfig(level=logging.INFO,format=f"%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)

logging.info("Testing")

def get_gcs_client(project_id):
    return storage.Client(project=project_id)

def list_files(project_id,bucket_name,prefix):
    client=get_gcs_client(project_id)
    bucket=client.bucket(bucket_name)
    files_blob=bucket.list_blobs(prefix=prefix)
    file_names=[]

    for files in files_blob:
        file_names.append(files.name)
    
    return file_names

files=list_files(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["landing_prefix"])

print(files)