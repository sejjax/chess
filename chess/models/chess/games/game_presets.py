from chess.models.chess.board import Board
from chess.models.chess.game_state import GameState
from chess.models.chess.games.game_mode import GameMode
from chess.models.chess.games.local_game import LocalGame
from chess.models.chess.party import Party


class ClassicalGame:
    def __init__(self):
        self.board = Board.build()
        self.game_mode = GameMode(True)
        self.game_state = GameState(board=self.board)
        self.party = Party.new(LocalGame, self.game_state, self.game_mode)


class DebugGame:
    def __init__(self, string_map: str = None):

        if string_map is not None:
            self.board = Board.build_from_string(string_map)
        else:
            self.board = Board.build()

        self.game_mode = GameMode(False)
        self.game_state = GameState(board=self.board)
        self.party = Party.new(LocalGame, self.game_state, self.game_mode)