from swm.widgets import Menu


class CategoryMenu(Menu):
    def _convert_item_to_string(self, item):
        length = len(max(self.contents, key=len))
        return (" " + str(item)).ljust(length + 2)

    def _convert_selected_item_to_string(self, item):
        return self._convert_item_to_string(item)

    def _render_item(self, offset, item, render_screen):
        if item == self.selected_item:
            render_screen.draw(offset, self._convert_selected_item_to_string(item), reverse=True, colour="yellow")
        else:
            render_screen.draw(offset, self._convert_item_to_string(item))
        return render_screen
