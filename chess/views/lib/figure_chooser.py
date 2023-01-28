from ..lib.board import Grid, Layered
from ...lib.vec import vec


class FigureChooserGrid(Grid):
    def __init__(self):
        GRID = vec(4, 1)
        super(FigureChooserGrid, self).__init__(GRID)


class FigureChooser(FigureChooserGrid):
    def __init__(self, cell_size):
        super(FigureChooser, self).__init__(cell_size)