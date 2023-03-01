from chess.controllers.chess_controller import ChessController
from chess.controllers.game_session_controller import GameSessionController
from chess.views.lib.view import ScreenActionFormMinimal
from chess.views.utils import navigate_to
from chess.views.widgets.board_widget import BoardWidget


class LocalChessGameView(ScreenActionFormMinimal):
    controller: ChessController
    game_controller: GameSessionController | None
    board_widget: any
    start: any

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self):
        self.game_controller = self.controller.create_game()
        self.board_widget = self.add_widget(BoardWidget, name="Cool Board Widget ",
                                            game_controller=self.game_controller)

    def on_enter(self):
        self.game_controller = self.controller.create_game()

        self.board_widget.reset()

    def on_ok(self):
        navigate_to(self, 'MainMenuView')
        self.game_controller = self.controller.create_game()
        self.board_widget.reset()

    def on_exit(self):
        self.game_controller = self.controller.create_game()
        self.board_widget.reset()
