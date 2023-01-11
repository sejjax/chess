from chess._types import AbstractModel
from abc import ABC
from typing import Type

from chess.models.chess.games.game import AbstractGame


class AbstractChessModel(AbstractModel):
    pass


class ChessModel(AbstractChessModel, ABC):
    def make_step(self):
        pass

    def start_game(self, game_kind_class: Type[AbstractGame]):
        return game_kind_class()
