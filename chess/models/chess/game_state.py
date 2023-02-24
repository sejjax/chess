# Object represents chess game state

from .board import Board
from .figure import FigureColor


class GameState:
    def __init__(
            self,
            is_game_end: bool = False,
            winner: FigureColor | None = None,
            current_step_player: FigureColor = FigureColor.WHITE,
            board: Board = Board(),
            was_figure_moved: dict = None
    ) -> None:
        self.is_game_end = is_game_end
        self._winner = None
        self.winner = winner
        self.current_step_player = current_step_player
        self.board = board
        self.was_figure_moved = was_figure_moved

        if self.was_figure_moved is None:
            self.was_figure_moved = {}

            for row in self.board.board:
                for cell in row:
                    figure = cell.content
                    if figure is not None:
                        self.was_figure_moved[figure] = False

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, val):
        self.is_game_end = val is not None
        self._winner = val
