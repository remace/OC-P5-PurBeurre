import kivy
from kivy.config import Config

from kivy.base import runTouchApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
kivy.require("1.11.1")
from user_interface import first_screen, itemLists, itemView


class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(itemLists.CategoryList())


class FoodsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(itemLists.FoodsList())


class ItemsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(itemView.ItemView())

class FavouritesScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PurBeurreApp(App):
    title = "Pur Beurre"
    def on_stop(self):
        self.first_screen.stop.set()

    def build(self):
        # delete multitouch behaviour simulator (red dots on labels for example)
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

        Builder.load_file('PurBeurre.kv')
        screen_manager = ScreenManager()
        self.first_screen = first_screen.FirstScreen(name='accueil')
        screen_manager.add_widget(self.first_screen)
        screen_manager.add_widget(CategoriesScreen(name='categories'))
        screen_manager.add_widget(FoodsScreen(name='foods'))
        screen_manager.add_widget(ItemsScreen(name='item'))
        screen_manager.add_widget(FavouritesScreen(name='favourites'))
        return screen_manager


if __name__ == "__main__":
    PurBeurreApp().run()
