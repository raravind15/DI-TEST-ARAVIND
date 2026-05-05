from datetime import datetime
import file_utils as file_utils
import validators
from config import CONFIG
import logging
import loader
import json
import uuid

logger=logging.getLogger("__name__")
    

def capture_final_metrics(job_name,batch_id,file_name,file_row_count,start_time,end_time,rows_loaded,job_status,error_msg):
    metrics={
        "job_name":job_name,
        "batch_id":batch_id,
        "file_name":file_name,
        "file_row_count":file_row_count,
        "start_time":start_time.isoformat(),
        "end_time":end_time.isoformat(),
        "rows_loaded":rows_loaded,
        "job_status":job_status,
        "error_msg":error_msg
    }

    logger.info(f"Final metrics:{json.dumps(metrics)}")
    return metrics

def main():
    print("Started Process")
    job_name="Employees_load"
    batch_id=str(uuid.uuid4())
    file_name=None
    start_time=datetime.now()
    end_time=datetime.now()
    job_status="Success"
    error_message='N/A'
    row_count=None
    rows_loaded=None

    try:
        file_name,row_count=validators.file_validation(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["landing_prefix"])
        validators.data_validation(CONFIG["project_id"],CONFIG["landing_bucket"],file_name,CONFIG["mandatory_columns"],CONFIG["mandatory_non_null_columns"])
        rows_loaded=loader.load_bigquery_table(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["dataset"],CONFIG["table"],file_name,CONFIG["load_type"])
        if CONFIG["row_count_validation"]:
            if abs(row_count-rows_loaded)>CONFIG["row_count_threshold"]:
                raise ValueError("Some records are not loaded")
        logger.info(f"File movement started")
        if file_name:
            file_utils.move_file(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["archive_bucket"],file_name,CONFIG["landing_prefix"])
            logger.info(f"File moved to archive bucket")
        else:
            logger.info(f"No file to move")
    except Exception as e:
        job_status="Failure"
        error_message=str(e)
        end_time=datetime.now()
        logger.error(f"error:{error_message}")
        if file_name:
            file_utils.move_file(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["error_bucket"],file_name,CONFIG["landing_prefix"])
            logger.info(f"File moved to error bucket")
        else:
            logger.info(f"No file to move")
    end_time=datetime.now()
    capture_final_metrics(job_name,batch_id,file_name,row_count,start_time,end_time,rows_loaded,job_status,error_message)


if __name__=="__main__":
    main()