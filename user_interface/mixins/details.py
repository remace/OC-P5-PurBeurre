from itemView import ItemView


class DetailsMixin:

    def on_click_details(self):
        manager = self.manager
        next_screen = manager.get_screen('item')
        next_screen.clear_widgets()
        view = ItemView(self.item.food_id)
        next_screen.add_widget(view)
        manager.current = 'item'
