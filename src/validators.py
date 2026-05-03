import logging
from datetime import datetime
import file_utils
import re
import os
import tempfile
from config import CONFIG
import pyarrow.parquet as pq

logger=logging.getLogger("__name__")

def file_validation(project_id,bucket_name,prefix):
    logger.info("File Validation Started")
    all_files=file_utils.list_files(project_id,bucket_name,prefix)
    #valid files
    valid_files=[f for f in all_files if re.findall(r"employees_\d{8}.parquet$",f,re.IGNORECASE)]
    if not valid_files:
        raise ValueError(f"No valid file in {bucket_name}")
    #multi files check
    if len(valid_files)>1 and not CONFIG["multiple_files_allowed"]:
       raise ValueError(f"Multiple files are in {bucket_name}")
    valid_file=valid_files[0]
    valid_file_name=valid_file.split("/")[-1]
    #extension check
    if not [valid_file_name.lower().endswith(ext) for ext in CONFIG["allowed_extensions"]]:
        raise ValueError(f"File with this extension {valid_file_name} is not allowed")
    #pattern
    match=re.fullmatch(r"employees_(\d{8}).parquet",valid_file_name)
    if not match:
        raise ValueError(f"File {valid_file_name} pattern not correct")
    #date validation
    date_str=match.group(1)
    try:
        datetime.strptime(date_str,"%Y%m%d")
    except Exception as e:
        logger.error(f"File({valid_file_name}) has invalid date")
    
    # empy file check
    try:
        file=file_utils.download_file(project_id,bucket_name,valid_file)
        emp_table=pq.read_table(file)
        row_count=emp_table.num_rows
        print(row_count)

        if row_count==0 and CONFIG["reject_empty_file"]:
            raise ValueError(f"File({valid_file_name} is empty)")
        logger.info("File Validation successfully completed")
        return valid_file,row_count
    except Exception as e:
        raise ValueError(str(e)) 
    finally:
        os.unlink(file)
    

def data_validation(project_id,bucket_name,file_name,mandatory_columns,mandatory_non_null_columns):
    logger.info("Data Validation Started")
    file=file_utils.download_file(project_id,bucket_name,file_name)
    try:
        table=pq.read_table(file)
        actual_columns=table.column_names
        actual_lower={ac.lower(): ac for ac in actual_columns }
        missing_columns=[col for col in mandatory_columns if col.lower() not in actual_lower]
        if missing_columns:
            raise ValueError("Missing mandatory columns")
        for col in mandatory_non_null_columns:
            actual_col=actual_lower[col.lower()]
            column=table.column(actual_col)
            if column.null_count>0:
                raise ValueError(f"mandatory column:{col} has null values")
    except Exception as e:
        logger.error(f"Data validation failed:{str(e)}")
    else:
        logger.info("Data Validation successfully completed")
    finally:
        os.unlink(file)
        
