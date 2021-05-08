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

    def __str__(self):
        return f"{{ {self.food_id},{self.category_id},{self.food_name},{self.ingredients},{self.additives},{self.nutrients},{self.nutriscore},{self.labels},{self.stores},{self.barcode},{self.url},{self.favourite} }}"

    def __repr__(self):
        return f"{{ {self.food_id},{self.category_id},{self.food_name},{self.ingredients},{self.additives},{self.nutrients},{self.nutriscore},{self.labels},{self.stores},{self.barcode},{self.url},{self.favourite} }}"


class Favourite(Item):
    def __init__(self,item, created_at):
        super().__init__(item)
        self.created_at = created_at
