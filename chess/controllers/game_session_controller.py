from typing import Type

from chess.lib.vec import vec
from chess.models.chess.chess_engine import AbstractChessEngine
from chess.models.chess.chess_game import ChessGame
from chess.models.chess.figures import Figure


class GameSessionController(ChessGame):

    def __init__(self, game_engine: AbstractChessEngine):
        self.game_engine = game_engine

    def do_peace(self, pos_from, pos_to, transform_pawn_into: Type[Figure]):
        self.game_engine.do_peace(pos_from, pos_to, transform_pawn_into)

    def get_available_cells(self, position) -> list[vec]:
        return self.game_engine.get_available_cells(position)

    def do_pawn_peace_transform(self, pos_from, pos_to, figure):
        return self.do_pawn_peace_transform(pos_from, pos_to, figure)

    def will_pawn_transform(self, pos_from, pos_to) -> bool:
        return False
        # return self.will_pawn_transform(pos_from, pos_to)

    def setup_on_game_end_callback(self, callback):
        pass

    def get_board(self):
        return self.game_engine.game_state.board

    def get_current_player_color(self):
        return self.game_engine.game_state.current_step_player

    def get_game_mode(self):
        return self.game_engine.game_mode
