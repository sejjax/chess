from typing import Type, Callable

from blinker import signal


class Event:
    pass


class EventBus:
    def __init__(self, name: str):
        self.bus = signal(name)

    def emit(self, event: Event):
        self.bus.send(event=event)

    def on(self, *event_types: Type['Event']):
        def wrap(func):
            check = event_types is None or len(event_types) == 0

            def wrapper(sender, event: Event, **kwargs):
                if check or type(event) in event_types:
                    func(event, **kwargs)

            self.bus.connect(wrapper, weak=False)
            return wrapper

        return wrap

    def connect(self, func, event_types: list[Type[Event]] = None):
        check = event_types is None or len(event_types) == 0

        def wrapper(sender, event: Event, **kwargs):
            if check or type(event) in event_types:
                func(event, **kwargs)

        self.bus.connect(wrapper, weak=False)

    def disconnect(self, receiver: Callable):
        self.bus.disconnect(receiver)
