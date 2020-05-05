from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from user_interface import itemLists, itemView
from user_interface.mixins import CallbackMixin


class FoodsListItem(CallbackMixin, FloatLayout):
    name = ObjectProperty()
    details_btn = ObjectProperty()
    favourite_btn = ObjectProperty()
    image = ObjectProperty()

    @property
    def manager(self):
        parent = self
        manager = None
        while manager is None:
            parent = getattr(parent, 'parent')
            manager = getattr(parent, 'manager', None)
        return manager

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.name.text = self.item.food_name
        self.image.source = "./ressources/img/unfav_icon.png" if self.item.favourite else "./ressources/img/fav_icon.png"
        self.favourite_btn.background_color = (1, 0, 0, 1) if self.item.favourite else (0, 1, 0, 1)

    def on_click_details(self):
        manager = self.manager
        next_screen = manager.get_screen('item')
        next_screen.clear_widgets()
        view = itemView.ItemView(self.item.food_id)
        next_screen.add_widget(view)
        manager.current = 'item'


class SubstituteListItem(CallbackMixin, FloatLayout):

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.name.text = str(self.item.food_name)
        self.image.source = "./ressources/img/unfav_icon.png" if self.item.favourite else "./ressources/img/fav_icon.png"
        self.favourite_btn.background_color = (1, 0, 0, 1) if self.item.favourite else (0, 1, 0, 1)

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


class CategoryListItem(CallbackMixin, FloatLayout):

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




