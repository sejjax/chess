import npyscreen
from chess.models.chess.board import Board, BOARD_SIDE_SIZE
from chess.views.constants import BOARD_SIDE_X, BOARD_SIDE_Y
from ..lib.board import MainBoard, BoardRenderer
from ..utils import get_pad
from ...controllers.chess_controller import ChessController
from ...lib.vec import vec
from ...lib.styled_string import addstr, bold, underline

CELL_SIZE = vec(3, 5)

class BoardWidget(npyscreen.widget.Widget):

    def __init__(self, screen, board: Board = None, relx=0, rely=0, name=None, value=None, width=False, height=False,
                 max_height=False, max_width=False, editable=True, hidden=False, color='DEFAULT', use_max_space=False,
                 check_value_change=True, check_cursor_move=True, value_changed_callback=None, **keywords):
        super().__init__(screen, relx, rely, name, value, width, height, max_height, max_width, editable, hidden, color,
                         use_max_space, check_value_change, check_cursor_move, value_changed_callback, **keywords)

        self.pos = CELL_SIZE

        self.chess_controller = ChessController()
        self.chess_controller.create_game()

        _board = self.chess_controller.get_board()
        self.board = MainBoard(vec(5, 3), _board)

        self.board_renderer = BoardRenderer(self.pos, self.board)
        self._set_up_handlers()

    def _set_up_handlers(self):
        top, bottom, left, right = self.board.get_movement_handlers()
        select_cell_handler = self.board.get_select_cell_handler()
        self.add_handlers({
            ord('w'): self.move_update(top),
            ord('s'): self.move_update(bottom),
            ord('a'): self.move_update(left),
            ord('d'): self.move_update(right),
            ord('k'): self.move_update(select_cell_handler)
        })

    def move_update(self, callback):
        def wrapper(_):
            callback()
            self.update()

        return wrapper

    def calculate_area_needed(self):
        return CELL_SIZE.x * BOARD_SIDE_SIZE, CELL_SIZE.y * BOARD_SIDE_SIZE

    def update(self, clear=True):
        if clear:
            self.clear()
        screen = get_pad(self)

        self.board_renderer.display(screen)

    def make_attributes_list(self, unicode_string, attribute):
        return super().make_attributes_list(unicode_string, attribute)
