from enum import Enum


class FigureType(Enum):
    KING = 0
    QUIN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHTS = 4
    PAWN = 5


class FigureColor(Enum):
    BLACK = 0
    WHITE = 1


class Figure:
    kind: FigureType
    color: FigureColor

    def __init__(self, kind: FigureType, color: FigureColor) -> None:
        self.kind = kind
        self.color = color
