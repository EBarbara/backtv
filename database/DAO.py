import cx_Oracle

from database import settings


def run(query, params=None):
    connection = cx_Oracle.connect(user=settings.DS_EXADATA_user,
                                   password=settings.DS_EXADATA_password,
                                   dsn=settings.DS_EXADATA_CONN_SID,
                                   encoding="UTF-8",
                                   nencoding="UTF-8")
    cursor = connection.cursor()
    if params is None:
        return cursor.execute(query)
    return cursor.execute(query, params)
