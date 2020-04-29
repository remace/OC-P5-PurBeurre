from mysql import connector
import mysql.connector

DB_USER = 'root'
DB_HOST = 'localhost'
DB_PASSWORD = 'root'
DB_DATABASE = 'mydb'
DB_AUTH_PLUGIN = 'mysql_native_password'

# mydb = mysql.connector.connect(
#     host=DB_HOST,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     database=DB_DATABASE,
#     auth_plugin=DB_AUTH_PLUGIN
# )


class CursorWrapper:

    @property
    def db(self):
        if not self._db or self._reload:
            self._db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE,
                auth_plugin=DB_AUTH_PLUGIN
            )
            self._reload = False
        return self._db

    def __init__(self):
        self._db = None
        self.cursor = None
        self._reload = False

    def reload(self):
        self._reload = True

    def close(self):
        try:
            self._db.close()
        except (AttributeError, TypeError, Exception):
            pass

    def _execute(self, sql, multi=False, commit=True, *args, **kwargs):
        result = self.cursor.execute(sql, multi=multi, *args, **kwargs)
        commit and self.db.commit()
        return result

    def execute(self, sql: str, *args, **kwargs):
        return self._execute(sql, multi=False, *args, **kwargs)

    def execute_many(self, sql: str, *args, **options):
        return self._execute(sql, multi=True, *args, **options)

    def __enter__(self):
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
        except (Exception,) as error:
            print('Issue while closing cursor',  str(error))
        pass

    def __getattr__(self, attribute):
        return getattr(self.cursor, attribute)