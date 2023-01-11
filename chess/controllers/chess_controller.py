from chess.models.chess.chess_service import ChessService
from .._types import AbstractController
from abc import ABC

from ..models.chess.board import Board
from ..models.chess.games.game import GamePlayer
from ..models.chess.games.local_game import LocalGame
from ..models.chess.party import Party
from ..models.chess.game_state import GameState
from ..lib.singleton import singleton


class AbstractChessController(AbstractController, ABC):
    pass


@singleton
class ChessController(AbstractController):
    def __init__(self, chess: ChessService) -> None:
        self.chess = chess
        self.party: Party | None = None

    def get_figure_available_cells(self, pos):
        cell = self.party.game.board.get_cell(pos)
        return self.party.game.get_figure_available_cells(cell)

    def create_game(self):
        board = Board().build()
        state = GameState(board=board)
        self.party = Party.new(LocalGame, state)
        return self.party.game.board

    def get_board(self):
        return self.party.game.board

    def _get_current_player(self) -> GamePlayer:
        return self.party.game.get_current_player()

    def do_current_player_step(self, from_pos, to_pos):
        player = self._get_current_player()
        player.do_step(from_pos, to_pos)

    def get_current_player_color(self):
        return self._get_current_player().color