import cx_Oracle

from database import settings


def run(query):
    connection = cx_Oracle.connect(user=settings.DS_EXADATA_user,
                                   password=settings.DS_EXADATA_password,
                                   dsn=settings.DS_EXADATA_CONN_SID)
    cursor = connection.cursor()
    return cursor.execute(query)
