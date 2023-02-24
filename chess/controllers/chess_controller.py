from abc import ABC

from .constants import DEBUG_MOD_MAP
from ..config.config import CONFIG
from ..models.chess.games.game import GamePlayer
from ..models.chess.games.game_presets import DebugGame, ClassicalGame
from ..models.chess.party import Party
from ..lib.singleton import singleton

@singleton
class ChessController:
    def __init__(self) -> None:
        self.party: Party | None = None
        self.pawn_transform_into = None

    def get_figure_available_cells(self, pos):
        cell = self.party.game.board.get_cell(pos)
        return self.party.game.get_figure_available_cells(cell)

    def create_game(self):
        if CONFIG.debug:
            game = DebugGame(DEBUG_MOD_MAP)
        else:
            game = ClassicalGame()
        self.party = game.party
        return self.party.game.board

    def get_board(self):
        if self.party is None:
            raise Exception('You can\'t get board without created game.')
        return self.party.game.board

    def get_game_mode(self):
        return self.party.game.game_mode

    def _get_current_player(self) -> GamePlayer:
        return self.party.game.get_current_player()

    def do_current_player_step(self, from_pos, to_pos, transform_pawn_into = None):
        player = self._get_current_player()
        player.process_step(from_pos, to_pos, transform_pawn_into)

    def get_current_player_color(self):
        return self._get_current_player().color

    def will_pawn_transform(self, from_pos, to_pos):
        return self.party.game.will_pawn_transform(from_pos, to_pos)
