from enum import Enum


class FigureColor(Enum):
    BLACK = 0
    WHITE = 1


class Figure:
    color: FigureColor

    def __init__(self, color: FigureColor) -> None:
        self.color = color


class Pawn(Figure):
    def __init__(self, color):
        super(Pawn, self).__init__(color)


class Rook(Figure):
    def __init__(self, color):
        super(Rook, self).__init__(color)


class King(Figure):
    def __init__(self, color):
        super(King, self).__init__(color)


class Knight(Figure):
    def __init__(self, color):
        super(Knight, self).__init__(color)


class Quin(Figure):
    def __init__(self, color):
        super(Quin, self).__init__(color)


class Bishop(Figure):
    def __init__(self, color):
        super(Bishop, self).__init__(color)
