
from typing import Type, Callable


from blinker import signal

class Event:
    pass


class DataEvent(Event):
    data: any

    def __init__(self, data=None):
        self.data = data

class EventBus:
    def __init__(self, name: str):
        self.bus = signal(name)

    def emit(self, event):
        self.bus.send(event)

    def on(self, *event_types: Type['Event']):
        def wrap(func: Callable):
            def wrapper(event: Event):
                if type(event) in event_types:
                    func(event)

            self.bus.connect(wrapper)
            return wrapper

        return wrap

    def disconnect(self, receiver: Callable):
        self.bus.disconnect(receiver)



