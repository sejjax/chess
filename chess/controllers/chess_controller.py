from chess.models.chess.games import ClassicGame, DebugGame
from .base import BaseController
from .constants import DEBUG_MOD_MAP
from .game_session_controller import GameSessionController
from ..config.config import CONFIG
from ..models.chess.chess_engine import ChessEngine


class ChessController(BaseController):

    def __init__(self):
        pass

    def create_game(self) -> GameSessionController:
        if CONFIG.debug:
            return self.create_debug_game()
        return self.create_local_game()

    def create_local_game(self) -> GameSessionController:
        game = ClassicGame()
        # TODO: Как мне вынести логику инициализации движка из контроллера на более высокий уровень?
        game_engine = ChessEngine(game)
        return GameSessionController(game_engine)

    def create_debug_game(self) -> GameSessionController:
        game = DebugGame(DEBUG_MOD_MAP)
        game_engine = ChessEngine(game)
        return GameSessionController(game_engine)
