from .models.chess.chess_service import ChessService, ChessModel
from .controllers.chess_controller import ChessController
from .views.chess_view import ChessView
from .config.config import configure


class App:
    def __init__(self) -> None:
        configure()

        chess_model = ChessModel()
        chess_service = ChessService(chess_model, chess_model)
        chess_controller = ChessController(chess_service)
        self.chess_view = ChessView(chess_controller)
    
    def run(self):
        self.chess_view.run()

