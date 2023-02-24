from npyscreen import NotEnoughSpaceForWidget

from ..lib.singleton import singleton
from ..controllers.chess_controller import ChessController
from .utils import *
from .constants import *
from .widgets.board_widget import BoardWidget


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
    back: any

    def create(self):
        super(ChooseGameStyleForm, self).create()
        self.local_game = navigate_to_button(self, 'Local Game', LOCAL_GAME_FORM)
        self.back = navigate_to_button(self, 'Back', MAIN_FORM)

    def on_ok(self):
        navigate_to(self, MAIN_FORM)


class ChooseSavedGame(npyscreen.FormWithMenus):
    back: any
    def create(self):
        super(ChooseSavedGame, self).create()
        self.back = navigate_to_button(self, 'Back', CHOOSE_GAME_STYLE)


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
    def __init__(self) -> None:
        super().__init__()

    def onStart(self):
        self.addForm(MAIN_FORM, MainForm, name="The Chess", color="IMPORTANT")
        self.addForm(CHOOSE_GAME_STYLE, ChooseGameStyleForm, name="Choose Game Style", color="WARNING")
        self.addForm(LOCAL_GAME_FORM, BoardForm, name="Local Chess Game", color="WARNING")
        self.addForm(CHOOSE_SAVED_GAME, ChooseSavedGame, name="Saved Games", color="WARNING")


@singleton
class ChessView:
    def __init__(self) -> None:
        self.chess_view = _ChessView()

    def run(self):
        try:
            self.chess_view.run()
        except NotEnoughSpaceForWidget:
            print('Not enough space. Please increase the size of the terminal.')

    def exit(self):
        exit_from_view(self.chess_view.getForm(MAIN_FORM))
