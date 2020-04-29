from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from actions_db import dbread
from model.Item import Item
import webbrowser


class ItemView(Screen):
    name = ObjectProperty(None)
    ingredients = ObjectProperty(None)
    additives = ObjectProperty(None)
    nutriscore = ObjectProperty(None)
    nutrients = ObjectProperty(None)
    labels = ObjectProperty(None)
    stores = ObjectProperty(None)
    barcode = ObjectProperty(None)
    url = ObjectProperty(None)
    favourite = ObjectProperty(None)

    def __init__(self, item_id=None):
        super().__init__()
        if item_id:
            item_dict = dbread.get_item(item_id)
            self.item = Item(item_dict)
            self.name.text = self.item.food_name
            self.ingredients.text = self.item.ingredients
            self.additives.text = self.item.additives
            self.nutriscore.text = self.item.nutriscore
            self.nutrients.text = self.item.nutrients
            self.labels.text = self.item.labels
            self.stores.text = self.item.stores
            self.barcode.text = str(self.item.barcode)
            self.url.text = "lien vers Open Food Facts"
            self.favourite.text = "supprimer des favoris" if self.item.is_favourite() else "ajouter aux favoris"

    def update(self, item_id):
        item_dict = dbread.get_item(item_id)
        self.item = Item(item_dict)

        self.name.text = self.item.food_name
        self.ingredients.text = self.item.ingredients
        self.additives.text = self.item.additives
        self.nutriscore.text = self.item.nutriscore
        self.nutrients.text = self.item.nutrients
        self.labels.text = self.item.labels
        self.stores.text = self.item.stores
        self.barcode.text = str(self.item.barcode)
        self.url.text = "lien vers Open Food Facts"
        self.favourite.text = "supprimer des favoris" if self.item.is_favourite() else "ajouter aux favoris"


    def click_link(self):
        webbrowser.open(self.item.url)

    def click_favourite(self):
        self.item.favourite = not(self.item.favourite)
        # TODO répercuter le changement en DB

        self.favourite.text =  "supprimer des favoris" if self.item.is_favourite() else "ajouter aux favoris"


