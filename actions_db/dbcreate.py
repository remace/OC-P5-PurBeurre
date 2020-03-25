import mysql.connector
import requests
import json

db_user = 'root'
db_host = 'localhost'
db_password = 'root'
db_database = 'mydb'
db_auth_plugin = 'mysql_native_password'

mydb = None


def connect():
    global mydb
    print()
    is_not_connected = (mydb and not mydb.is_connected())

    if is_not_connected or not mydb:
        try:
            mydb.close()
        except Exception as error:
            print(f'[{type(error).__name__}] {error}')
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database,
            auth_plugin='mysql_native_password'
        )
    return mydb
    # return mysql.connector.connect(
    #         host=db_host,
    #         user=db_user,
    #         password=db_password,
    #         database=db_database,
    #         auth_plugin='mysql_native_password'
    #     )


categories_size = 50
PRODUCT_PAGE_NUMBER = 1

categories_url = 'https://fr.openfoodfacts.org/categories.json'
search_url = 'https://fr.openfoodfacts.org/cgi/search.pl'


class Food:
    def __init__(self,
                 food_name,
                 category_id,
                 ingredients,
                 additives,
                 nutriscore,
                 nutrient,
                 label,
                 stores,
                 barcode,
                 url):
        self.food_name = food_name
        self.category_id = category_id
        self.ingredients = ingredients
        self.additives = additives
        self.nutriscore = nutriscore
        self.nutrient = nutrient
        self.label = label
        self.stores = stores
        self.barcode = barcode
        self.url = url


class CursorWrapper:

    @property
    def db(self):
        return connect()

    def __init__(self):
        self.cursor = None

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
        # try:
        #     self.cursor.close()
        # except (Exception,) as error:
        #     print('Issue while closing cursor',  str(error))
        pass

    def __getattr__(self, attribute):
        return getattr(self.cursor, attribute)


def get_categories(notifier=None):
    r = requests.get(categories_url)
    categories_json = r.json()
    categories = []
    category_sql = "INSERT INTO categories (category_name) VALUES (\"{name}\");"
    product_sql = (
        "INSERT INTO foods ("
        "category_id, "
        "food_name, "
        "ingredients,"
        "additives,"
        "nutriscore,"
        "nutrient,"
        "label,"
        "store,"
        "barcode,"
        "url) "
        "VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"); "
    )

    notifier('start processing...')
    cursor_wrapper = CursorWrapper()

    for i in range(categories_size):
        category_name = categories_json["tags"][i]["name"]
        categories.append({
            "name": category_name,
            "url": categories_json["tags"][i]["url"]
        })
        # ajouter la categorie à la BDD, en récupérant son ID via le cursor
        with cursor_wrapper as cursor:
            cursor.execute(category_sql.format(name=category_name))
            category_id = cursor.lastrowid

        foods = get_foods(categories[i]["url"], category_id)

        operations = []
        for j in foods:
            category_id = j.category_id
            food_name = str(j.food_name)[:999]
            ingredients = str(j.ingredients)[:999]
            additives = str(j.additives)[:999]
            nutriscore = j.nutriscore
            nutrient = str(j.nutrient)[:999]
            label = str(j.label)[:999]
            stores = str(j.stores)[:999]
            barcode = j.barcode
            url = str(j.url)[:999]

            operation = product_sql.format(
                category_id,
                food_name,
                ingredients,
                additives,
                nutriscore,
                nutrient,
                label,
                stores,
                barcode,
                url)

            try:
                if operation:
                    operations.append(operation)
                else:
                    print(operation)
            except(Exception,)as e:
                print(f"erreur de contenu avant insertion:", e)
                print(operation)

        with cursor_wrapper as cursor:
            try:
                cursor.execute_many('\n'.join(operations))
                notifier and notifier(f'Category {category_name} processed')
            except(Exception,) as e:
                print(f"erreur de contenu: le curseur contient une requête vide:", e)
                print(operations)


def get_foods(category_url, category_id):
    foods = []
    # envoyer la requête
    for i in range(PRODUCT_PAGE_NUMBER):
        r = requests.get(category_url + ".json")
        foods_json = r.json()

        for j in (foods_json.get("products") or []):

            barcode = j.get("code")
            food_name = j.get("product_name_fr")
            nutriscore = j.get("nutriscore_grade")
            if nutriscore not in ['a','b','c','d','e']:
                nutriscore = 'f'

            if not all([barcode, food_name, nutriscore]):
                continue

            f = Food(
                food_name=food_name,
                category_id=category_id,
                ingredients=j.get("ingredients_text"),
                additives=j.get("additives_original_tags"),
                nutriscore=nutriscore,
                nutrient=j.get("nutrient_levels"),
                label=j.get("labels"),
                stores=j.get("stores"),
                barcode=barcode,
                url="https://fr.openfoodfacts.org/api/v0/product/" + barcode
            )
            foods.append(f)
    return foods


def empty_db():
    cursor_wrapper = CursorWrapper()
    sql = [
        "SET FOREIGN_KEY_CHECKS = 0;",
        "TRUNCATE TABLE mydb.favourites;",
        "TRUNCATE TABLE mydb.foods;",
        "TRUNCATE TABLE mydb.categories;",
        "SET FOREIGN_KEY_CHECKS = 1;",
    ]

    for req in sql:
        with cursor_wrapper as cursor:
            result = cursor.execute(req)
        # for elem in result:
        #     print('elem', elem)
    print()


if __name__ == '__main__':
    empty_db()
