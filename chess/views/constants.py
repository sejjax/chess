from ..models.chess.figure import FigureType, FigureColor
from ..models.chess.board import BOARD_SIDE_SIZE

SYMBOL_FIGURE_MAP = {
    (FigureType.KING, FigureColor.WHITE): '♔',
    (FigureType.QUIN, FigureColor.WHITE): '♕',
    (FigureType.ROOK, FigureColor.WHITE): '♖',
    (FigureType.BISHOP, FigureColor.WHITE): '♗',
    (FigureType.KNIGHTS, FigureColor.WHITE): '♘',
    (FigureType.PAWN, FigureColor.WHITE): '♙',
    (FigureType.KING, FigureColor.BLACK): '♚',
    (FigureType.QUIN, FigureColor.BLACK): '♛',
    (FigureType.ROOK, FigureColor.BLACK): '♜',
    (FigureType.BISHOP, FigureColor.BLACK): '♝',
    (FigureType.KNIGHTS, FigureColor.BLACK): '♞',
    (FigureType.PAWN, FigureColor.BLACK): '♟',
}

ALPHA = 'ABCDEFGH'
NUMBERS = '12345678'

LETTERS_FIGURE_MAP = {
    FigureType.KING: 'K',
    FigureType.QUIN: 'Q',
    FigureType.ROOK: 'R',
    FigureType.BISHOP: 'B',
    FigureType.KNIGHTS: 'H',
    FigureType.PAWN: 'P'
}
CURRENT_MAP = LETTERS_FIGURE_MAP

MAIN_FORM = 'MAIN'
CHOOSE_GAME_STYLE = 'CHOOSE_MAIN_GAME'
LOCAL_GAME_FORM = 'LOCAL_GAME'
NETWORK_GAME_FORM = 'NETWORK_GAME'


CELL_SIZE = 4
SIDE_SIZE = BOARD_SIDE_SIZE * CELL_SIZE
ASPECT = 2

FILLED = '#'
EMPTY = '.'
CELL_X = 5
CELL_Y = 3
BOARD_SIDE_Y = BOARD_SIDE_SIZE * CELL_Y
BOARD_SIDE_X = BOARD_SIDE_SIZE * CELL_X
CELL_MIDDLE_Y = 1