import cx_Oracle
import os

from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DS_EXADATA_HOST = config('DB_HOST')
DS_EXADATA_PORT = config('DB_PORT')
DS_EXADATA_SN = config('DB_SN')
DS_EXADATA_user = config('DB_USER')
DS_EXADATA_password = config('DB_PASSWORD')

DS_EXADATA_CONN_SID = cx_Oracle.makedsn(
    DS_EXADATA_HOST,
    DS_EXADATA_PORT,
    service_name=DS_EXADATA_SN)
