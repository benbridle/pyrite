from swm.components import Screen, Point, Border


class Table:
    def __init__(self, column_headers):
        self.columns = []
        for header in column_headers:
            self.add_column(header)
        self.clear_rows()
        self.theme = Border.NORMAL
        self.highlighted_cells = []

    def clear_rows(self):
        self.rows = []

    def add_column(self, header, **kwargs):
        if header in self.get_headers():
            raise KeyError("Column named {} already exists".format(header))
        self.columns.append(TableColumn(header, **kwargs))

    def get_headers(self):
        return [column.header for column in self.columns]

    def get_column(self, header):
        for column in self.columns:
            if column.header == header:
                return column
        raise KeyError("No column named {}".format(header))

    def add_row(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            self.rows.append(args[0])
        else:
            self.rows.append([*args])

    def _render_sequence_over_columns(self, sequence, row_index, render_screen):
        proportional_unit_size = self._get_proportional_unit_size(render_screen.width, allow_space_for_grid=True)
        x_offset = 0
        for column_index, column in enumerate(self.columns):
            column_width = column.get_width(proportional_unit_size)
            try:
                item = str(sequence[column_index])
            except IndexError:
                item = ""
            highlight = False
            for cell in self.highlighted_cells:
                if cell[0] == column_index and cell[1] == row_index - 2:
                    highlight = True
            render_screen.draw((x_offset + 1, row_index), item, reverse=highlight)
            if column != self.columns[-1]:
                render_screen.draw((x_offset + column_width, row_index), self.theme[Border.VERTICAL])
            x_offset += column_width + 1

    def _render_row(self, row, row_index, render_screen):
        self._render_sequence_over_columns(row, row_index, render_screen)

    def _render_headers(self, render_screen):
        self._render_sequence_over_columns(self.get_headers(), 0, render_screen)

        proportional_unit_size = self._get_proportional_unit_size(render_screen.width, allow_space_for_grid=True)
        i = 0
        for column in self.columns:
            column_width = column.get_width(proportional_unit_size)
            if column == self.columns[-1]:
                # prevent offscreen intersection from showing in some circumstances
                render_screen.draw((0 + i, 1), self.theme[Border.HORIZONTAL] * column_width * 2)
            else:
                render_screen.draw(
                    (0 + i, 1), self.theme[Border.HORIZONTAL] * column_width + self.theme[Border.INTERSECTION]
                )

            i += column_width + 1

    def render_to_window(self, window, offset=(0, 0)):
        rendered_menu = self.render(window.screen.width, window.screen.height)
        window.draw(offset, rendered_menu)

    def render(self, width, height) -> Screen:
        render_screen = Screen(width, height)
        self._render_headers(render_screen)

        for index, row in enumerate(self.rows):
            self._render_row(row, index + 2, render_screen)
        return render_screen

    def _get_proportional_unit_size(self, screen_width, allow_space_for_grid=False):
        if allow_space_for_grid:
            screen_width -= len(self.columns) - 1
        try:
            total_prop_units = sum([column.proportional_width for column in self.columns])
        except ZeroDivisionError:
            total_prop_units = 1
        # get proportional unit size, ignoring minimum column widths for now
        prop_unit_size_first_pass = screen_width // total_prop_units

        # reserve width for columns that need it. these are columns where the
        # proportional width from the first pass is smaller than their minimum width
        width_to_portion_out = screen_width
        for column in self.columns:
            if column.minimum_width > 0:
                prop_minus_min = column.minimum_width - (column.proportional_width * prop_unit_size_first_pass)
                width_to_portion_out -= max(prop_minus_min, 0)
        prop_unit_size_second_pass = width_to_portion_out // total_prop_units
        return prop_unit_size_second_pass

    def get_rendered_screen(self, width, height):
        screen = Screen(width, height)
        screen_width = screen.width
        column_widths = self.get_column_widths(screen_width)
        column_headers = self.get_column_headers()
        header_line = ""
        under_line = ""
        for width, header in zip(column_widths, column_headers):
            header_line += header.center(width - 1)[: width - 1] + Border.NORMAL[Border.VERTICAL]
            under_line += Border.NORMAL[Border.HORIZONTAL] * (width - 1) + Border.NORMAL[Border.INTERSECTION]
        screen.draw((0, 0), header_line)
        screen.draw((0, 1), under_line)

        for row_index in range(height):
            line = ""
            for column_index, column_width in enumerate(column_widths):
                line += (
                    " "
                    + self.columns[column_index].formatData(self.get_cell(column_index, row_index), column_width)
                    + Border.NORMAL[Border.VERTICAL]
                )
            line = line
            screen.draw(Point(0, row_index + 2), line)
        return screen

    def get_row(self, index):
        try:
            row = self.rows[index]
        except IndexError:
            row = [""] * len(self.columns)
        while len(row) < len(self.columns):
            row.append("")
        return row

    def get_cell(self, x, y):
        row = self.get_row(y)
        try:
            cell = row[x]
        except IndexError:
            cell = ""
        cell = str(cell)
        return cell

    def get_column_widths(self, screen_width):
        column_widths = []
        for column in self.columns:
            column_widths.append(column.getMinimumSize())
        used_width = sum(column_widths)
        remaining_width = screen_width - used_width
        for index, column in enumerate(self.columns):
            relative_width = self.convert_proportional_size_to_fraction(column.getProportionalSize())
            column_widths[index] += int(remaining_width * relative_width)
        if sum(column_widths) < screen_width:
            for index, width in enumerate(column_widths):
                column_widths[index] += 1

        return column_widths

    def get_column_headers(self):
        column_headers = []
        for column in self.columns:
            column_headers.append(column.getHeader())
        return column_headers

    def convert_proportional_size_to_fraction(self, proportion):
        total_proportions = 0
        for column in self.columns:
            total_proportions += column.getProportionalSize()
        return proportion / total_proportions


class TableColumn:
    def __init__(self, header, proportional_width=1, minimum_width=0, justification="right"):
        self.header = header
        self.proportional_width = proportional_width
        self.minimum_width = minimum_width
        self.justification = justification

    def get_width(self, proportional_unit_size):
        return max(self.minimum_width, self.proportional_width * proportional_unit_size)
