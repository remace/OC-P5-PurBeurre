from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from user_interface import itemLists
from user_interface import itemView
from user_interface.mixins import CallbackMixin


class FoodsListItem(CallbackMixin, FloatLayout):
    name = ObjectProperty()
    details_btn = ObjectProperty()
    favourite_btn = ObjectProperty()

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.name.text = self.item.food_name
        self.favourite_btn.text = "supprimer des favoris" if self.item.favourite else "ajouter aux favoris"

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
        view = itemView.ItemView(self.item.food_id)
        next_screen.add_widget(view)
        manager.current = 'item'

    # def on_click_fav(self):
    #     self.item.favourite = not self.item.favourite
    #     if self.item.favourite:
    #         dbread.set_favourite(self.item.food_id)
    #     else:
    #         dbread.reset_favourite(self.item.food_id)
    #     self.fav_btn.text = "supprimer des favoris" if self.item.favourite else "ajouter aux favoris"


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
