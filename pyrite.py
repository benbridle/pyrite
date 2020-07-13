from modules import CategoryList, CategoryMenu, PriceTextBuffer, Timer, PurchaseList, Table, datetime_tools
import os
import sys
import time
from datetime import datetime
import string
from swm import silica, Key

silica.setup()

project_path = os.path.dirname(os.path.realpath(__file__))
categories_path = os.path.join(project_path, "data/categories.csv")
spending_data_path = os.path.join(project_path, "data/spending_data.csv")


class Program:
    def __init__(self):
        self.initialise_windows()
        self.initialise_overview_table()

        self.category_list = CategoryList.from_csv(categories_path)
        self.category_menu = CategoryMenu(self.category_list.categories)
        self.textbuffer = PriceTextBuffer()

        self.example_text_timer = Timer(3)
        self.standby_timer = Timer(5)
        self.reset_time_pointer_to_now()

        self.purchase_list = PurchaseList.from_csv(spending_data_path)
        self.populate_overview_table()
        self.update_table_highlight()

    def initialise_windows(self):
        silica.add_window((0, 0, 22, -4), "categories").set_title("Categories")
        silica.add_window((22, 0, -1, -4), "overview").set_title("Overview")
        silica.add_window((0, -3, 22, -1), "cost").set_title("Enter cost")
        silica.add_window((22, -3, -1, -1), "time").set_title("\u2190 Selected week \u2192")
        silica.add_centered_window((38, 3), "examples").set_title("Examples")

    def initialise_overview_table(self):
        self.overview_table = Table(["Category", "Total"])
        cat_column = self.overview_table.get_column("Category")
        cat_column.proportional_width = 2
        total_column = self.overview_table.get_column("Total")
        total_column.minimum_width = 10
        total_column.proportional_width = 1

    def populate_overview_table(self):
        self.overview_table.clear_rows()
        category_totals = self.get_purchases_in_selected_week().group_purchases_by_category()
        category_totals_names = [purchase.category_name for purchase in category_totals]

        for category in self.category_list:
            if category.name in category_totals_names:
                for purchase in category_totals:
                    if purchase.category_name == category.name:
                        cost = purchase.cost
                row = (category.name, str(cost))
                self.overview_table.add_row(row)

    def update_table_highlight(self):
        category_totals = self.get_purchases_in_selected_week().group_purchases_by_category()
        category_totals_names = [purchase.category_name for purchase in category_totals]

        category_totals_names_sorted = []
        for category in self.category_list:
            if category.name in category_totals_names:
                category_totals_names_sorted.append(category.name)

        selected_cat = self.category_menu.selected_item.name
        try:
            row_number = category_totals_names_sorted.index(selected_cat)
        except ValueError:
            self.overview_table.highlighted_cells = []
            return
        self.overview_table.highlighted_cells = [(1, row_number)]

    def get_purchases_in_selected_week(self):
        week_start = datetime_tools.get_start_of_week(self.time_pointer)
        week_end = datetime_tools.get_end_of_week(self.time_pointer)
        purchase_list = self.purchase_list.get_purchases_within_time_period(week_start, week_end)
        return purchase_list

    def reset_time_pointer_to_now(self):
        self.time_pointer = datetime_tools.get_start_of_week(datetime.now())

    def draw_category_menu(self):
        cat_window = silica.get_window("categories")
        width = cat_window.screen.width
        height = cat_window.screen.height
        cat_screen = self.category_menu.render(width, height)
        cat_window.draw((0, 0), cat_screen)

    def draw_text_buffer(self):
        cat_screen = silica.get_window("cost")
        cat_screen.draw((1, 0), "$ " + self.textbuffer.get())

    def draw_selected_week(self):
        time_window = silica.get_window("time")
        date_string_1 = datetime_tools.get_human_readable_string(self.time_pointer)
        date_string_2 = datetime_tools.get_human_readable_string(datetime_tools.get_end_of_week(self.time_pointer))
        date_string = date_string_1 + " - " + date_string_2
        time_window.draw((0, 0), date_string.center(time_window.screen.width))

    def draw_subtotals(self):
        food_spending = 0
        total_spending = 0

        selected_purchases = self.get_purchases_in_selected_week()
        for purchase in selected_purchases.purchases:
            if purchase.category_name.startswith("Food: "):
                food_spending += float(purchase.cost)
            total_spending += float(purchase.cost)
        overview_window = silica.get_window("overview")
        overview_window.draw((-12, -2), f" Food: ${food_spending:.0f}")
        overview_window.draw((-12, -1), f"Total: ${total_spending:.0f}")

    def parse_keypress(self, key):
        if not key.is_empty():
            self.standby_timer.start()

        if key == "q":
            sys.exit()
        if key == Key.UP:
            self.category_menu.previous()
            self.example_text_timer.start()
            self.update_table_highlight()
        if key == Key.DOWN:
            self.category_menu.next()
            self.example_text_timer.start()
            self.update_table_highlight()
        if key == Key.PAGEUP:
            self.category_menu.pointer = 0
            self.example_text_timer.start()
            self.update_table_highlight()
        if key == Key.PAGEDOWN:
            self.category_menu.pointer = -1
            self.example_text_timer.start()
            self.update_table_highlight()
        if key == Key.LEFT:
            self.time_pointer -= datetime_tools.one_week_delta
            self.populate_overview_table()
            self.update_table_highlight()
        if key == Key.RIGHT:
            self.time_pointer += datetime_tools.one_week_delta
            self.populate_overview_table()
            self.update_table_highlight()
        if key == Key.ENTER:
            tb = self.textbuffer.get()
            if tb != "":
                current_category = self.category_menu.selected_item
                self.purchase_list.add_purchase(current_category.name, float(tb))
                self.textbuffer.clear()
                self.reset_time_pointer_to_now()
                self.populate_overview_table()
                self.update_table_highlight()
                self.purchase_list.save()

        if key.is_character():
            self.textbuffer.add(str(key))
        if key == Key.BACKSPACE:
            self.textbuffer.backspace()

    def main(self):
        overview_window = silica.get_window("overview")
        examples_window = silica.get_window("examples")
        hint = self.category_menu.selected_item.hint
        examples_window.draw((0, 0), hint.center(examples_window.screen.width))
        examples_window.visible = not self.example_text_timer.is_expired()

        key = silica.get_keypress()
        self.parse_keypress(key)

        # Draw different border on overview window if on current week
        start_time = datetime_tools.get_start_of_week(self.time_pointer)
        end_time = datetime_tools.get_end_of_week(self.time_pointer)

        if start_time <= datetime_tools.now() <= end_time:
            overview_window.set_theme("double")
        else:
            overview_window.set_theme("normal")

        self.overview_table.render_to_window(overview_window)
        self.draw_category_menu()
        self.draw_selected_week()
        self.draw_text_buffer()
        self.draw_subtotals()

        silica.process()


try:
    program = Program()
    while True:
        program.main()
except BaseException as e:
    silica.cleanup()
    raise e
finally:
    silica.cleanup()
