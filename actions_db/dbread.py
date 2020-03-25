import mysql.connector

db_user = 'root'
db_host = 'localhost'
db_password = 'root'
db_database = 'mydb'
db_auth_plugin = 'mysql_native_password'

mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database,
    auth_plugin='mysql_native_password'
)


class CursorWrapper:

    def __init__(self, db):
        self.db = db
        self.cursor = None

    def execute(self, sql):
        result = self.cursor.execute(sql)
        return result

    def __enter__(self):
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
        except(Exception,) as error:
            print('issue while closing cursor', str(error))

    def __getattr__(self, attribute):
        return getattr(self.cursor, attribute)


def get_categories():
    cursor_wrapper = CursorWrapper(mydb)
    sql = "SELECT category_id, category_name from categories"
    with cursor_wrapper as cursor:
        cursor.execute(sql)
        categories_tuple = cursor.fetchall()
        categories = []
        for cat in categories_tuple:
            categorie = {'id': cat[0], 'name': cat[1]}
            categories.append(categorie)
    return categories


def get_foods(category_id):
    cursor_wrapper = CursorWrapper(mydb)
    sql = "SELECT food_id, food_name FROM foods WHERE category_id = {}".format(category_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql)
        categories_tuple = cursor.fetchall()
        categories = []
        for cat in categories_tuple:
            categorie = {'id': cat[0], 'name': cat[1]}
            categories.append(categorie)
    return categories


def get_food(food_id):
    cursor_wrapper = CursorWrapper(mydb)
    sql = "SELECT * FROM foods WHERE food_id = {}".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql)
        cat = cursor.fetchall()
        categorie = {
            'id': cat[0][0],
            'name': cat[0][2],
            'category_id': cat[0][1],
            'ingredients': cat[0][3],
            'additives': cat[0][4],
            'nutriscore': cat[0][5],
            'nutrients': cat[0][6],
            'labels': cat[0][7],
            'stores': cat[0][8],
            'barcode': cat[0][9],
            'url': cat[0][10],
        }
    return categorie


def get_favourites():
    pass


def set_favourite(food_id):
    pass


if __name__ == '__main__':
    print(get_foods(2))
