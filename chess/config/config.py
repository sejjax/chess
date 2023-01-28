import argparse
from dataclasses import dataclass

from chess.lib.singleton import singleton


@singleton
@dataclass
class Config:
    debug: bool = False


def configure():
    parser = argparse.ArgumentParser(
        prog='Chess',
        description='Tui chess game'
    )
    parser.add_argument('--debug', action='store_const', const=True, default=False)

    args = parser.parse_args()

    debug_mode = args.debug

    config = Config(
        debug=debug_mode
    )
    return config


CONFIG = configure()
