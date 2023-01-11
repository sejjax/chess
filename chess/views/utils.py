import npyscreen

from chess.models.chess.figure import FigureType, FigureColor
from chess.views.constants import LETTERS_FIGURE_MAP, SYMBOL_FIGURE_MAP, CURRENT_MAP


def create_button(callback, *args):
    class Button(npyscreen.ButtonPress):
        def whenPressed(self):
            callback(*args)

    return Button


def make_button(form, name, callback):
    button = create_button(callback)
    return form.add(button, name=name)


def navigate_to_button(form, name, page_name):
    def callback():
        navigate_to(form, page_name)

    return make_button(form, name, callback)


def navigate_to(form, page_name):
    form.parentApp.switchForm(page_name)


def exit_from_view(form):
    navigate_to(form, None)


def symbol_figure_map(figure_type: FigureType, figure_color: FigureColor):
    if CURRENT_MAP == LETTERS_FIGURE_MAP:
        return LETTERS_FIGURE_MAP[figure_type]
    return SYMBOL_FIGURE_MAP[(figure_type, figure_color)]


def get_pad(self):
    return self.parent.curses_pad
