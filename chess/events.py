from dataclasses import dataclass

from blinker import signal

from chess.lib.vec import vec

# Event bus for views
VIEW_EVENT_BUS_NAME = 'VIEW_EVENT_BUS'
ViewEventBus = signal(VIEW_EVENT_BUS_NAME)

FIGURE_WAS_CHOSE = 'FIGURE_WAS_CHOSE'
OPEN_FIGURE_CHOOSE_POPUP = 'OPEN_FIGURE_CHOOSE_POPUP'
CLOSE_FIGURE_CHOOSE_POPUP = 'CLOSE_FIGURE_CHOOSE_POPUP'
