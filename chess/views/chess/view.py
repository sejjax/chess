import npyscreen

from chess.controllers.chess_controller import ChessController
from chess.lib.event_bus import EventBus
from chess.views.chess.local_game import LocalChessGameView
from chess.views.chess.main_menu import MainMenuView
from chess.views.lib.view import ScreenAppView


class ChessViewApp(ScreenAppView):
    controller: ChessController

    def __init__(self, controller: ChessController, event_bus: EventBus):
        super().__init__(controller, event_bus)

    def on_start(self):
        self.add_view(MainMenuView, name="Main view", color='WARNING')
        self.add_view(LocalChessGameView, name="Local Chess Game View", color='Ok')

    def run(self):
        try:
            super().run()
        except npyscreen.NotEnoughSpaceForWidget:
            print('Not enough space. Please increase the size of the terminal')
