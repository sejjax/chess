from chess.models.chess.constants import TOP_BORDER, BOTTOM_BORDER
from chess.models.chess.figures import FigureColor


def get_side_by_color(color):
    return TOP_BORDER if color == FigureColor.BLACK else BOTTOM_BORDER
