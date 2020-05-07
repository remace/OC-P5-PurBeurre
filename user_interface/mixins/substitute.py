from itemLists import SubstitutesList


class SubstituteMixin:

    def on_click_substitute(self):
        manager = self.manager
        next_screen = manager.get_screen('substitutes')
        next_screen.clear_widgets()
        view = SubstitutesList()
        view.update_layout(self.item.category_id, self.item.nutriscore)
        next_screen.add_widget(view)
        manager.current = 'substitutes'
