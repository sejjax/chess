import curses

from ...lib.vec import vec
from .figure import Figure, FigureColor, Pawn, Rook, Knight, Bishop, King, Quin
from chess.models.chess.constants import *
from ...views.utils import symbol_figure_map, symbol_figure_color_map
from ...utils import str_to_list


class Cell:
    content: Figure | None

    def __init__(self, content: Figure | None = None) -> None:
        self._content = content

    def clear(self):
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, figure: Figure | None):
        self._content = figure


class Board:
    def __init__(self, matrix: list | None = None) -> None:
        if matrix is not None:
            self.board = matrix
        else:
            # Generate matrix 8x8
            self.board = self.create_init_state()

        self.white_figures = []
        self.black_figures = []

    @staticmethod
    def build():
        board = Board()

        for row, row_list in enumerate(board.board):
            for column, cell in enumerate(row_list):
                figure_color = FigureColor.BLACK if row < 4 else FigureColor.WHITE

                is_empty_cell = 1 < row < 6

                # Implements default figure location
                cls_ = None
                if row == 1 or row == 6:
                    cls_ = Pawn
                elif row in [LEFT_BORDER, RIGHT_BORDER]:
                    if column in [TOP_BORDER, BOTTOM_BORDER]:
                        cls_ = Rook
                    elif column in [1, 6]:
                        cls_ = Knight
                    elif column in [2, 5]:
                        cls_ = Bishop
                    elif column == 3:
                        cls_ = King
                    elif column == 4:
                        cls_ = Quin

                if is_empty_cell:
                    figure = None
                else:
                    figure = cls_(figure_color)

                board.set_cell_content(column, row, figure)

                group = board.white_figures if figure_color == FigureColor.WHITE else board.black_figures
                group.append(figure)

        return board

    @staticmethod
    def build_from_string(string):
        board = Board()
        string = string.strip()
        strings = str_to_list(string)
        def check(checkable):
            if len(checkable) != BOARD_SIDE_SIZE:
                raise Exception('rows cound in the strings must be equal to 8. Got ' + str(len(checkable)))

        # Fill not enough space
        if len(strings) < BOARD_SIDE_SIZE:
            strings += [' ' * BOARD_SIDE_SIZE for _ in range(BOARD_SIDE_SIZE - len(strings))]
        elif len(strings) > BOARD_SIDE_SIZE:
            strings = strings[:BOARD_SIDE_SIZE]

        for string_row, board_row in zip(strings, board.board):
            if len(string_row) < 8:
                string_row += ' ' * (BOARD_SIDE_SIZE - len(string_row))
            for str_cell, board_cell in zip(string_row, board_row):
                try:
                    figure = symbol_figure_color_map(str_cell)
                    board_cell.content = figure
                except KeyError:
                    if str_cell != ' ':
                        raise Exception('Unknown char')

        return board



    @staticmethod
    def create_init_state():
        return [[Cell() for _ in range(BOARD_SIDE_SIZE)] for _ in range(BOARD_SIDE_SIZE)]

    def get_figures(self):
        return self.white_figures, self.black_figures

    def get_cell(self, pos: BoardPos) -> Cell | None:
        if len(self.board) <= pos[0] or len(self.board[pos[0]]) <= pos[1]:
            return None
        return self.board[pos[1]][pos[0]]

    def get_cell_position(self, cell):
        for row_idx, row in enumerate(self.board):
            for c_idx, c in enumerate(row):
                if c == cell:
                    return vec(c_idx, row_idx)
        return None

    def move_figure(self, pos_from: BoardPos, pos_to: BoardPos):
        cell_from = self.get_cell(pos_from)
        cell_to = self.get_cell(pos_to)

        figure_from = cell_from.content
        cell_to.content = figure_from
        cell_from.clear()

    def reset(self):
        self.board = self.create_init_state()

    def set_cell_content(self, pos_x, pos_y, content: Figure | None):
        self.board[pos_y][pos_x].content = content
