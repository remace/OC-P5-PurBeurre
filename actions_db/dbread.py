from actions_db.cursor_Wrapper import CursorWrapper


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
        categories_tuple = cursor.fetchall()
        categories = []
        for cat in categories_tuple:
            categorie = {'id': cat[0], 'name': cat[1]}
            categories.append(categorie)
    return categories


def get_item(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM mydb.foods WHERE food_id = {}".format(food_id)
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
    pass


def set_favourite(food_id):
    pass


if __name__ == '__main__':
    print (get_categories())
