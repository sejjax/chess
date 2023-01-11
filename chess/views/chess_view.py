from .widgets.board_widget import BoardWidget
from ..lib.singleton import singleton
from ..models.chess.board import Board
from .._types import AbstractView, AbstractController
from abc import ABC, abstractmethod
from ..controllers.chess_controller import AbstractChessController
from .utils import *
from .constants import *
from .widgets.modern_board_widget import BoardWidget


class AbstractChessView(AbstractView, ABC):
    @abstractmethod
    def __init__(self, controller: AbstractController) -> None:
        pass


class BoardForm(npyscreen.Form):
    board: any

    def create(self):
        super(BoardForm, self).create()



class ChooseGameStyleForm(npyscreen.Form):
    local_game: any
    net_game: any

    def create(self):
        # This line is not strictly necessary: the API promises that the create method does nothing by default.
        # I've omitted it from later example code.
        self.board = Board.build()
        self.add_widget(BoardWidget, name="Cool Board Widget", board=self.board)

        self.local_game = navigate_to_button(self, 'Local Game', LOCAL_GAME_FORM)
        self.net_game = navigate_to_button(self, 'Network Game', MAIN_FORM)

    def on_cancel(self):
        navigate_to(self, MAIN_FORM)


class MainForm(npyscreen.FormBaseNew):
    start_game: any
    exit_button: any

    def create(self):
        super(MainForm, self).create()
        self.start_game = make_button(self, 'Start Game', self.on_start_game)
        self.exit_button = make_button(self, 'Exit', self.on_cancel)

    def on_start_game(self):
        navigate_to(self, CHOOSE_GAME_STYLE)

    def on_cancel(self):
        exit_from_view(self)


class _ChessView(npyscreen.NPSAppManaged):
    def __init__(self, controller: AbstractChessController) -> None:
        super().__init__()

    def onStart(self):
        self.addForm(MAIN_FORM, MainForm, name="The Chess", color="IMPORTANT")
        self.addForm(CHOOSE_GAME_STYLE, ChooseGameStyleForm, name="Choose Game Style", color="WARNING")
        self.addForm(LOCAL_GAME_FORM, BoardForm, name="Chess Game (Board Form)", color="WARNING")


@singleton
class ChessView(AbstractChessView):
    def __init__(self, controller: AbstractChessController) -> None:
        self.chess_view = _ChessView(controller)

    def run(self):
        self.chess_view.run()
