from .board import Board
from .figure import FigureColor


class GameState:
    def __init__(
            self,
            is_game_end: bool = False,
            winner: FigureColor | None = None,
            current_step_player: FigureColor = FigureColor.WHITE,
            board: Board = Board()
    ) -> None:
        self.is_game_end = is_game_end
        self._winner = None
        self.winner = winner
        self.current_step_player = current_step_player
        self.board = board

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, val):
        self.is_game_end = val is not None
        self._winner = val
