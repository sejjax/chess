import curses
from abc import abstractmethod, ABC
from typing import Literal, Callable, Type

import npyscreen

from ..constants import LETTERS_FIGURE_MAP
from ..events import MoveFigureEvent
from ..events_queue import moveFigureEventsQueue
from ..utils import figure_symbol_map
from ...controllers.game_session_controller import GameSessionController
from ...events import ViewEventBus, OPEN_FIGURE_CHOOSE_POPUP
from ...lib.styled_string import addstr, bold, styled
from ...lib.vec import vec
from ...models.chess.board import BOARD_SIDE_SIZE
from ...models.chess.board import Board as _Board
from ...models.chess.constants import MIN_BORDER
from ...models.chess.figures import FigureColor, Figure
from ...utils.utils import belongs_to_range

Axis = Literal['x', 'y']
Step = Literal[-1, 0, 1]


class BoardGrid(ABC):
    def __init__(self, cell_size: vec):
        self.cell_size = cell_size


class BoardLayer(BoardGrid, ABC):
    def __init__(self, cell_size):
        super(BoardLayer, self).__init__(cell_size)
        self.hidden = False

    def show(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    @abstractmethod
    def display_cell(self, x, y, addstr: Callable):
        pass

    def display(self, _addstr: Callable):
        for y in range(BOARD_SIDE_SIZE):
            for x in range(BOARD_SIDE_SIZE):
                def addstr(text, relx=0, rely=0):
                    _addstr(text, relx + x * self.cell_size.x, rely + y * self.cell_size.y)

                self.display_cell(x, y, addstr)


class Board(BoardGrid, ABC):
    def __init__(self, cell_size):
        super(Board, self).__init__(cell_size)
        self.layers: list[BoardLayer] = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def add_layers(self, layers: list):
        self.layers += layers


class BoardCellIndexes:
    def __init__(self):
        pass

    def horizontal(self):
        pass

    def vertical(self):
        pass


FILLED_CELL_CHAR = '='
EMPTY_CELL_CHAR = ' '


class ClassicalBoardViewLayer(BoardLayer):
    def __init__(self, cell_size):
        super(BoardLayer, self).__init__(cell_size)

    def display_cell(self, x, y, addstr):
        filled = (x + y) % 2 != 0
        color = FILLED_CELL_CHAR if filled else EMPTY_CELL_CHAR
        row = color * self.cell_size.x
        cell_view = "\n".join([row for _ in range(self.cell_size.y)])
        addstr(cell_view)


class ClassicalBoard(Board):
    def __init__(self, cell_size):
        super(ClassicalBoard, self).__init__(cell_size)
        self.add_layer(ClassicalBoardViewLayer(cell_size))


class ChessBoard(ClassicalBoard):
    pass


class Cursor:
    def __init__(self, pos: vec):
        self.pos = pos


class CursorView:
    def __init__(self, cursor: Cursor, view):
        self.cursor = cursor
        self.view = view


DEFAULT_CURSOR_VIEW = '*'


class MagneticMovementControl:
    pass


class BoardCursorLayer(BoardLayer):
    def __init__(self, cell_size, cursor: Cursor, board: _Board):
        self.board = board
        super(BoardLayer, self).__init__(cell_size)

        self.cursor_view = CursorView(cursor, DEFAULT_CURSOR_VIEW)

    def display_cell(self, x, y, addstr):
        pos = self.cursor_view.cursor.pos
        figure = self.board.get_cell((x, y)).content
        middle = self.cell_size // 2

        if vec(x, y) == self.cursor_view.cursor.pos:
            view = DEFAULT_CURSOR_VIEW
            if figure:
                view = render_figure(figure)

            view = bold(view)
            addstr(view, middle.x, middle.y)


def map_figure_to_color(figure):
    RED = curses.color_pair(7)
    BLUE = curses.color_pair(4)
    return RED if figure.color == FigureColor.BLACK else BLUE


def render_figure(figure):
    color = map_figure_to_color(figure)
    figure_view = styled(LETTERS_FIGURE_MAP[type(figure)], color=color)
    return figure_view


class ChessFiguresLayer(BoardLayer):
    def __init__(self, cell_size, board: _Board):
        super(ChessFiguresLayer, self).__init__(cell_size)
        self.board = board
        self.theme_manager = npyscreen.ThemeManager()

    def display_cell(self, x, y, addstr):
        figure = self.board.get_cell((x, y)).content
        if figure is not None:
            figure_view = render_figure(figure)
            middle = self.cell_size // 2
            addstr(figure_view, middle.x, middle.y)


class ChessAvailableCellsHighlightLayer(BoardLayer):
    def __init__(self, cell_size, board, board_view):
        self.board = board
        self.board_view = board_view
        if self.board_view.highlight_cells is None:
            self.board_view.highlight_cells = []
        super(ChessAvailableCellsHighlightLayer, self).__init__(cell_size)

    def display_cell(self, x, y, addstr):
        s = list(filter(lambda i: i == vec(x, y), self.board_view.highlight_cells))

        check = len(s) > 0
        if check:
            s = s[0]
            middle = self.cell_size // 2
            figure = self.board.get_cell(self.board_view.selected_cell_pos).content

            cell_figure = self.board.get_cell(s).content

            if cell_figure is not None:
                color = map_figure_to_color(cell_figure)
                symbol = figure_symbol_map(cell_figure)
            else:
                color = map_figure_to_color(figure)
                symbol = '*'
            is_bold = bool(figure)
            view = styled(symbol, color=color, bold=is_bold)
            addstr(view, middle.x, middle.y)


class CursorMovementControl:
    def __init__(self, cursor: Cursor, limits_to: vec):
        self._current_cell_pos_index = 0
        self.is_movement_lock = False
        self.cells_map: list[vec] = []
        self.cursor = cursor
        self.limits = limits_to - 1

    def lock_movement(self):
        self.is_movement_lock = True

    def unlock_movement(self):
        self.is_movement_lock = False

    def set_cells_map(self, cells_map):
        self.cells_map = cells_map

    def get_current_cell_pos(self):
        return self.cells_map[self._current_cell_pos_index]

    def next_pos(self):
        self._current_cell_pos_index = min(len(self.cells_map) - 1, self._current_cell_pos_index + 1)

    def prev_pos(self):
        self._current_cell_pos_index = max(0, self._current_cell_pos_index - 1)

    def set_current_pos_with_border_limit(self, new_val, axis: Axis):
        if belongs_to_range(MIN_BORDER, getattr(self.limits, axis), new_val, True, True):
            setattr(self.cursor.pos, axis, new_val)

    def move(self, step: Step, axis: Axis):
        val = getattr(self.cursor.pos, axis)
        new_val = val + step
        self.set_current_pos_with_border_limit(new_val, axis=axis)

    def go_top(self):
        self.move(-1, axis='y')

    def go_down(self):
        self.move(1, axis='y')

    def go_left(self):
        self.move(-1, axis='x')

    def go_right(self):
        self.move(1, axis='x')

    def controllers(self):
        return self.go_top, self.go_right, self.go_down, self.go_left


class MainBoard(ClassicalBoard):
    def __init__(self, widget, cell_size, game_controller: GameSessionController):
        self.selected_cell_pos = None
        self.widget = widget
        self.game_controller = game_controller

        self.board = self.game_controller.get_board()
        self.highlight_cells = []
        if self.selected_cell_pos is not None:
            self.highlight_cells = self.game_controller.get_figure_available_cells(self.selected_cell_pos)

        super(MainBoard, self).__init__(cell_size)

        self.cursor = Cursor(vec(0, 0))
        limits_to = vec(BOARD_SIDE_SIZE, BOARD_SIDE_SIZE)
        self.cursor_movement_control = CursorMovementControl(self.cursor, limits_to)
        cursor_layer = BoardCursorLayer(cell_size, self.cursor, self.board)

        if self.selected_cell_pos:
            cell = self.board.get_cell(self.selected_cell_pos)
            figure = cell.content
        chess_figures_layer = ChessFiguresLayer(cell_size, self.board)
        self.available_cells_highlight_layers = ChessAvailableCellsHighlightLayer(
            cell_size,
            self.board,
            self
        )

        self.add_layers([
            chess_figures_layer,
            self.available_cells_highlight_layers,
            cursor_layer
        ])

        self.prev_from_pos = None
        self.prev_to_pos = None

    def reset(self):
        self.game_controller.reset_game()
        self.cursor.pos = vec(0, 0)
        self.highlight_cells = []
        self.selected_cell_pos = None

    def get_movement_handlers(self):
        return self.cursor_movement_control.controllers()

    def get_select_cell_handler(self):
        return self.select_cell_handler

    def select_cell(self):
        cursor_cell_content = self.board.get_cell(tuple(self.cursor.pos)).content
        current_player_color = self.game_controller.get_current_player_color()
        step_by_step_play = self.game_controller.get_game_mode().step_by_step_play
        check = cursor_cell_content is not None and (
                cursor_cell_content.color == current_player_color or not step_by_step_play)
        if check:
            self.selected_cell_pos = self.cursor.pos.copy()
            available_cells = self.game_controller.get_figure_available_cells(self.selected_cell_pos)
            self.highlight_cells = available_cells

    def get_available_cells_pos(self):
        pass

    def deselect_cell(self):
        self.selected_cell_pos = None
        self.highlight_cells = []

    def select_cell_handler(self):
        if self.cursor.pos in self.highlight_cells:
            self.do_step_action()
            self.deselect_cell()
        elif self.selected_cell_pos != self.cursor.pos or self.selected_cell_pos is not None:
            self.select_cell()
        else:
            self.deselect_cell()

    def from_to_pos(self):
        return self.selected_cell_pos, self.cursor.pos

    def do_step_action(self):

        from_pos, to_pos = self.from_to_pos()

        will_pawn_trans = self.game_controller.will_pawn_transform(from_pos, to_pos)
        if will_pawn_trans:
            ViewEventBus.send(OPEN_FIGURE_CHOOSE_POPUP)
            event = MoveFigureEvent(from_pos, to_pos)
            moveFigureEventsQueue.put_nowait(event)
            return
        self.do_step(from_pos, to_pos)

    def complete_pawn_step(self, figure: Type[Figure]):
        event = moveFigureEventsQueue.get_nowait()
        self.do_step(event.from_pos, event.to_pos, figure)

    def do_step(self, from_pos, to_pos, transform_pawn_into=None):
        self.game_controller.do_current_player_step(from_pos, to_pos, transform_pawn_into)

    def choose_figure(self, choosed_figure):
        pass


class BoardRenderer:
    def __init__(self, board_pos, board):
        self.board = board
        self.board_pos = board_pos

    def display(self, screen):
        if len(self.board.layers) == 0:
            return
        layer_renderer = LayerRenderer(screen, self.board.layers[0], self.board_pos)
        layer_renderer.display()
        for layer in self.board.layers[1:]:
            layer_renderer.layer = layer
            layer_renderer.display()


class LayerRenderer:
    def __init__(self, screen, layer: BoardLayer, board_pos):
        self.screen = screen
        self.layer = layer
        self.board_pos = board_pos

    def display(self):
        self.layer.display(self.addstr)

    def addstr(self, text, relx=0, rely=0):
        addstr(self.screen, text, relx + self.board_pos.x, rely + self.board_pos.y)
