from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from user_interface import itemLists
from user_interface import itemView


class FoodsListItem(FloatLayout):
    name = ObjectProperty()
    details_btn = ObjectProperty()
    fav_btn = ObjectProperty()

    def __init__(self, item):
        super().__init__()

        self.item_id = item['id']
        self.name = item['name']
        # self.fav_btn.text = "supprimer des favoris" if item.favourite else "ajouter aux favoris"
        self.fav_btn.text = "ajouter aux favoris"

    @property
    def manager(self):
        parent = self
        manager = None
        while manager is None:
            parent = getattr(parent, 'parent')
            manager = getattr(parent, 'manager', None)
        return manager

    def on_click_details(self):
        manager = self.manager
        next_screen = manager.get_screen('item')
        next_screen.clear_widgets()
        view = itemView.ItemView(self.item_id)
        next_screen.add_widget(view)
        manager.current = 'item'

    def on_click_fav(self):

        pass


class CategoryListItem(FloatLayout):

    btn = ObjectProperty()

    @property
    def manager(self):
        parent = self
        manager = None
        while manager is None:
            parent = getattr(parent, 'parent')
            manager = getattr(parent, 'manager', None)
        return manager

    def __init__(self, category_dict):
        super().__init__()
        self.category_id = category_dict['id']
        self.build_layout(category_dict)

    def build_layout(self, category_dict):
        self.btn.text = category_dict['name']

    def category_click(self):
        manager = self.manager
        next_screen = manager.get_screen('foods')
        next_screen.clear_widgets()
        view = itemLists.FoodsList(self.category_id)
        next_screen.add_widget(view)
        manager.current = 'foods'

    def create_view(self):
        return itemLists.FoodsList(self.category_id)
