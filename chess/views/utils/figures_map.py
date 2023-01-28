from typing import Type

from chess.models.chess.figure import FigureColor, Figure
from chess.views.constants import LETTERS_FIGURE_MAP


def figure_symbol_map(figure: Type[Figure]) -> str:
    return LETTERS_FIGURE_MAP[type(figure)]


def symbol_figure_map(figure_symbol) -> Type[Figure]:
    return LETTERS_FIGURE_MAP.inverse[figure_symbol]


def symbol_figure_color_map(figure_symbol: str) -> Figure:
    figure = symbol_figure_map(figure_symbol.upper())
    color = FigureColor.WHITE if figure_symbol.isupper() else FigureColor.BLACK
    return figure(color)
