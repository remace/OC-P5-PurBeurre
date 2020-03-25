import threading
import time

import kivy
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from actions_db import dbcreate, dbread
kivy.require("1.11.1")


class FirstScreen(Screen):
    db_state_text = StringProperty()

    stop = threading.Event()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_state_text = ""
        self.update_status("Update DB")

    @mainthread
    def update_status(self, message):
        self.db_state_text = message

    @mainthread
    def update_button(self, enabled):
        self.children[0].children[0].disabled = not enabled

    def async_update_db(self):
        threading.Thread(target=self.process_update).start()

    def notify(self, message):
        Clock.schedule_once(lambda *args, **kwargs: self.update_status(message), 0)

    def process_update(self):
        self.update_button(False)
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        self.notify("DB Update...")
        # Clock.schedule_once(lambda *args, **kwargs: self.update_status("DB Update..."), 0)

        #TODO soucis de synchronisation de BDD
        # apparemment mysql sort cette excuse quand il sait pas.
        # print("coucou")
        # Do some thread blocking operations.
        dbcreate.empty_db()
        # todo celle-la elle marche mais trop longue
        dbcreate.get_categories(self.notify)
        # time.sleep(5)

        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        # self.update_status("DB Updated") //MARCHE PAS
        self.notify("DB Updated")
        self.update_button(True)

        #TODO pas l'impression que la boucle infinie ait vraiment un interet:
        # le processus semble se terminer de lui-meme

        # # # Start a new thread with an infinite loop and stop the current one.
        # threading.Thread(target=self.infinite_loop).start()

    # def infinite_loop(self):
    #     iteration = 0
    #     while True:
    #         if self.stop.is_set():
    #             # Stop running this thread so the main Python process can exit.
    #             return
    #         iteration += 1
    #         print('Infinite loop, iteration {}.'.format(iteration))
    #         time.sleep(1)


class ItemButton(Button):
    def __init__(self, iid, name, **kwargs):
        super().__init__(**kwargs)
        self.iid = iid
        self.text = self.name = name


class FoodsButton(ItemButton):
    """
    Class representing a Product Button
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class CategoryButton(ItemButton):
    """
    Class representing a Category Button
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def click(self, instance):
        # TODO la methode s'execute 2 fois
        category_id = instance.iid
        print(category_id)
        # next_screen = self.parent.parent.parent.parent.manager.getScreen('foods')
        # foods = dbread.get_foods(category_id)
        # next_screen.items = foods
        # next_screen.init()


class ItemList(ScrollView):

    button_class = ItemButton

    def __init__(self, items, **kwargs):
        super().__init__(size_hint=(1, None), size=(Window.width, Window.height), **kwargs)
        self.items = items
        self.init()

    def init(self):
        list_layout = self.build_layout()
        self.add_widget(list_layout)

    def build_layout(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for item in self.items:
            button = self.button_class(
                iid=item['id'], name=item['name'], size_hint_y=None, height=50
            )
            layout.add_widget(button)
        return layout


class CategoryList(ItemList):
    """
    Class representing A list of category buttons
    """
    button_class = CategoryButton


class FoodsList(ItemList):
    """
    Class representing A list of product buttons
    """
    button_class = FoodsButton


class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = CategoriesScreenStackLayout()
        self.add_widget(layout)


class CategoriesScreenStackLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        categories = dbread.get_categories()
        self.add_widget(CategoryList(categories))


class FoodsScreen(Screen):
    pass


class ItemsScreen(Screen):
    pass


class FavouritesScreen(Screen):
    pass


class PurBeurreApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.first_screen.stop.set()

    def build(self):
        Builder.load_file('PurBeurre.kv')
        screen_manager = ScreenManager()

        self.first_screen = FirstScreen(name='accueil')

        screen_manager.add_widget(self.first_screen)
        screen_manager.add_widget(CategoriesScreen(name='categories'))
        screen_manager.add_widget(FoodsScreen(name='foods'))
        screen_manager.add_widget(ItemsScreen(name='items'))
        screen_manager.add_widget(FavouritesScreen(name='favourites'))
        return screen_manager


if __name__ == "__main__":
    PurBeurreApp().run()
