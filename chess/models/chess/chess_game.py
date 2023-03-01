from abc import ABC, abstractmethod
from typing import Type

from chess.lib.vec import vec
from chess.models.chess.figures import Figure


class ChessGame(ABC):
    @abstractmethod
    def do_peace(self, pos_from: vec, pos_to: vec, pawn_transform_into: Type[Figure]) -> bool:
        pass

    @abstractmethod
    def get_available_cells(self, pos: vec) -> list[vec]:
        pass

    @abstractmethod
    def will_pawn_transform(self, pos_from: vec, pos_to: vec) -> bool:
        pass
