from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from user_interface import itemLists
from user_interface.mixins.favorite import FavoriteMixin
from user_interface.mixins.substitute import SubstituteMixin
from user_interface.mixins.details import DetailsMixin
from user_interface.mixins.properties import PropertiesMixin


class FoodsListItem(PropertiesMixin, FavoriteMixin,
                    SubstituteMixin, DetailsMixin, FloatLayout):
    name = ObjectProperty()
    details_btn = ObjectProperty()
    favourite_btn = ObjectProperty()
    image = ObjectProperty()

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.name.text = self.item.food_name
        self.image.source = "./ressources/img/unfav_icon.png" if self.item.favourite else "./ressources/img/fav_icon.png"
        self.favourite_btn.background_color = (1, 0, 0, 1) if self.item.favourite else (0, 1, 0, 1)



class SubstituteListItem(PropertiesMixin, FavoriteMixin, DetailsMixin, FloatLayout):

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.name.text = str(self.item.food_name)
        self.image.source = "./ressources/img/unfav_icon.png" if self.item.favourite else "./ressources/img/fav_icon.png"
        self.favourite_btn.background_color = (1, 0, 0, 1) if self.item.favourite else (0, 1, 0, 1)


class CategoryListItem(PropertiesMixin, FloatLayout):

    btn = ObjectProperty()

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




