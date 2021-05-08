import os
app_env = os.environ.get('DEV')

if app_env == "DEV":
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
MAX_PAGE_COUNT = 1 # nombre de pages de l'API, il y a 20 produits par page
MAX_CATEGORIES = 5
