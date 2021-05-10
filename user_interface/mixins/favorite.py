from actions_db import dbread


class FavoriteMixin:

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
        self.image.center_x = self.favourite_btn.center_x
        self.image.center_y = self.favourite_btn.center_y

    def reload_favourite_screen(self):
        if self.manager.current == 'favourites':
            self.parent.remove_widget(self)