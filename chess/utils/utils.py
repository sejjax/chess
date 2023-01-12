from typing import Literal

from chess.models.chess.figure import FigureColor
from ..lib.vec import vec
from ..models.chess.board import MIN_BORDER, MAX_BORDER, Board, Cell


def invert_color(color):
    COLOR_INVERT = {
        FigureColor.WHITE: FigureColor.BLACK,
        FigureColor.BLACK: FigureColor.WHITE
    }
    return COLOR_INVERT[color]


def belongs_to_range(from_num, to_num, num, including_from=False, including_to=False):
    is_num_greater = from_num <= num if including_from else from_num < num
    is_num_less = to_num >= num if including_to else to_num > num
    return is_num_greater and is_num_less


def none_filter(iterable):
    return filter(lambda i: i is not None, iterable)


def is_board_belong(pos: vec):
    def _f(val):
        return belongs_to_range(MIN_BORDER, MAX_BORDER, val, True, True)

    return _f(pos.x) and _f(pos.y)


def positions_to_cells(board: Board, positions: list[vec]):
    return list(map(lambda pos: board.get_cell(pos), positions))


def cells_to_positions(board: Board, cells: list[Cell]):
    return list(map(lambda cell: board.get_cell_position(cell), cells))


def is_empty_pos(board: Board, pos):
    return board.get_cell(pos).content is None


def get_direction_by_color(color: FigureColor) -> int:
    return 1 if color == FigureColor.BLACK else -1


def filterlist(fn, iterable):
    return list(filter(fn, iterable))
