from bidict import bidict

from ..lib.vec import vec
from ..models.chess.constants import BOARD_SIDE_SIZE
from ..models.chess.figures import Knight, Bishop, Rook, Quin, King, Pawn

ALPHA = 'ABCDEFGH'
NUMBERS = '12345678'

LETTERS_FIGURE_MAP = bidict({
    King: 'K',
    Quin: 'Q',
    Rook: 'R',
    Bishop: 'B',
    Knight: 'H',
    Pawn: 'P'
})

CURRENT_MAP = LETTERS_FIGURE_MAP

MAIN_FORM = 'MAIN'
CHOOSE_GAME_STYLE = 'CHOOSE_MAIN_GAME'
LOCAL_GAME_FORM = 'LOCAL_GAME'
NETWORK_GAME_FORM = 'NETWORK_GAME'
CHOOSE_SAVED_GAME = 'CHOOSE_SAVED_GAME'


CELL_SIZE = 4
SIDE_SIZE = BOARD_SIDE_SIZE * CELL_SIZE

FILLED = '#'
EMPTY = '.'
CELL_X = 5
CELL_Y = 3
BOARD_SIDE_Y = BOARD_SIDE_SIZE * CELL_Y
BOARD_SIDE_X = BOARD_SIDE_SIZE * CELL_X
CELL_MIDDLE_Y = 1

CELL_SIZE = vec(CELL_X, CELL_Y)