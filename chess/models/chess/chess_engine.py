# Core chess rules implementation
from abc import abstractmethod, ABC
from typing import Type

from chess.lib.vec import vec
from chess.models.chess.board import Board, Cell
from chess.models.chess.chess_game import ChessGame
from chess.models.chess.constants import LEFT_BORDER, TOP_BORDER, RIGHT_BORDER, BOTTOM_BORDER
from chess.models.chess.figures import FigureColor, Pawn, Rook, Bishop, Quin, Knight, King, Figure
from chess.models.chess.games import Game
from chess.models.chess.utils import get_side_by_color
from chess.utils.utils import invert_color, is_board_belong, cells_to_positions, positions_to_cells, is_empty_pos, \
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


def knights_available_cells(board: Board, pos_from: vec) -> list[Cell]:
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


class AbstractChessEngine(ChessGame, ABC):
    @abstractmethod
    def get_figures(self, color: FigureColor):
        pass


class ChessEngine(AbstractChessEngine):
    board: Board

    def __init__(self, game: Game):
        self.game_state = game.game_state
        self.board = game.game_state.board
        self.game_mode = game.game_mode

        white_figures, black_figures = self.board.get_figures()
        self.white_figures, self.black_figures = white_figures, black_figures

    def _get_king_cells(self):
        king_cells = []
        for row in self.board.board:
            for cell in row:
                if cell.content and type(cell.content) == King:
                    king_cells.append(cell)

        return king_cells

    def _get_figure(self, pos):
        return self.board.get_cell(pos).content

    def _get_king_cell_by_color(self, color):
        cells = self._get_figures_cells_by_color_and_kind(color, King)
        return cells[0]

    def _castle_king(self, king_pos, rook_pos):
        new_king_pos = king_pos.copy()
        new_rook_pos = rook_pos.copy()
        if king_pos.x > rook_pos.x:
            new_king_pos.x = 1
            new_rook_pos.x = 2
        else:
            new_king_pos.x = 6
            new_rook_pos.x = 5
        self._move_figure(king_pos, new_king_pos)
        self._move_figure(rook_pos, new_rook_pos)

    def _is_able_to_castling(self, king_or_rook):
        return not self._was_figure_moved(king_or_rook)

    def _get_figures_cells_by_color(self, color):
        cells = []
        for row in self.board.board:
            for i in row:
                figure = i.content
                if figure and figure.color == color:
                    cells.append(i)
        return cells

    def _get_figures_cells_by_color_and_kind(self, color, kind):
        cells = self._get_figures_cells_by_color(color)
        return filterlist(lambda i: type(i.content) == kind, cells)

    def _get_available_to_castling_rooks_cells(self):
        color = self.game_state.current_step_player
        king_cell = self._get_king_cell_by_color(color)
        if not self._is_able_to_castling(king_cell.content):
            return []
        king_pos = self.board.get_cell_position(king_cell)

        rooks_cells = self._get_figures_cells_by_color_and_kind(color, Rook)
        rooks_cells = filterlist(lambda i: self._is_able_to_castling(i.content), rooks_cells)
        rooks_cells = filterlist(lambda i: is_figures_between_row_cells(
            self.board,
            king_pos,
            self.board.get_cell_position(i)
        ), rooks_cells)
        return rooks_cells

    def _get_figure_available_cells(self, cell: Cell):
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
            is_on_started_pos = not self._was_figure_moved(figure)
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
            available_cells = knights_available_cells(self.board, cell_pos)
        elif figure_type == King:
            current_color = figure.color

            enemy_color = invert_color(current_color)
            enemy_king_cell = filterlist(lambda i: i.content.color == enemy_color, self._get_king_cells())
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
            available_cells += self._get_available_to_castling_rooks_cells()

        available_cells = cells_to_positions(self.board, available_cells)
        return available_cells

    def _get_figures_by_color(self, color: FigureColor):
        return self.white_figures if color == FigureColor.WHITE else self.black_figures

    def _get_enemy_color(self):
        return invert_color(self.game_state.current_step_player)

    def _is_king_in_dangerous(self):
        king_cell = self._get_king_cell_by_color(self.game_state.current_step_player)
        enemy_color = self._get_enemy_color()
        enemy_figures_cells = self._get_figures_cells_by_color(enemy_color)
        attacking_cells = []
        for cell in enemy_figures_cells:
            attacking_cells += self._get_figure_available_cells(cell)
        return king_cell in attacking_cells

    def _turn_figure(self, pos, turn_to_cls: Type[Figure]):
        cell = self.board.get_cell(tuple(pos))
        cell.content = turn_to_cls(cell.content.color)
        return cell.content

    def _move_figure(self, pos_from, pos_to):
        figure = self.board.get_cell(pos_from).content
        if figure is not None:
            self.game_state.was_figure_moved[figure] = True
        self.board.move_figure(pos_from, pos_to)

    def _was_figure_moved(self, figure):
        return self.game_state.was_figure_moved[figure]

    def _pawn_available_transform_cells(self, from_pos, to_pos):
        cell = self.board.get_cell(from_pos)
        figure = cell.content
        if figure is None or type(figure) != Pawn:
            return None

        color = figure.color
        available_cell_positions = self._get_figure_available_cells(cell)

        cells = []
        for pos in available_cell_positions:
            if to_pos.y == get_side_by_color(invert_color(color)):
                cell = self.board.get_cell(pos)
                cells.append(cell)
        return cells

    def will_pawn_transform(self, from_pos, to_pos):
        res = self._pawn_available_transform_cells(from_pos, to_pos)

        if res is None:
            return False
        return len(res) > 0

    def _process_any_figure_step(self, from_pos, to_pos):
        self._move_figure(tuple(from_pos), tuple(to_pos))
        return True

    def _process_pawn_step(self, from_pos, to_pos, transform_to):
        check = self.will_pawn_transform(from_pos, to_pos)
        if not check:
            return self._process_any_figure_step(from_pos, to_pos)

        figure = self.board.get_cell(from_pos).content
        enemy_border = BOTTOM_BORDER if figure.color == FigureColor.BLACK else TOP_BORDER
        if type(figure) != Pawn:
            return False
        if to_pos.y != enemy_border:
            return False

        prev_cell = self.board.get_cell(from_pos)
        prev_cell.clear()
        new_cell = self.board.get_cell(to_pos)
        new_cell.content = transform_to(figure.color)
        return True

    def _process_king_step(self, from_pos, to_pos):
        figure = self._get_figure(to_pos)

        if type(figure) == Rook:
            self._castle_king(from_pos, to_pos)
            return True
        return self._process_any_figure_step(from_pos, to_pos)

    def _change_current_step_player(self):
        self.game_state.current_step_player = invert_color(self.game_state.current_step_player)

    def get_available_cells(self, pos: vec) -> list[vec]:
        cell = self.board.get_cell(tuple(pos))
        return self._get_figure_available_cells(cell)

    def do_peace(self, from_pos: vec, to_pos: vec, figure: Type[Figure] | None = None):
        # FIXME move to game engine
        # The Order and Hierarcy of functions calling
        # process_step -> | is_allowed_step | -> _process_any_figure_step -> game_engine.move_figure
        #                                               or
        #                                   | -> _process_pawn_step  | -> step_with_pawn_transform
        #                                                           | -> _process_any_figure_step
        #                                               or
        #                                   | -> _process_king_step       -> game_engine.castle_king

        if not self._is_allowed_step(from_pos, to_pos):
            return False

        moved_figure = self.board.get_cell(tuple(from_pos)).content

        moved_figure_type = type(moved_figure)

        if moved_figure_type == Pawn:
            res = self._process_pawn_step(from_pos, to_pos, figure)
        elif moved_figure_type == King:
            res = self._process_king_step(from_pos, to_pos)
        else:
            res = self._process_any_figure_step(from_pos, to_pos)
        if not res:
            return False

        if self.game_mode.step_by_step_play:
            self._change_current_step_player()

    def get_figures(self, color: FigureColor):
        pass

    def _is_allowed_step(self, from_pos, to_pos):
        # FIXME move to game engine
        from_cell = self.board.get_cell(from_pos)
        moved_figure = from_cell.content

        if moved_figure is None:
            return False
        step_by_step_check = moved_figure.color == self.game_state.current_step_player and self.game_mode.step_by_step_play
        if step_by_step_check:
            return False

        available_cells = self._get_figure_available_cells(from_cell)
        search = list(filter(lambda _cell: to_pos == _cell, available_cells))
        if len(search) == 0:
            return False
        return True
