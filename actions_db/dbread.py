from actions_db.cursor_Wrapper import CursorWrapper
from model.Item import Item, Favourite
from model.Category import Category


def get_categories():
    cursor_wrapper = CursorWrapper()
    sql = "SELECT category_id, category_name from categories"
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        categories_tuple = cursor.fetchall()
    categories = []
    for cat in categories_tuple:
        categorie = {'id': cat[0], 'name': cat[1]}
        categories.append(categorie)
    return categories

def get_foods(category_id):
    cursor_wrapper = CursorWrapper()
    sql = "SELECT food_id, food_name FROM foods WHERE category_id = {}".format(category_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        # categories_tuple = cursor.fetchall()
        categories = Category.from_rows(cursor.fetchall())
        # categories = []
        # for cat in categories_tuple:
        #     categorie = {'id': cat[0], 'name': cat[1]}
        #     categories.append(categorie)
    return categories


def get_foods_as_list_of_objects(category_id):
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM foods WHERE category_id = {}".format(category_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        foods_tuple = cursor.fetchall()
        foods = []
        for item in foods_tuple:
            food_dict = {
                'food_id': item[0],
                'category_id': item[1],
                'name': item[2],
                'ingredients': item[3],
                'additives': item[4],
                'nutrients': item[6],
                'nutriscore': item[5],
                'labels': item[7],
                'stores': item[8],
                'barcode': item[9],
                'url': item[10],
                'favourite': is_favourite_in_db(item[0])
            }
            food = Item(food_dict)
            foods.append(food)
    return foods


def get_item(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM PurBeurre.foods WHERE food_id = {}".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        item_list = cursor.fetchall()
        item_dict = {
            'food_id': item_list[0][0],
            'category_id': item_list[0][1],
            'name': item_list[0][2],
            'ingredients': item_list[0][3],
            'additives': item_list[0][4],
            'nutriscore': item_list[0][5],
            'nutrients': item_list[0][6],
            'labels': item_list[0][7],
            'stores': item_list[0][8],
            'barcode': item_list[0][9],
            'url': item_list[0][10],
        }
    return item_dict


def get_favourites():
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM PurBeurre.favourites INNER JOIN PurBeurre.foods ON PurBeurre.favourites.food_id = PurBeurre.foods.food_id "
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        favourites_list = cursor.fetchall()
        favourites = []
        for item in favourites_list:
            food_dict = {
                'food_id': item[3],
                'category_id': item[4],
                'name': item[5],
                'ingredients': item[6],
                'additives': item[7],
                'nutrients': item[9],
                'nutriscore': item[8],
                'labels': item[10],
                'stores': item[11],
                'barcode': item[12],
                'url': item[13],
                'favourite': True
            }
            favourite = Favourite(food_dict, item[2])
            favourites.append(favourite)
    return favourites


def set_favourite(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "INSERT INTO PurBeurre.favourites (food_id) VALUES ({})".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=True)


def reset_favourite(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "DELETE FROM PurBeurre.favourites WHERE food_id ={}".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=True)


def is_favourite_in_db(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM PurBeurre.favourites WHERE food_id = {}".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        item_list = cursor.fetchall()
    return bool(item_list)


def get_substitutes(cat_id, nutriscore):
    cursor_wrapper = CursorWrapper()
    sql = f"SELECT * FROM PurBeurre.foods WHERE category_id={cat_id} AND nutriscore < '{nutriscore}' ORDER BY nutriscore;"
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        item_list = cursor.fetchall()
        items = []
        for item in item_list:
            item_dict = {
                'food_id': item[0],
                'category_id': item[1],
                'name': item[2],
                'ingredients': item[3],
                'additives': item[4],
                'nutrients': item[6],
                'nutriscore': item[5],
                'labels': item[7],
                'stores': item[8],
                'barcode': item[9],
                'url': item[10],
                'favourite': is_favourite_in_db(item[0])
            }
            food = Item(item_dict)
            items.append(food)
    return items


if __name__ == '__main__':
    items = get_favourites()
    for i in items:
        print(i)
