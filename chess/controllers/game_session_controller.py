from typing import Type

from chess.lib.vec import vec
from chess.models.chess.chess_game import ChessGame
from chess.models.chess.figures import Figure


class GameSessionController(ChessGame):

    def __init__(self, game_engine: ChessGame):
        self.game_engine = game_engine

    def do_peace(self, pos_from, pos_to, transform_pawn_into: Type[Figure]):
        self.game_engine.do_peace(pos_from, pos_to, transform_pawn_into)

    def get_available_cells(self, position) -> list[vec]:
        return self.game_engine.get_available_cells(position)

    def do_pawn_peace_transform(self, pos_from, pos_to, figure):
        return self.do_pawn_peace_transform(pos_from, pos_to, figure)

    def will_pawn_transform(self, pos_from, pos_to) -> bool:
        return self.will_pawn_transform(pos_from, pos_to)

    def setup_on_game_end_callback(self, callback):
        pass
