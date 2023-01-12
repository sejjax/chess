import npyscreen

from ..lib.singleton import singleton
from .._types import AbstractView, AbstractController
from abc import ABC, abstractmethod
from ..controllers.chess_controller import AbstractChessController, ChessController
from .utils import *
from .constants import *
from .widgets.modern_board_widget import BoardWidget


class AbstractChessView(AbstractView, ABC):
    @abstractmethod
    def __init__(self, controller: AbstractController) -> None:
        pass


class EnterExitCallbacks:
    def on_enter(self):
        pass

    def on_exit(self):
        pass


class BoardForm(EnterExitCallbacks, npyscreen.ActionFormMinimal):
    board: any
    chess_controller: ChessController
    board_widget: BoardWidget

    def create(self):
        self.chess_controller = ChessController()
        self.chess_controller.create_game()
        self.board_widget = self.add_widget(BoardWidget, name="Cool Board Widget ")

    def on_exit(self):
        self.chess_controller.create_game()
        self.board_widget.reset()


    def on_enter(self):
        pass

    def on_ok(self):
        navigate_to(self, CHOOSE_GAME_STYLE)


class ChooseGameStyleForm(npyscreen.ActionFormMinimal):
    local_game: any
    net_game: any

    def create(self):
        super(ChooseGameStyleForm, self).create()
        # This line is not strictly necessary: the API promises that the create method does nothing by default.
        # I've omitted it from later example code.

        self.local_game = navigate_to_button(self, 'Local Game', LOCAL_GAME_FORM)
        self.net_game = navigate_to_button(self, 'Network Game', MAIN_FORM)
        self.back = navigate_to_button(self, 'Back', MAIN_FORM)

    def on_ok(self):
        # print('FUck')
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
        self.addForm(LOCAL_GAME_FORM, BoardForm, name="Local Chess Game", color="WARNING")


@singleton
class ChessView(AbstractChessView):
    def __init__(self, controller: AbstractChessController) -> None:
        self.chess_view = _ChessView(controller)

    def run(self):
        self.chess_view.run()
