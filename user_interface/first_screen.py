import threading
from actions_db import dbcreate

from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from user_interface import itemLists


class FirstScreen(Screen):
    db_state_text = StringProperty()
    db_update_btn = ObjectProperty()
    stop = threading.Event()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_state_text = ""
        self.update_status("Bonjour!")

    @mainthread
    def update_status(self, message):
        self.db_state_text = message

    @mainthread
    def update_button(self, enabled):
        self.db_update_btn.disabled = not enabled

    def async_update_db(self):
        threading.Thread(target=self.process_update).start()

    def notify(self, message):
        Clock.schedule_once(lambda *args, **kwargs: self.update_status(message), 0)

    def process_update(self):
        self.update_button(False)
        self.notify("DB Update...")
        dbcreate.process_update(notifier=self.notify)
        self.notify("DB Updated")
        self.update_button(True)

    def press_categories(self):
        manager = self.parent
        next_screen = manager.get_screen('categories')
        next_screen.clear_widgets()
        view = itemLists.CategoryList()
        next_screen.add_widget(view)
        manager.current = 'categories'

    def press_favourites(self):
        manager = self.manager
        next_screen = manager.get_screen('favourites')
        next_screen.clear_widgets()
        view = itemLists.FavouritesList()
        next_screen.add_widget(view)
        manager.current = 'favourites'
