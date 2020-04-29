
class Item:
    def __init__(self, item, **kwargs):
        self.food_id = item['food_id']
        self.category_id = item['category_id']
        self.food_name = item['name']
        self.ingredients = item['ingredients']
        self.additives = item['additives']
        self.nutrients = item['nutrients']
        self.nutriscore = item['nutriscore']
        self.labels = item['labels']
        self.stores = item['stores']
        self.barcode = item['barcode']
        self.url = item['url']
        self.favourite = item['favourite']
        # self.favourite = dbread.is_favourite_in_db(self.food_id)
