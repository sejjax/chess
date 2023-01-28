from typing import Type

from chess.config.config import CONFIG
from chess.lib.vec import vec
from chess.utils.utils import invert_color, get_direction_by_color
from .game import Game, GamePlayer, WINNER_GAME_END_MAP, GameEnd
from .game_mode import GameMode
from ..constants import BOTTOM_BORDER, TOP_BORDER
from ..figure import FigureColor, King, Figure, Pawn, Rook
from ..game_state import GameState

PLAYERS_COUNT = 2


class LocalGame(Game):
    def __init__(self, game_state: GameState, game_mode: GameMode):
        super().__init__(game_state, game_mode, LocalGamePlayer)

    def do_step(self, from_pos, to_pos):
        self.move_figure(from_pos, to_pos)

        king_cells = []
        for row in self.board.board:
            for cell in row:
                if cell.content and type(cell.content) == King:
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


class InvalidStepMethodException(Exception):
    def __init__(self):
        super().__init__('You must use only process_step in this case')


class LocalGamePlayer(GamePlayer):
    """Just Interface to interracting with Game Engine by a player"""

    def __init__(self, game_engine: LocalGame, color: FigureColor) -> None:
        super().__init__(game_engine, color)

    def process_step(self, from_pos, to_pos, pawn_transform_into: Type[Figure] = None):
        # FIXME move to game engine
        # The Order and Hierarcy of functions calling
        # process_step -> | is_allowed_step | -> process_any_figure_step -> game_engine.move_figure
        #                                               or
        #                                   | -> process_pawn_step  | -> step_with_pawn_transform
        #                                                           | -> process_any_figure_step
        #                                               or
        #                                   | -> process_king_step       -> game_engine.castle_king

        if not self.is_allowed_step(from_pos, to_pos):
            return False

        moved_figure = self.get_board_cell(from_pos).content

        def process_any_figure_step(from_pos, to_pos):
            self.game_engine.move_figure(tuple(from_pos), tuple(to_pos))
            return True

        def process_pawn_step(from_pos, to_pos, transform_to):
            check = self.game_engine.will_pawn_transform(from_pos, to_pos)
            if not check:
                return process_any_figure_step(from_pos, to_pos)

            figure = self.get_board_cell(from_pos).content
            enemy_border = BOTTOM_BORDER if figure.color == FigureColor.BLACK else TOP_BORDER
            if type(figure) != Pawn:
                return False
            if to_pos.y != enemy_border:
                return False

            prev_cell = self.get_board_cell(from_pos)
            prev_cell.clear()
            new_cell = self.get_board_cell(to_pos)
            new_cell.content = transform_to(figure.color)
            return True

        def process_king_step(from_pos, to_pos):
            figure = self.game_engine.get_figure(to_pos)

            if type(figure) == Rook:
                self.game_engine.castle_king(from_pos, to_pos)
                return True
            return process_any_figure_step(from_pos, to_pos)

        moved_figure_type = type(moved_figure)

        if moved_figure_type == Pawn:
            res = process_pawn_step(from_pos, to_pos, pawn_transform_into)
        elif moved_figure_type == King:
            res = process_king_step(from_pos, to_pos)
        else:
            res = process_any_figure_step(from_pos, to_pos)
        if not res:
            return False

        if self.game_engine.game_mode.step_by_step_play:
            self.game_engine.change_current_player()





    def do_step(self, from_pos, to_pos):
        pass

    def is_allowed_step(self, from_pos, to_pos, transform_to: Type[Figure] = None):
        # FIXME move to game engine
        from_cell = self.get_board_cell(from_pos)
        moved_figure = from_cell.content



        if moved_figure is None:
            return False
        step_by_step_check = moved_figure.color != self.color and self.game_engine.game_mode.step_by_step_play
        if step_by_step_check:
            return False


        available_cells = self.game_engine.get_figure_available_cells(from_cell)
        search = list(filter(lambda _cell: to_pos == _cell, available_cells))
        if len(search) == 0:
            return False
        return True
