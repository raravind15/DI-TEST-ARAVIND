import logging
from datetime import datetime
from google.cloud import storage
import re
from config import CONFIG
import tempfile
import os
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


def download_file(project_id,bucket_name,file_name):
    client=get_gcs_client(project_id)
    bucket=client.bucket(bucket_name)
    file_blob=bucket.blob(file_name)
    temp_file=tempfile.NamedTemporaryFile(delete=False,suffix=".parquet")
    file_blob.download_to_file(temp_file)
    temp_file.close()
    return temp_file.name

def move_file(project_id,source_bucket,target_bucket,source_file,prefix):
    client=get_gcs_client(project_id)
    src_bkt=client.bucket(source_bucket)
    tgt_bkt=client.bucket(target_bucket)
    src_blob=src_bkt.blob(source_file)
    tgt_file=f"{prefix}/{source_file.split("/")[-1]}"
    tgt_blob=tgt_bkt.blob(tgt_file)
    tgt_blob.rewrite(src_blob)
    src_blob.delete()


