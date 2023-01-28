import npyscreen
from chess.views.constants import LETTERS_FIGURE_MAP
import bidict


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


def _navigate_to(form, page_name):
    form.parentApp.switchForm(page_name)


def navigate_to(form, form_name):
    current_form = form

    app = get_view_app(form)

    if hasattr(current_form, 'on_exit'):
        current_form.on_exit()

    if form_name is not None:
        next_form = app.getForm(form_name)

        if hasattr(next_form, 'on_enter'):
            next_form.on_enter()

    _navigate_to(form, form_name)


def get_view_app(form) -> npyscreen.NPSAppManaged:
    return form.parentApp


def exit_from_view(form):
    navigate_to(form, None)





def get_pad(self):
    return self.parent.curses_pad
