import functools
import requests
import settings
from actions_db.cursor_Wrapper import CursorWrapper

CATEGORIES_SIZE = 5
PRODUCT_PAGE_COUNT = settings.MAX_PAGE_COUNT

categories_url = 'https://fr.openfoodfacts.org/categories.json'
search_url = 'https://fr.openfoodfacts.org/cgi/search.pl'

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
    "VALUES ({}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"); "
)


def norm(text, patterns='\n\r', replacement='  '):
    text = str(text)
    for idx, pattern in enumerate(patterns):
        text = text.replace(pattern, replacement[idx])
    return text


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
        self.food_name = norm(food_name)
        self.category_id = category_id
        self.ingredients = norm(ingredients)
        self.additives = norm(additives)
        self.nutriscore = norm(nutriscore)
        self.nutrient = norm(nutrient)
        self.label = norm(label)
        self.stores = norm(stores)
        self.barcode = norm(barcode)
        self.url = norm(url)


def get_categories(cursor_wrapper, notifier=None):
    r = requests.get(categories_url)
    categories_json = r.json()
    categories = []
    category_sql = "INSERT INTO categories (category_name) VALUES (\"{name}\");"

    notifier('start processing...')

    for i in range(CATEGORIES_SIZE):
        category_name = categories_json["tags"][i]["name"]
        categories.append({
            "name": category_name,
            "url": categories_json["tags"][i]["url"]
        })
        # ajouter la categorie à la BDD, en récupérant son ID via le cursor
        with cursor_wrapper as cursor:
            cursor.execute(category_sql.format(name=category_name))
            category_id = cursor.lastrowid

        get_foods(cursor_wrapper, categories[i]["url"], category_id, category_name, i, notifier=notifier)


def get_foods(cursor_wrapper, category_url, category_id, category_name, index, notifier=None):
    operations = []
    # envoyer la requête
    for page in range(1, PRODUCT_PAGE_COUNT+1):
        r = requests.get(category_url + "/" + str(page) + ".json")
        foods_json = r.json()

        for j in (foods_json.get("products") or []):
            barcode = j.get("code")
            food_name = j.get("product_name_fr")
            nutriscore = j.get("nutriscore_grade")
            if nutriscore not in ['a', 'b', 'c', 'd', 'e']:
                nutriscore = 'f'

            if not all([barcode, food_name, nutriscore]):
                continue

            food = Food(
                food_name=food_name,
                category_id=category_id,
                ingredients=j.get("ingredients_text") or '',
                additives=j.get("additives_original_tags") or '',
                nutriscore=nutriscore,
                nutrient=j.get("nutrient_levels") or '',
                label=j.get("labels") or '',
                stores=j.get("stores") or '',
                barcode=barcode,
                url="https://fr.openfoodfacts.org/api/v0/product/" + barcode
            )

            category_id = food.category_id
            food_name = str(food.food_name)[:999]
            ingredients = str(food.ingredients)[:999]
            additives = str(food.additives)[:999]
            nutriscore = food.nutriscore
            nutrient = str(food.nutrient)[:999]
            label = str(food.label)[:999]
            stores = str(food.stores)[:999]
            barcode = food.barcode
            url = str(food.url)[:999]

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
            # operations.append(operation)

            with cursor_wrapper as cursor:
                try:
                    cursor.execute(operation)
                    notifier and notifier(f'Category {category_name} processed {index + 1}/{CATEGORIES_SIZE}')
                except(Exception,) as e:
                    print(f"erreur de contenu: le curseur contient une requête vide:", e)
                    print(operations)


def empty_db(cursor_wrapper):
    sql = "DELETE FROM PurBeurre.categories WHERE category_id >= 0 ;"   # todo soutien BDD

    with cursor_wrapper as cursor:
        _ = cursor.execute(sql, commit=True)


def process_update(notifier=print):
    wrapper = CursorWrapper()
    empty_db(wrapper)
    wrapper.reload()
    get_categories(wrapper, notifier=notifier)
    wrapper.close()


if __name__ == '__main__':
    process_update()
