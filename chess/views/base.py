from abc import ABC


class BaseView(ABC):
    event_bus: AbstractEventBus
