import os

#config database
app_env = os.environ.get('DEV_DB')

if app_env == "True":
    DB_USER = 'PurBeurre'
    DB_HOST = '192.168.1.112'
    DB_PASSWORD = 'PurBeurre'
    DB_DATABASE = 'PurBeurre'
    DB_AUTH_PLUGIN = 'mysql_native_password'
else:
    DB_USER = 'PurBeurre'
    DB_HOST = 'localhost'
    DB_PASSWORD = 'PurBeurre'
    DB_DATABASE = 'PurBeurre'
    DB_AUTH_PLUGIN = 'mysql_native_password'

# data size for the local database
MAX_PAGE_COUNT = 1 # API page count. there are 20 product in each API page.
MAX_CATEGORIES = 5
