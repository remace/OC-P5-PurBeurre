from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
import actions_db
from user_interface import buttons

from user_interface.mixins.properties import PropertiesMixin


class CategoryList(PropertiesMixin, FloatLayout):

    cat_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foods = actions_db.dbread.get_categories()
        self.build_layout()

    def build_layout(self):
        self.cat_layout.clear_widgets()
        for i in self.foods:
            self.cat_layout.add_widget(buttons.CategoryListItem(i))


class FoodsList(PropertiesMixin, FloatLayout):

    foods_layout = ObjectProperty()

    def __init__(self, iid=None):
        super().__init__()
        if iid:
            self.items = actions_db.dbread.get_foods_as_list_of_objects(iid)
            self.build_layout()

    def update_layout(self, iid):
        self.items = actions_db.dbread.get_foods(iid)
        self.update_layout()

    def build_layout(self):
        for i in self.items:
            self.foods_layout.add_widget(buttons.FoodsListItem(i))


class SubstitutesList(PropertiesMixin, FloatLayout):

    substitutes_layout = ObjectProperty()

    def __init__(self, cat_id=None, nutriscore=None):
        super().__init__()
        if cat_id and nutriscore:
            self.items = actions_db.dbread.get_substitutes(cat_id, nutriscore)
            self.build_layout()

    def build_layout(self):
        for item in self.items:
            self.substitutes_layout.add_widget(buttons.SubstituteListItem(item))

    def update_layout(self, cat_id, nutriscore):
        self.items = self.items = actions_db.dbread.get_substitutes(cat_id, nutriscore)
        if self.items:
            self.build_layout()


class FavouritesList(PropertiesMixin, FloatLayout):
    fav_layout = ObjectProperty()

    def __init__(self):
        super().__init__()
        self.items = actions_db.dbread.get_favourites()
        self.build_layout()

    def build_layout(self):
        self.fav_layout.clear_widgets()
        for item in self.items:
            self.fav_layout.add_widget(buttons.SubstituteListItem(item))

    def update_layout(self):
        self.items = actions_db.dbread.get_favourites()
        self.build_layout()

        if self.items:
            self.build_layout()
