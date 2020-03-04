import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
import mocks
kivy.require("1.11.1")


class FirstScreen(Screen):
    def update_db(self):
        print('ici il faudra appeler ./python\ scripts/dbcreate.py')


class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CategoriesButton(Button):

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = StringProperty(name)


class FoodsScreen(Screen):
    pass


class ItemsScreen(Screen):
    pass


class FavouritesScreen(Screen):
    pass


class PurBeurreApp(App):
    def build(self):
        Builder.load_file('PurBeurre.kv')
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='accueil'))
        screen_manager.add_widget(CategoriesScreen(name='categories'))
        screen_manager.add_widget(FoodsScreen(name='foods'))
        screen_manager.add_widget(ItemsScreen(name='items'))
        screen_manager.add_widget(FavouritesScreen(name='favourites'))
        return screen_manager


if __name__ == "__main__":
    PurBeurreApp().run()
