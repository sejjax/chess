from .controllers.chess_controller import ChessController
from .lib.event_bus import EventBus
from .views.chess.view import ChessViewApp

VIEW_EVENT_BUS = 'VIEW_EVENT_BUS'


class App:
    def __init__(self) -> None:
        self.event_bus = EventBus(VIEW_EVENT_BUS)
        self.controller = ChessController()
        self.chess_view = ChessViewApp(self.controller, self.event_bus)

    def run(self):
        self.chess_view.run()

    def exit(self):
        self.chess_view.exit()
