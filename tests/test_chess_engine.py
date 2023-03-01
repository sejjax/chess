import pytest

from chess.lib.vec import vec
from chess.models.chess.chess_engine import ChessEngine
from chess.models.chess.figures import FigureColor, Pawn
from chess.models.chess.games import ClassicGame, DebugGame


class TestChessEngine:

    def test_pawn_default_step(self, classic_game_res):
        from_ = vec(0, 1)
        to_ = vec(0, 3)
        engine = classic_game_res
        engine.do_peace(from_, to_)
        cell = engine.game_state.board.get_cell(tuple(to_))
        assert cell.content is not None
        assert cell.content.color == FigureColor.BLACK
        assert type(cell.content) == Pawn

    def test_long_step(self, classic_game_res):
        from_ = vec(1, 1)
        to_ = vec(1, 3)
        engine = classic_game_res
        engine.do_peace(from_, to_)
        cell = engine.game_state.board.get_cell(tuple(to_))
        assert cell.content is not None
        assert cell.content.color == FigureColor.BLACK
        assert type(cell.content) == Pawn

    def test_available_cells(self, classic_game_res):
        engine = classic_game_res
        from_ = vec(3, 1)
        cells = engine.get_available_cells(from_)
        CELLS = [vec(3, 2), vec(3, 3)]
        assert cells == CELLS

    def test_will_pawn_transform(self):
        pass

    def test_setup_on_game_end_callbacks(self):
        pass


@pytest.fixture(scope='function', autouse=True)
def debug_game_res():
    game_map = """
P
PPPPPPPP



PPPPPPPP
PPPPP
PPPPPPPP
    """
    game = DebugGame(game_map)
    engine = ChessEngine(game)
    return engine


@pytest.fixture(scope='function', autouse=True)
def classic_game_res():
    game = ClassicGame()
    engine = ChessEngine(game)
    return engine
