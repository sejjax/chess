from dataclasses import dataclass

from chess.lib.event_bus import Event
from chess.lib.vec import vec


@dataclass
class MoveFigureEvent(Event):
    from_pos: vec
    to_pos: vec
