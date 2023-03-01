from typing import Type

import npyscreen

from chess.views.lib.view import ScreenFormBaseNew


def create_button(callback, *args):
    class Button(npyscreen.ButtonPress):
        def whenPressed(self):
            callback(*args)

    return Button


def make_button(form: ScreenFormBaseNew, name: str, callback):
    button = create_button(callback)
    return form.add(button, name=name)


def navigate_to_button(form: ScreenFormBaseNew, name: str, view_cls: Type[ScreenFormBaseNew]):
    def callback():
        _navigate_to(form, view_cls)

    return make_button(form, name, callback)


def _navigate_to(form: ScreenFormBaseNew, view_cls: Type[ScreenFormBaseNew]):
    form.parent.navigator.navigate_to(view_cls)


def get_view_app(form) -> npyscreen.NPSAppManaged:
    return form.parentApp


def exit_from_view(form: ScreenFormBaseNew):
    form.parent.navigator.view_exit()


def get_pad(self):
    return self.parent.curses_pad
