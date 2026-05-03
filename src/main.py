import file_utils as file_utils
import validators
from config import CONFIG
import logging
import loader

logger=logging.getLogger("__name__")

def main():
    print("Started Process")
    try:
        file_name,row_count=validators.file_validation(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["landing_prefix"])
        validators.data_validation(CONFIG["project_id"],CONFIG["landing_bucket"],file_name,CONFIG["mandatory_columns"],CONFIG["mandatory_non_null_columns"])
        loader.load_bigquery_table(CONFIG["project_id"],CONFIG["landing_bucket"],CONFIG["dataset"],CONFIG["table"],file_name,CONFIG["load_type"])
    except Exception as e:
        error_message=str(e)
        logger.error(f"error:{error_message}")


if __name__=="__main__":
    main()