from .controllers.chess_controller import ChessController
from .views.chess_view import ChessView
import chess.config.config


class App:
    def __init__(self) -> None:
        # TODO: Move logic from controller to service and model
        chess_controller = ChessController()
        self.chess_view = ChessView()

    def run(self):
        self.chess_view.run()

    def exit(self):
        self.chess_view.exit()
