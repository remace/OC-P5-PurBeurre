from actions_db.cursor_Wrapper import CursorWrapper
from model.Item import Item


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


class Category:

    @classmethod
    def from_rows(cls, rows):
        items = []
        for row in rows:
            items.append(cls(row))
        return items

    @property
    def to_dict(self):
        as_dict = {}
        for name, value in self.__dict__.items():
            if not name.startswith('_') and not callable(value):
                as_dict[name] = value
        return as_dict

    def __init__(self, row: tuple):
        self.id = row[0]
        self.name = row[1]



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
                'nutrients': item[5],
                'nutriscore': item[6],
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
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM mydb.favourites INNER JOIN mydb.foods ON mydb.favourites.food_id = mydb.foods.food_id "
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        favourites_list = cursor.fetchall()
        favourites = []
        for item in favourites_list:
            food_dict = {
                'food_id': item[0],
                'category_id': item[1],
                'name': item[2],
                'ingredients': item[3],
                'additives': item[4],
                'nutrients': item[5],
                'nutriscore': item[6],
                'labels': item[7],
                'stores': item[8],
                'barcode': item[9],
                'url': item[10],
                'favourite': is_favourite_in_db(item[0])
            }
            favourite = Item(food_dict)
            favourites.append(favourite)
    return favourites


def set_favourite(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "INSERT INTO mydb.favourites (food_id) VALUES ({})".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=True)


def reset_favourite(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "DELETE FROM mydb.favourites WHERE food_id ={}".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=True)


def is_favourite_in_db(food_id):
    cursor_wrapper = CursorWrapper()
    sql = "SELECT * FROM mydb.favourites WHERE food_id = {}".format(food_id)
    with cursor_wrapper as cursor:
        cursor.execute(sql, commit=False)
        item_list = cursor.fetchall()
    return bool(item_list)


if __name__ == '__main__':

    print(get_favourites())

    # scores = f"SELECT * FROM mydb.foods WHERE category_id={id} AND nutriscore < '{ns}';"
