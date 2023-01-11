import curses

from ...lib.vec import vec
from .figure import Figure, FigureColor, FigureType
from chess.models.chess.constants import *


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
            # Generating Matrix 8x8
            self.board = [[Cell() for _ in range(BOARD_SIDE_SIZE)] for _ in range(BOARD_SIDE_SIZE)]

        self.white_figures = []
        self.black_figures = []

    @staticmethod
    def build():
        board = Board()

        for row, row_list in enumerate(board.board):
            for column, cell in enumerate(row_list):
                figure_color = FigureColor.BLACK if row < 4 else FigureColor.WHITE

                is_empty_cell = 1 < row < 6

                # Implementing default figure location
                figure_type = None
                if row == 1 or row == 6:
                    figure_type = FigureType.PAWN
                elif row in [LEFT_BORDER, RIGHT_BORDER]:
                    if column in [TOP_BORDER, BOTTOM_BORDER]:
                        figure_type = FigureType.ROOK
                    elif column in [1, 6]:
                        figure_type = FigureType.KNIGHTS
                    elif column in [2, 5]:
                        figure_type = FigureType.BISHOP
                    elif column == 3:
                        figure_type = FigureType.KING
                    elif column == 4:
                        figure_type = FigureType.QUIN

                if is_empty_cell:
                    figure = None
                else:
                    figure = Figure(figure_type, figure_color)

                board.set_cell_content(column, row, figure)

                group = board.white_figures if figure_color == FigureColor.WHITE else board.black_figures
                group.append(figure)

        return board

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

    def set_cell_content(self, pos_x, pos_y, content: Figure | None):
        self.board[pos_y][pos_x].content = content
