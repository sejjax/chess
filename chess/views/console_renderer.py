from ..utils.utils import invert_color
from ..models.chess.board import Board
from ..models.chess.figure import FigureColor
from .constants import LETTERS_FIGURE_MAP, CURRENT_MAP, ALPHA, NUMBERS


def symbol_figure_map(figure_type, figure_color: FigureColor):
    if CURRENT_MAP == LETTERS_FIGURE_MAP:
        return LETTERS_FIGURE_MAP[figure_type]


EMPTY_FIELD = '.'
AVAILABLE_CELL = 'x'


class BoardRenderer:
    def __init__(self) -> None:
        pass

    def string(self, board: Board, awailable_cells: list = [], invert_colors=False):
        str_rows = []
        for row in board.board:
            str_row = ''
            str_figures = []
            for cell in row:
                figure = cell.content
                if figure is not None:
                    color = figure.color if not invert_colors else invert_color(figure.color)
                if cell in awailable_cells:
                    str_figure = AVAILABLE_CELL
                else:
                    str_figure = EMPTY_FIELD if figure is None else symbol_figure_map(figure.kind, color)
                str_figures += [str_figure]
                str_row = " ".join(str_figures)
            str_rows += [str_row]
        return "\n".join(str_rows)
