from typing import Type
from .games.game import Game, GamePlayer
from .game_state import GameState
from .games.game_mode import GameMode
from .player import Player


class Party:
    players: list[Player]
    game: Game

    def __init__(self, game: Game, players=None) -> None:
        if players is None:
            players = []
        self.players = players
        self.game = game

    @staticmethod
    def new(GameClass: Type[Game], game_state: GameState, game_mode: GameMode, players=None):
        if players is None:
            players = []
        game = GameClass(game_state, game_mode)
        party = Party(game, players)
        return party
