from .party import Party
from .games.local_game import LocalGame
from multiprocessing.connection import Listener

from ...lib.singleton import singleton


class GameKinds:
    pass


class ChessModel:
    parties: list[Party]

    def get_all_parties(self):
        return self.parties

    def create_party(self, party):
        self.parties.append(party)
        return party

    def delete_party(self, party):
        parties = list(filter(lambda i: i == party, self.parties))
        if len(parties) == 0:
            return False
        del party
        return True


GAME_KINDS_CLASS_MAP = {

}


@singleton
class ChessService:
    party: Party
    chess_model: ChessModel

    def __init__(self, chess_model,
                 party) -> None:
        # ? Do I need to set party object as chess service attribute or I can pass via method arguments
        self.party = party
        self.chess_model = chess_model

    def do_step(self, from_pos, to_pos,
                player):
        # ? Does it right pass player object to change
        # game state via ChessService? Probably I need to create another object
        self.party.game.do_step(from_pos, to_pos)

    def new_game(game_kind: GameKinds, players=None):  # ? Do I need to pass game class or game kind enum
        if players is None:
            players = []
        if game_kind not in GAME_KINDS_CLASS_MAP:
            raise ValueError('Unknown kind of game: ' + repr(game_kind))
        game = GAME_KINDS_CLASS_MAP[game_kind]
        return Party.new(game, players)

    def add_player(self, player):
        # Max count of players in the party is 2 
        if len(self.party.players) > 1:
            return False

        self.party.players.append(player)
        return True

    def start_game(self):
        self.party.game.start()

    def finish_game(self):
        self.party.game.finish()
