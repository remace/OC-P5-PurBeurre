import mysql.connector
import requests
import json

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

categories_size = 50

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

    def __init__(self, db):
        self.db = db
        self.cursor = None

    def _execute(self, sql, many=False, *args, **kwargs):
        # print('sql =>', sql)
        # print('ARGS =>', args)
        # print('KWARGS =>', kwargs)
        if many:
            for line in sql:
                result = self.cursor.execute(line, *args, **kwargs)
        else:
            result = self.cursor.execute(sql, *args, **kwargs)
        self.db.commit()
        return result

    def execute(self, sql, *args, **kwargs):
        return self._execute(sql, many=False, *args, **kwargs)

    def execute_many(self, sql: list, *args, **options):
        return self._execute(sql, many=True, *args, **options)

    def __enter__(self):
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
        except (Exception,) as error:
            print('Issue while closing cursor',  str(error))

    def __getattr__(self, attribute):
        return getattr(self.cursor, attribute)


def get_categories():
    r = requests.get(categories_url)
    categories_json = r.json()
    categories = []
    category_sql = "INSERT INTO categories (category_name) VALUES (\"{name}\")"
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
        "VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") "
    )

    cursor_wrapper = CursorWrapper(mydb)

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

            try:
                operations.append(
                    product_sql.format(
                        j.category_id,
                        j.food_name[:999],
                        j.ingredients[:999],
                        j.additives[:999],
                        j.nutriscore[:999],
                        j.nutrient[:999],
                        j.label[:999],
                        j.stores[:999],
                        j.barcode,
                        j.url[:999])
                )
            except(Exception)as e:
                print(f"erreur de contenu avant insertion:", e)
        with cursor_wrapper as cursor:
            cursor.execute_many(operations)


def get_foods(category_url, category_id):
    foods = []
    # envoyer la requête
    for i in range(5):
        r = requests.get(category_url + ".json")
        foods_json = r.json()

        for j in (foods_json.get("products") or []):

            barcode = j.get("code")
            food_name = j.get("product_name_fr")
            nutriscore = j.get("nutriscore_score")

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


if __name__ == '__main__':
    get_categories()
