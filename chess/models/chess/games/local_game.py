from chess.utils.utils import invert_color
from .game import Game, GamePlayer, WINNER_GAME_END_MAP, GameEnd
from ..figure import FigureType, FigureColor
from ..game_state import GameState

PLAYERS_COUNT = 2
class LocalGame(Game):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, LocalGamePlayer)

    def do_step(self, from_pos, to_pos):
        self.board.move_figure(from_pos, to_pos)

        king_cells = []
        for row in self.board.board:
            for cell in row:
                if cell.content and cell.content.kind == FigureType.KING:
                    king_cells.append(cell)

        return king_cells

    def change_current_step_player(self):
        next_player_index = (self.players.index(self.game_state.current_step_player) + 1) % PLAYERS_COUNT
        next_player = self.players[next_player_index]
        self.game_state.current_step_player = next_player

    def change_current_player(self):

        current_player = self.get_current_player()
        current_step_player_index = self.players.index(current_player)
        next_player_index = (current_step_player_index + 1) % PLAYERS_COUNT
        self.game_state.current_step_player = self.players[next_player_index].color
        return self.game_state.current_step_player

    def end_game(self, winner_color: FigureColor | None):
        self.game_state.game_end = WINNER_GAME_END_MAP[winner_color]
        if self.game_state.game_end == GameEnd.STALEMATE:
            for player in self.players:
                player.on_stalemate()
        winner = self.get_player_by_color(winner_color)
        loser_color = invert_color(winner_color)
        loser = self.get_player_by_color(loser_color)

        winner.on_win()
        loser.on_lose()
        return winner


class LocalGamePlayer(GamePlayer):
    """Just Interface to interracting with Game Engine by a player"""

    def __init__(self, game_engine: LocalGame, color: FigureColor) -> None:
        super().__init__(game_engine, color)

    def do_step(self, from_pos, to_pos):
        from_cell = self._get_board_cell(from_pos)
        moved_figure = from_cell.content
        if moved_figure is None or moved_figure.color != self.color:
            return False
        to_cell = self._get_board_cell(to_pos)
        available_cells = self.game_engine.get_figure_available_cells(from_cell)
        search = list(filter(lambda _cell: to_pos == _cell, available_cells))
        if len(search) == 0:
            return False
        self.game_engine.board.move_figure(tuple(from_pos), tuple(to_pos))
        self.game_engine.change_current_player()
        return True
