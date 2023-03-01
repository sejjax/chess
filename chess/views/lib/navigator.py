from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from chess.views.lib.view import ScreenAppView, ScreenFormBaseNew


class ViewNavigator:
    app: 'ScreenAppView'

    def __init__(self, app: 'ScreenAppView'):
        self.app = app

    def _navigate_to(self, view_id: Type['ScreenFormBaseNew'] | None | str):
        if view_id is not None:
            next_view = self.app.get_view(view_id)
        else:
            next_view = None

        current_view = self.get_current_view()
        current_view.on_exit()

        view = next_view if next_view is None else next_view.view_id
        self.app.npyscreen_app.switchForm(view)

        if next_view is not None:
            next_view.view.on_enter()

    def get_current_view(self):
        form = self.app.npyscreen_app.ACTIVE_FORM_NAME
        return self.app.npyscreen_app.getForm(form)

    def navigate_to(self, view_cls: Type['ScreenFormBaseNew'] | str):
        self._navigate_to(view_cls)

    def view_exit(self):
        self._navigate_to(None)
