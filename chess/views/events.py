from dataclasses import dataclass

from chess.lib.vec import vec


class Event:
    pass


@dataclass
class MoveFigureEvent(Event):
    from_pos: vec
    to_pos: vec
