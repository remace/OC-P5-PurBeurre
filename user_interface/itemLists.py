from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
import actions_db
from user_interface.buttons import FoodsListItem, CategoryListItem


class CategoryList(FloatLayout):

    cat_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foods = actions_db.dbread.get_categories()
        self.build_layout()

    def build_layout(self):
        self.cat_layout.clear_widgets()
        for i in self.foods:
            self.cat_layout.add_widget(CategoryListItem(i))

    @property
    def manager(self):
        parent = self
        manager = None
        while manager is None:
            parent = getattr(parent, 'parent')
            manager = getattr(parent, 'manager', None)
        return manager


class FoodsList(FloatLayout):

    layout = ObjectProperty()

    @property
    def manager(self):
        parent = self
        manager = None
        while manager is None:
            parent = getattr(parent, 'parent')
            manager = getattr(parent, 'manager', None)
        return manager

    def __init__(self, iid=None):
        super().__init__()
        if iid:
            self.items = actions_db.dbread.get_foods(iid)
            self.build_layout()

    def update_layout(self, iid):
        self.items = actions_db.dbread.get_foods(iid)
        self.update_layout()

    def build_layout(self):
        for i in self.items:
            self.layout.add_widget(FoodsListItem(i))


class FavouritesList(Widget):

    pass
