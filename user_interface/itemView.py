from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from actions_db import dbread
from model.Item import Item
from user_interface.mixins import CallbackMixin

import webbrowser


class ItemView(CallbackMixin, Screen):
    name = ObjectProperty(None)
    ingredients = ObjectProperty(None)
    additives = ObjectProperty(None)
    nutriscore = ObjectProperty(None)
    nutrients = ObjectProperty(None)
    labels = ObjectProperty(None)
    stores = ObjectProperty(None)
    barcode = ObjectProperty(None)
    url = ObjectProperty(None)
    favourite_btn = ObjectProperty(None)

    def __init__(self, item_id=None):
        super().__init__()
        if item_id:
            item_dict = dbread.get_item(item_id)
            item_dict['favourite'] = dbread.is_favourite_in_db(item_dict['food_id'])
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
            self.favourite_btn.text = "supprimer des favoris" if self.item.favourite else "ajouter aux favoris"

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
        self.favourite_btn.text = "supprimer des favoris" if self.item.favourite else "ajouter aux favoris"

    def click_link(self):
        webbrowser.open("https://fr.openfoodfacts.org/produit/"+str(self.item.barcode))