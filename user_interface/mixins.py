from actions_db import dbread


class CallbackMixin:

    def on_click_favorite(self):
        self.item.favourite = not self.item.favourite
        if self.item.favourite:
            dbread.set_favourite(self.item.food_id)
        else:
            dbread.reset_favourite(self.item.food_id)
        self.favourite_btn.text = "supprimer des favoris" if self.item.favourite else "ajouter aux favoris"
