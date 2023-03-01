from chess.views.chess.local_game import LocalChessGameView
from chess.views.lib.view import ScreenFormBaseNew
from chess.views.utils import make_button, navigate_to_button, exit_from_view


class MainMenuView(ScreenFormBaseNew):
    start_game: any
    exit_button: any

    def create(self):
        self.start_game = navigate_to_button(self, 'Start Game', LocalChessGameView)
        self.exit_button = make_button(self, 'Exit', self.on_cancel)

    def on_cancel(self):
        exit_from_view(self)
