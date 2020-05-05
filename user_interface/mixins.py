from actions_db import dbread
from user_interface import itemLists #, itemView


class CallbackMixin:

    @property
    def manager(self):
        parent = self
        manager = None
        while manager is None:
            parent = getattr(parent, 'parent')
            manager = getattr(parent, 'manager', None)
        return manager

    def on_click_favorite(self):
        self.item.favourite = not self.item.favourite
        if self.item.favourite:
            dbread.set_favourite(self.item.food_id)
        else:
            dbread.reset_favourite(self.item.food_id)
        self.favourite_btn.text = "supprimer des favoris" if self.item.favourite else "ajouter aux favoris"

    def change_fav_image(self):
        self.image.source = "./ressources/img/unfav_icon.png" if self.item.favourite else "./ressources/img/fav_icon.png"
        self.favourite_btn.text = ""
        self.favourite_btn.background_color = (1, 0, 0, 1) if self.item.favourite else (0, 1, 0, 1)

    # def on_click_details(self):
    #     manager = self.manager
    #     next_screen = manager.get_screen('item')
    #     next_screen.clear_widgets()
    #     view = itemView.ItemView(self.item.food_id)
    #     next_screen.add_widget(view)
    #     manager.current = 'item'

    def on_click_substitute(self):
        manager = self.manager
        next_screen = manager.get_screen('substitutes')
        next_screen.clear_widgets()
        view = itemLists.SubstitutesList()
        view.update_layout(self.item.category_id, self.item.nutriscore)
        next_screen.add_widget(view)
        manager.current = 'substitutes'


