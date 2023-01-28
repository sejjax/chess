from typing import Type

from .game_mode import GameMode
from ..board import Board, Cell
from ..constants import LEFT_BORDER, TOP_BORDER, RIGHT_BORDER, BOTTOM_BORDER
from ..figure import FigureColor, Pawn, Rook, Bishop, Quin, Knight, King, Figure
from ..game_state import GameState

from enum import Enum

from abc import abstractmethod, ABC

from ....lib.vec import vec
from ....utils.utils import invert_color, is_board_belong, cells_to_positions, positions_to_cells, is_empty_pos, \
    get_direction_by_color, filterlist

TOP_DIRECTION = vec(0, -1)
RIGHT_DIRECTION = vec(1, 0)
BOTTOM_DIRECTION = vec(0, 1)
LEFT_DIRECTION = vec(-1, 0)

NORMAL_DIRECTIONS = [TOP_DIRECTION, RIGHT_DIRECTION, BOTTOM_DIRECTION, LEFT_DIRECTION]

TOP_RIGHT_DIRECTION = vec(1, -1)
RIGHT_BOTTOM_DIRECTION = vec(1, 1)
BOTTOM_LEFT_DIRECTION = vec(-1, 1)
LEFT_TOP_DIRECTION = vec(-1, -1)

DIAGONAL_DIRECTIONS = [TOP_RIGHT_DIRECTION, RIGHT_BOTTOM_DIRECTION, BOTTOM_LEFT_DIRECTION, LEFT_TOP_DIRECTION]

HORIZONTAL = [LEFT_DIRECTION, RIGHT_DIRECTION]
VERTICAL = [TOP_DIRECTION, BOTTOM_DIRECTION]

MIN_BORDERS = [LEFT_BORDER, TOP_BORDER]
MAX_BORDERS = [RIGHT_BORDER, BOTTOM_BORDER]


class GameEnd(Enum):
    STALEMATE = 0
    WHITE_WINNER = 1
    BLACK_WINNER = 2


GAME_END_WINNER_MAP = {
    GameEnd.WHITE_WINNER: FigureColor.WHITE,
    GameEnd.BLACK_WINNER: FigureColor.BLACK,
    GameEnd.STALEMATE: None
}

WINNER_GAME_END_MAP = {
    FigureColor.WHITE: GameEnd.WHITE_WINNER,
    FigureColor.BLACK: GameEnd.BLACK_WINNER,
    GameEnd.STALEMATE: None
}


def get_side_by_color(color):
    return TOP_BORDER if color == FigureColor.BLACK else BOTTOM_BORDER


class AbstractGamePlayer(ABC):
    pass

    """Just Interface to interacting with Game Engine by a player"""

    def __init__(self, game_engine: 'AbstractGame', color: FigureColor) -> None:
        self.color = color
        self.game_engine = game_engine

    def get_enemy_figures(self):
        pass

    def get_my_figures(self):
        pass

    def get_available_cells(self, pos_from):
        pass

    def make_step(self, from_pos, to_pos):
        pass

    def on_win(self):
        pass

    def set_on_win_callback(self, callback):
        pass

    def on_lose(self):
        pass

    def set_on_lose_callback(self, callback):
        pass

    def on_stalemate(self):
        pass

    def set_on_stalemate_callback(self, callback):
        pass

    def get_current_player(self) -> 'AbstractGamePlayer':
        pass


class AbstractGame(ABC):
    @abstractmethod
    def get_current_player(self) -> AbstractGamePlayer:
        pass

    @abstractmethod
    def do_step(self, from_pos, to_pos):
        pass


def game_name_player_color_map(player_color, game_end_state: GameEnd):
    return FigureColor.WHITE


def get_winner(game_end_state):
    return GAME_END_WINNER_MAP[game_end_state]


def get_loser(game_end_state):
    winner_color = get_winner(game_end_state)
    if winner_color is None:
        return None
    return invert_color(winner_color)


def throw_ray(board: Board, pos_from: vec, direction: vec):
    cells = []

    def condition():
        x_axis_check = LEFT_BORDER <= current_pos.x <= RIGHT_BORDER
        y_axis_check = TOP_BORDER <= current_pos.y <= BOTTOM_BORDER
        return x_axis_check and y_axis_check

    current_pos = pos_from.copy()

    while True:
        current_pos += direction
        if not condition():
            break
        cell = board.get_cell(current_pos)
        if cell is None:
            break
        cells.append(cell)

        figure = cell.content
        if figure is not None:
            break
    return cells


def throw_ray_cross(board: Board, pos_from: vec) -> list[Cell]:
    cells = []
    for direction in NORMAL_DIRECTIONS:
        cells += throw_ray(board, pos_from, direction)
    return cells


def throw_ray_cross_diagonal(board: Board, pos_from: vec) -> list[Cell]:
    cells = []
    for direction in DIAGONAL_DIRECTIONS:
        cells += throw_ray(board, pos_from, direction)
    return cells


AVAILABLE_RELATIVE_CELLS = [
    vec(-2, 1),
    vec(-1, 2),
    vec(1, 2),
    vec(2, 1),
    vec(2, -1),
    vec(1, -2),
    vec(-2, -1),
    vec(-1, -2),
]


def knights_awailable_cells(board: Board, pos_from: vec) -> list[Cell]:
    """Generate list of step cells for knight figures"""
    cells = []
    for rel_pos in AVAILABLE_RELATIVE_CELLS:
        absolute_pos = rel_pos + pos_from
        if not is_board_belong(absolute_pos):
            continue
        cell = board.get_cell(absolute_pos)
        cells.append(cell)
    return cells


def get_king_available_cells(board: Board, pos_from: vec) -> list[Cell]:
    RANGE = [-1, 0, 1]
    cells = []
    for i in RANGE:
        for j in RANGE:
            if i != 0 or j != 0:
                rel_pos = vec(i, j)
                abs_pos = pos_from + rel_pos
                if not is_board_belong(abs_pos):
                    continue
                cell = board.get_cell(abs_pos)
                if cell is None:
                    continue
                cells.append(cell)
    return cells


def is_figures_between_row_cells(board: Board, pos_from: vec, pos_to: vec):
    if pos_from.y != pos_to.y:
        return False
    x_from, x_to = pos_from.x, pos_to.x
    if x_from > x_to:
        x_from, x_to = x_to, x_from
    start = x_from + 1
    end = x_to
    for i in range(start, end):
        figure = board.get_cell((i, pos_from.y)).content
        if figure is not None:
            return False

    return True


class Game(AbstractGame, ABC):
    board: Board

    def __init__(self, game_state: GameState, game_mode: GameMode, cls_game_player: Type['GamePlayer']):
        self.game_state = game_state
        self.board = game_state.board

        white_figures, black_figures = self.board.get_figures()
        self.white_figures, self.black_figures = white_figures, black_figures

        self.white_player = cls_game_player(self, FigureColor.WHITE)
        self.black_player = cls_game_player(self, FigureColor.BLACK)

        self.players = [self.white_player, self.black_player]
        self.game_mode = game_mode

    def get_king_cells(self):
        king_cells = []
        for row in self.board.board:
            for cell in row:
                if cell.content and type(cell.content) == King:
                    king_cells.append(cell)

        return king_cells

    def get_figure(self, pos):
        return self.board.get_cell(pos).content

    def get_king_cell_by_color(self, color):
        cells = self.get_figures_cells_by_color_and_kind(color, King)
        return cells[0]

    def castle_king(self, king_pos, rook_pos):
        new_king_pos = king_pos.copy()
        new_rook_pos = rook_pos.copy()
        if king_pos.x > rook_pos.x:
            new_king_pos.x = 1
            new_rook_pos.x = 2
        else:
            new_king_pos.x = 6
            new_rook_pos.x = 5
        self.move_figure(king_pos, new_king_pos)
        self.move_figure(rook_pos, new_rook_pos)

    def is_able_to_castling(self, king_or_rook):
        return not self.was_figure_moved(king_or_rook)

    def get_figures_cells_by_color(self, color):
        cells = []
        for row in self.board.board:
            for i in row:
                figure = i.content
                if figure and figure.color == color:
                    cells.append(i)
        return cells

    def get_figures_cells_by_color_and_kind(self, color, kind):
        cells = self.get_figures_cells_by_color(color)
        return filterlist(lambda i: type(i.content) == kind, cells)

    def get_available_to_castling_rooks_cells(self):
        color = self.get_current_player().color
        king_cell = self.get_king_cell_by_color(color)
        if not self.is_able_to_castling(king_cell.content):
            return []
        king_pos = self.board.get_cell_position(king_cell)

        rooks_cells = self.get_figures_cells_by_color_and_kind(color, Rook)
        rooks_cells = filterlist(lambda i: self.is_able_to_castling(i.content), rooks_cells)
        rooks_cells = filterlist(lambda i: is_figures_between_row_cells(
            self.board,
            king_pos,
            self.board.get_cell_position(i)
        ), rooks_cells)
        return rooks_cells

    def get_figure_available_cells(self, cell: Cell):
        figure = cell.content
        cell_pos = self.board.get_cell_position(cell)

        if figure is None:
            return []

        allie_cells = set()
        for row in self.board.board:
            for cell in row:
                if cell.content and cell.content.color == figure.color:
                    allie_cells.add(cell)

        available_cells = []

        figure_type = type(figure)

        if figure_type == Pawn:
            is_on_started_pos = not self.was_figure_moved(figure)
            direction = get_direction_by_color(figure.color)
            cell_pos.y += direction

            def calculate_potential_attacking_cells(shift):
                _cell = cell_pos.copy()
                _cell.x += shift
                return _cell

            potential_attacking_cells_pos = [
                calculate_potential_attacking_cells(-1),
                calculate_potential_attacking_cells(1)
            ]
            potential_attacking_cells_pos = filterlist(is_board_belong, potential_attacking_cells_pos)

            potential_attacking_cells = positions_to_cells(self.board, potential_attacking_cells_pos)
            available_attacking_cells = filterlist(lambda _cell: _cell.content is not None, potential_attacking_cells)
            available_cells = available_attacking_cells

            vertical_cells = [cell_pos]

            if is_on_started_pos:
                additional_vertical_cell = cell_pos.copy()
                additional_vertical_cell.y += direction
                vertical_cells.append(additional_vertical_cell)

            if is_on_started_pos and self.board.get_cell(cell_pos).content:
                vertical_cells.remove(additional_vertical_cell)

            vertical_cells = filterlist(lambda i: is_empty_pos(self.board, i), vertical_cells)
            vertical_cells = positions_to_cells(self.board, vertical_cells)
            available_cells += vertical_cells

        elif figure_type == Rook:
            available_cells = throw_ray_cross(self.board, cell_pos)
        elif figure_type == Bishop:
            available_cells = throw_ray_cross_diagonal(self.board, cell_pos)
        elif figure_type == Quin:
            available_cells = [
                *throw_ray_cross(self.board, cell_pos),
                *throw_ray_cross_diagonal(self.board, cell_pos)
            ]
        elif figure_type == Knight:
            available_cells = knights_awailable_cells(self.board, cell_pos)
        elif figure_type == King:
            current_color = figure.color

            enemy_color = invert_color(current_color)
            enemy_king_cell = filterlist(lambda i: i.content.color == enemy_color, self.get_king_cells())
            enemy_king_available_cells = set()

            if len(enemy_king_cell) > 0:
                enemy_king_cell = enemy_king_cell[0]
                enemy_king_cell_pos = self.board.get_cell_position(enemy_king_cell)
                enemy_king_available_cells = set(get_king_available_cells(self.board, enemy_king_cell_pos))

            king_available_cells = get_king_available_cells(self.board, cell_pos)
            king_available_cells = set(king_available_cells)

            available_cells = list(king_available_cells - enemy_king_available_cells)

        available_cells = list(set(available_cells) - set(allie_cells))

        if figure_type == King:
            available_cells += self.get_available_to_castling_rooks_cells()

        available_cells = cells_to_positions(self.board, available_cells)
        return available_cells

    def get_current_player(self):
        return self.get_player_by_color(self.game_state.current_step_player)

    def get_figures_by_color(self, color: FigureColor):
        return self.white_figures if color == FigureColor.WHITE else self.black_figures

    def get_enemy_color(self):
        return invert_color(self.game_state.current_step_player)

    def is_king_in_dangerous(self):
        king_cell = self.get_king_cell_by_color(self.game_state.current_step_player)
        enemy_color = self.get_enemy_color()
        enemy_figures_cells = self.get_figures_cells_by_color(enemy_color)
        attacking_cells = []
        for cell in enemy_figures_cells:
            attacking_cells += self.get_figure_available_cells(cell)
        return king_cell in attacking_cells

    @abstractmethod
    def end_game(self, winner_color: FigureColor | None):
        pass

    def get_player_by_color(self, color: FigureColor):
        for player in self.players:
            if player.color == color:
                return player

    def turn_figure(self, pos, turn_to_cls: Type[Figure]):
        cell = self.board.get_cell(tuple(pos))
        cell.content = turn_to_cls(cell.content.color)
        return cell.content

    def move_figure(self, pos_from, pos_to):
        figure = self.board.get_cell(pos_from).content
        if figure is not None:
            self.game_state.was_figure_moved[figure] = True
        self.board.move_figure(pos_from, pos_to)

    def was_figure_moved(self, figure):
        return self.game_state.was_figure_moved[figure]

    def pawn_available_transform_cells(self, from_pos, to_pos):
        cell = self.board.get_cell(from_pos)
        figure = cell.content
        if figure is None or type(figure) != Pawn:
            return None

        color = figure.color
        available_cell_positions = self.get_figure_available_cells(cell)

        cells = []
        for pos in available_cell_positions:
            if to_pos.y == get_side_by_color(invert_color(color)):
                cell = self.board.get_cell(pos)
                cells.append(cell)
        return cells

    def will_pawn_transform(self, from_pos, to_pos):
        res = self.pawn_available_transform_cells(from_pos, to_pos)

        if res is None:
            return False
        return len(res) > 0



class GamePlayer(ABC):
    """Just Interface to interacting with Game Engine by a player"""

    def __init__(self, game_engine: Game, color: FigureColor) -> None:
        self.game_engine = game_engine
        self.color: FigureColor = color

        self.on_win_callback = None
        self.on_lose_callback = None

        self.on_win_callback = None
        self.on_lose_callback = None
        self.on_stalemate_callback = None

    def get_enemy_figures(self):
        enemy_color = invert_color(self.color)
        return self.game_engine.get_figures_by_color(enemy_color)

    def get_my_figures(self):
        return self.game_engine.get_figures_by_color(self.color)

    def get_available_cells(self, pos_from):
        cell = self.get_board_cell(pos_from)
        return self.game_engine.get_figure_available_cells(cell)

    @abstractmethod
    def do_step(self, from_pos, to_pos):
        pass

    def on_win(self):
        if self.on_win_callback:
            self.on_win_callback()

    def set_on_win_callback(self, callback):
        self.on_win_callback = callback

    def on_lose(self):
        if self.on_lose_callback:
            self.on_lose_callback()

    def set_on_lose_callback(self, callback):
        self.on_lose_callback = callback

    def on_stalemate(self):
        if self.on_stalemate_callback:
            self.on_stalemate_callback()

    def set_on_stalemate_callback(self, callback):
        self.on_stalemate_callback = callback

    def get_current_player(self):
        return self.game_engine.get_current_player()

    def get_board_cell(self, pos):
        return self.game_engine.board.get_cell(pos)
