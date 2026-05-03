import os
from datetime import datetime
today_prefix=datetime.today().strftime('%Y/%m/%d')
# GCP Configuration
CONFIG = {
    'project_id': 'di-dev-aravind',
    'dataset': 'ds_raw_dev',
    'table': 'employees',
    'landing_bucket': 'aravind-de-dev-landing-asia-south1',
    'archive_bucket': 'aravind-de-dev-archive-asia-south1',
    'error_bucket': 'aravind-de-dev-error-asia-south1',
    'landing_prefix': f'employees/{today_prefix}',
    'file_pattern': 'employees_YYYYMMDD.parquet',
    'file_format': 'PARQUET',
    'load_type': 'WRITE_APPEND',
    'mandatory_columns': ['employee_id'],  # Columns that must exist
    'mandatory_non_null_columns': ['employee_id'],  # Columns that must not be null
    'row_count_validation': True,
    'row_count_threshold': 0,  # Exact match
    'reject_empty_file': True,
    'multiple_files_allowed': False,
    'allowed_extensions': ['.parquet'],
    'header_present': False,  # Not applicable for Parquet
    'delimiter': None,  # Not applicable for Parquet
}