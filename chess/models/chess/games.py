from abc import ABC

from chess.models.chess.board import Board
from chess.models.chess.game_mode import GameMode
from chess.models.chess.game_state import GameState


class Game(ABC):
    board: Board
    game_mode: GameMode
    game_state: GameState


class ClassicGame(Game):
    def __init__(self):
        self.board = Board.build()
        self.game_mode = GameMode(True)
        self.game_state = GameState(board=self.board)


class DebugGame(Game):
    def __init__(self, string_map: str = None):

        if string_map is not None:
            self.board = Board.build_from_string(string_map)
        else:
            self.board = Board.build()

        self.game_mode = GameMode(False)
        self.game_state = GameState(board=self.board)
