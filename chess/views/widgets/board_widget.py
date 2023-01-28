import npyscreen

from chess.lib.styled_string import bold, reverse, styled, addstr
from chess.lib.vec import vec
from chess.models.chess.board import Board
from chess.models.chess.constants import *
from chess.views.constants import BOARD_SIDE_X, BOARD_SIDE_Y, CELL_Y, CELL_X, ALPHA, CELL_SIZE, NUMBERS, EMPTY, \
    CELL_MIDDLE_Y, FILLED
from chess.views.utils import get_pad, figure_symbol_map


class BoardWidget(npyscreen.widget.Widget):

    def __init__(self, screen, board: Board = None, relx=0, rely=0, name=None, value=None, width=False, height=False,
                 max_height=False, max_width=False, editable=True, hidden=False, color='DEFAULT', use_max_space=False,
                 check_value_change=True, check_cursor_move=True, value_changed_callback=None, **keywords):
        super().__init__(screen, relx, rely, name, value, width, height, max_height, max_width, editable, hidden, color,
                         use_max_space, check_value_change, check_cursor_move, value_changed_callback, **keywords)
        self.board = board

        self.some = True
        self.curr_pos = vec(0, 0)
        self.selected_cell_pos = None

    def set_up_handlers(self):
        super().set_up_handlers()
        self.add_handlers({
            ord('a'): self.h_left,
            ord('d'): self.h_right,
            ord('w'): self.h_up,
            ord('s'): self.h_down,
            ord('k'): self.h_swap_cell_selection
        })

    def when_cursor_moved(self):
        pass

    def select_cell(self):
        content = self.board.get_cell(self.curr_pos).content
        if content:
            self.selected_cell_pos = self.curr_pos

    def deselect_cell(self):
        self.selected_cell_pos = None

    def h_swap_cell_selection(self, event):
        if self.selected_cell_pos is None:
            return self.select_cell()
        return self.deselect_cell()

    def exit_widget(self):
        self.curr_pos = vec(0, 0)
        self.editing = False

    def h_left(self, event):
        if self.selected_cell_pos:
            return
        if self.curr_pos.x - 1 < LEFT_BORDER:
            return self.exit_widget()
        self.curr_pos.x -= 1

    def h_up(self, event):
        if self.selected_cell_pos:
            return
        if self.selected_cell_pos:
            return
        if self.curr_pos.y - 1 < TOP_BORDER:
            return self.exit_widget()
        self.curr_pos.y -= 1

    def h_right(self, event):
        if self.selected_cell_pos:
            return
        if self.curr_pos.x + 1 > RIGHT_BORDER:
            return self.exit_widget()
        self.curr_pos.x += 1

    def h_down(self, event):
        if self.selected_cell_pos:
            return
        if self.curr_pos.y + 1 > BOTTOM_BORDER:
            return self.exit_widget()
        self.curr_pos.y += 1

    def calculate_area_needed(self):
        return BOARD_SIDE_Y + 1, BOARD_SIDE_X + 1

    def update(self, clear=True):
        if clear:
            self.clear()
        if self.editing:
            get_pad(self).addstr(self.rely, self.relx, '$')

        self.draw_letters(self.rely, self.relx + 2)
        get_pad(self).addstr(self.rely, self.relx + 1, str(self.curr_pos))
        self.draw_symbols_side(self.rely, self.relx)
        BOARD_SHIFT = 1
        for i in range(BOARD_SIDE_SIZE):
            for a in range(BOARD_SIDE_SIZE):
                is_filled = (i + a) % 2 != 0
                cell_y_pos = self.rely + a * CELL_Y + BOARD_SHIFT
                cell_x_pos = self.relx + i * CELL_X + BOARD_SHIFT + 1
                symbol_figure = None
                figure = self.board.get_cell((i, a)).content
                if figure is not None:
                    symbol_figure = figure_symbol_map(figure)
                if self.editing and self.curr_pos == vec(i, a):
                    if symbol_figure is not None:
                        if self.selected_cell_pos == self.curr_pos:
                            symbol_figure = bold(symbol_figure)
                        else:
                            symbol_figure = bold(reverse(symbol_figure))
                    else:
                        symbol_figure = bold('*')
                self.draw_cell(is_filled, cell_x_pos, cell_y_pos, content=symbol_figure)

    def draw_letters(self, rely=0, relx=0, fill=' '):
        half = (CELL_SIZE // 2) * fill
        row = ''
        for i in range(len(ALPHA)):
            cell = half + ALPHA[i] + half
            row += cell

        get_pad(self).addstr(rely, relx, row)

    def draw_symbols_side(self, rely=0, relx=0, fill='', direction=''):
        for i in range(BOARD_SIDE_SIZE):
            middle = 2 + i * CELL_Y
            get_pad(self).addstr(middle + rely, relx, NUMBERS[i])

    def draw_cell(self, filled, relx=0, rely=0, content=None):
        color = FILLED if filled else EMPTY
        for i in range(CELL_Y):
            figure = content if i == CELL_MIDDLE_Y and content else color
            cell_y_pos = rely + i
            cell_x_pos = relx
            half = styled(color * (CELL_X // 2))
            row = half + figure + half
            addstr(get_pad(self), row, cell_x_pos, cell_y_pos)

    def make_attributes_list(self, unicode_string, attribute):
        return super().make_attributes_list(unicode_string, attribute)