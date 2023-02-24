import asyncio
from enum import Enum
from typing import Literal

import npyscreen
from npyscreen import TitleText, TitleFixedText

from chess.models.chess.board import BOARD_SIDE_SIZE
from chess.views.constants import BOARD_SIDE_X, BOARD_SIDE_Y
from ..lib.board import MainBoard, BoardRenderer, Axis, CursorMovementControl, Cursor
from ..utils import get_pad, figure_symbol_map
from ...controllers.chess_controller import ChessController
from ...events import ViewEventBus, FIGURE_WAS_CHOSE, OPEN_FIGURE_CHOOSE_POPUP
from ...lib.vec import vec
from ...lib.styled_string import addstr, bold, underline
from ...models.chess.figure import FigureColor, Quin, Bishop, Knight, Rook
from ...utils import str_to_list

CELL_SIZE = vec(5, 3)


def calc_shift(num):
    return 1 if num % 2 != 0 else 0


def get_size(widget):
    y, x = widget.calculate_area_needed()
    return x, y


Direction = Literal["vert", "horiz", "vert-horiz"]


def center_widget(widget, outer_widget, direction: Direction = "vert-horiz"):
    outer_size_x, outer_size_y = get_size(outer_widget)
    size_x, size_y = get_size(widget)

    horiz = get_center(outer_size_x, size_x)
    vert = get_center(outer_size_y, size_y)

    if direction == 'vert-horiz':
        widget.relx = horiz
        widget.rely = vert
    elif direction == 'vert':
        widget.rely = vert
    elif direction == 'horiz':
        widget.relx = horiz


def update_wrap(update_fn, callback):
    def wrapper(*args, **kwargs):
        callback(*args, **kwargs)
        update_fn()

    return wrapper


def setup_movement_control_handlers(form, handlers: dict):
    new_handlers = {}

    # Handler Format: Key => handler
    # w -> up_fn
    # d -> down_fn
    # ...

    def _update_wrap(update_fn, callback):
        def wrapper(_, *args, **kwargs):
            callback(*args, **kwargs)
            update_fn()

        return wrapper

    for key, value in handlers.items():
        new_handlers[key] = _update_wrap(form.update, value)

    form.add_handlers(new_handlers)


class HideShow:
    size_store: vec
    hidden: bool
    width: int
    height: int

    def __init__(self):
        self.size_store = vec(0, 0)

    def hide(self):
        self.hidden = True
        self.size_store.x = self.width
        self.size_store.y = self.height
        self.width = self.height = 0

    def show(self):
        self.hidden = False
        self.width = self.size_store.x
        self.height = self.size_store.y


def m_setup_movement_control_select_handlers(form, handlers_list):
    # handlers order top, bottom, left, right, select_cell_handler
    setup_movement_control_handlers(
        form,
        {
            ord('w'): handlers_list[0],
            ord('d'): handlers_list[1],
            ord('s'): handlers_list[2],
            ord('a'): handlers_list[3],
            ord('k'): handlers_list[4]
        }
    )


def get_center(size1, size2):
    check = size1 % 2 != size2 % 2
    shift = 2 if check else 0
    return (size1 // 2) - (size2 // 2)


def cell_shift(shift, axis: Axis):
    return getattr(CELL_SIZE, axis) * shift


STRINGS = {
    FigureColor.WHITE: 'Game Over',
    FigureColor.BLACK: 'Black has won',
}


class GameResultsWidget(npyscreen.widget.Widget, HideShow):
    def __init__(self, screen, winner_color: FigureColor, relx=0, rely=0, name=None, value=None, width=False,
                 height=False,
                 max_height=False, max_width=False, editable=True, hidden=False, color='DEFAULT', use_max_space=False,
                 check_value_change=True, check_cursor_move=True, value_changed_callback=None, **keywords):
        self.view = f"\n{STRINGS[winner_color]}\n"
        super().__init__(screen, relx, rely, name, value, width, height, max_height, max_width, editable, hidden, color,
                         use_max_space, check_value_change, check_cursor_move, value_changed_callback, **keywords)
        HideShow.__init__(self)
        self.winner_color = winner_color
        self.screen = screen

        self.curr_view_index = 0

    def update(self, clear=True):
        if clear:
            self.clear()

        addstr(get_pad(self), self.view, relx=self.relx, rely=self.rely)

    def calculate_area_needed(self):
        view_l = str_to_list(self.view)
        return len(view_l), max(*map(len, view_l))

    def make_attributes_list(self, unicode_string, attribute):
        return super().make_attributes_list(unicode_string, attribute)


class FigureChooser(npyscreen.widget.Widget, HideShow):
    def __init__(self, screen, relx=0, rely=0, name=None, value=None, width=False,
                 height=False,
                 max_height=False, max_width=False, editable=True, hidden=False, color='DEFAULT', use_max_space=False,
                 check_value_change=True, check_cursor_move=True, value_changed_callback=None, **keywords):

        color = FigureColor.WHITE

        figures = [Quin, Knight, Bishop, Rook]
        self.figures = figures = list(map(lambda i: i(color), figures))
        FIGURES_COUNT = len(figures)

        LIMITS_TO = vec(FIGURES_COUNT, 1)
        self.curr_view_index = 0
        self.cursor = Cursor(vec(0, 0))
        self.cursor_movement_control = CursorMovementControl(self.cursor, LIMITS_TO)

        super().__init__(screen, relx, rely, name, value, width, height, max_height, max_width, editable, hidden, color,
                         use_max_space, check_value_change, check_cursor_move, value_changed_callback, **keywords)
        HideShow.__init__(self)
        self.screen = screen
        self.chess_controller = ChessController()

    def update(self, clear=True):
        if clear:
            self.clear()
        if not self.hidden:
            screen = get_pad(self)
            for i in range(4):
                view = figure_symbol_map(self.figures[i])
                if self.cursor.pos.x == i:
                    view = bold(view)
                addstr(
                    screen, view,
                    relx=self.relx + cell_shift(i, 'x') + get_center(CELL_SIZE.x, 1),
                    rely=self.rely + get_center(CELL_SIZE.y, 1)
                )

    def calculate_area_needed(self):
        if not self.hidden:
            return CELL_SIZE.y, CELL_SIZE.x * 4
        return 0, 0

    def make_attributes_list(self, unicode_string, attribute):
        return super().make_attributes_list(unicode_string, attribute)

    def set_up_handlers(self):
        super().set_up_handlers()
        handlers = [
            *self.cursor_movement_control.controllers(),
            self.action_handler
        ]
        m_setup_movement_control_select_handlers(self, handlers)

    def _action_callback(self):
        ViewEventBus.send(FIGURE_WAS_CHOSE)

    def action_handler(self):
        self._action_callback()

    def get_current_figure(self):
        return type(self.figures[self.cursor.pos.x])


class BoardWidget(npyscreen.widget.Widget):
    board: MainBoard
    board_renderer: BoardRenderer
    chess_controller: ChessController
    size_store: vec
    choose_figure_popup: FigureChooser

    def __init__(self, screen, relx=0, rely=0, name=None, value=None, width=False, height=False,
                 max_height=False, max_width=False, editable=True, hidden=False, color='DEFAULT', use_max_space=False,
                 check_value_change=True, check_cursor_move=True, value_changed_callback=None, **keywords):
        self.size_store = vec(0, 0)
        self.screen = screen
        super().__init__(screen, relx, rely, name, value, width, height, max_height, max_width, editable, hidden, color,
                         use_max_space, check_value_change, check_cursor_move, value_changed_callback, **keywords)
        self.pos = vec(relx, rely)

        self.reset()
        ViewEventBus.connect(self.on_figure_choose)
        ViewEventBus.connect(self.on_open_figure_choose_popup)

    def on_figure_choose(self, event):
        if event == FIGURE_WAS_CHOSE:
            figure = self.choose_figure_popup.get_current_figure()
            self.board.complete_pawn_step(figure)
            self.hide_choose_figure_popup()

    def reset_choose_figure_popup(self):
        if hasattr(self, 'game_result_popup'):
            del self.game_result_popup

        self.choose_figure_popup = self.screen.add_widget(
            FigureChooser,
            hidden=True,
            name="Cool Board Widget ",
        )
        self.choose_figure_popup.relx = self.relx + cell_shift(2, 'x')
        self.choose_figure_popup.rely = self.rely + cell_shift(3, 'y')

    def show_choose_figure_popup(self):
        self.set_editable(False)
        self.choose_figure_popup.show()
        self.update()


    def hide_choose_figure_popup(self):
        self.choose_figure_popup.hide()
        self.update()
        self.edit()

    def on_open_figure_choose_popup(self, event):
        if event == OPEN_FIGURE_CHOOSE_POPUP:
            self.show_choose_figure_popup()

    def choose_figure_from_popup(self):
        self.show_choose_figure_popup()

    def _set_up_handlers(self):
        handlers = self.board.get_movement_handlers()
        select_cell_handler = self.board.get_select_cell_handler()

        m_setup_movement_control_select_handlers(self, [*handlers, select_cell_handler])

    def reset(self):
        self.chess_controller = ChessController()
        self.board = MainBoard(self, CELL_SIZE)
        self.board_renderer = BoardRenderer(self.pos, self.board)
        self._set_up_handlers()
        self.reset_choose_figure_popup()

    def move_update(self, callback):
        def wrapper(_):
            callback()
            self.update()

        return wrapper

    def calculate_area_needed(self):
        return CELL_SIZE.y * BOARD_SIDE_SIZE, CELL_SIZE.x * BOARD_SIDE_SIZE

    def update(self, clear=True):
        if clear:
            self.clear()
        screen = get_pad(self)

        self.board_renderer.display(screen)
        if not self.choose_figure_popup.hidden:
            self.choose_figure_popup.update()

    def make_attributes_list(self, unicode_string, attribute):
        return super().make_attributes_list(unicode_string, attribute)
