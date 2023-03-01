from abc import ABC
from dataclasses import dataclass
from typing import Type

import npyscreen

from chess.controllers.base import BaseController
from chess.lib.event_bus import EventBus
from chess.views.lib.navigator import ViewNavigator
from chess.views.utils.generator import generate_view_id


class BaseView(ABC):
    controller: BaseController
    event_bus: EventBus

    def __init__(self, controller: BaseController, event_bus: EventBus):
        self.controller = controller
        self.event_bus = event_bus


class ScreenBaseView(BaseView):
    """Base view class with supporting lifecycle callbacks"""
    parent: 'ScreenAppView'
    view_id: str

    def __init__(self, view_id: str, parent: 'ScreenAppView', controller: BaseController, event_bus: EventBus):
        super().__init__(controller, event_bus)
        self.parent = parent
        self.view_id = view_id

    def on_enter(self):
        pass

    def on_exit(self):
        pass


@dataclass
class ViewIDView:
    view: ScreenBaseView
    view_id: str


class ScreenFormBaseNew(ScreenBaseView, npyscreen.FormBaseNew):

    def __init__(self, view_id: str, parent: 'ScreenAppView', controller, event_bus, *args, **kwargs):
        ScreenBaseView.__init__(self, view_id, parent, controller, event_bus)
        npyscreen.FormBaseNew.__init__(self, *args, **kwargs)


class ScreenActionForm(ScreenFormBaseNew, npyscreen.ActionForm):
    def __init__(self, view_id, parent, controller, event_bus, *args, **kwargs):
        ScreenBaseView.__init__(self, view_id, parent, controller, event_bus)
        npyscreen.ActionForm.__init__(self, *args, **kwargs)
        self.parent = parent


class ScreenActionFormMinimal(ScreenFormBaseNew, npyscreen.ActionFormMinimal):
    def __init__(self, view_id, parent, controller, event_bus, *args, **kwargs):
        ScreenBaseView.__init__(self, view_id, parent, controller, event_bus)
        npyscreen.ActionFormMinimal.__init__(self, *args, **kwargs)
        self.parent = parent


class ScreenAppView(BaseView):
    npyscreen_app: npyscreen.NPSAppManaged
    navigator: ViewNavigator
    views: list[ViewIDView]

    def __init__(self, controller, event_bus):
        super().__init__(controller, event_bus)
        self.views = []
        self.navigator = ViewNavigator(self)
        self.npyscreen_app = npyscreen.NPSAppManaged()
        self.npyscreen_app.onStart = self.on_start

    def add_view(self, view_cls: Type[ScreenFormBaseNew], view_id=None, name: str = None, color: str = None):
        view = self.get_view(view_cls)
        if view is not None:
            raise ValueError('You can add only one view class to the app.')
        if view_id is None:
            view_id = generate_view_id(view_cls)
        if len(self.views) == 0:
            self._set_main_view(view_id)
        self.npyscreen_app.addForm(
            view_id,
            view_cls,
            # view initialization requirements
            controller=self.controller,
            event_bus=self.event_bus,
            view_id=view_id,
            parent=self,
            name=name,
            color=color,

        )
        view = self.npyscreen_app.getForm(view_id)
        self.views.append(ViewIDView(view, view_id))
        self.npyscreen_app.onStart = self.on_start

    def _set_main_view(self, view_id):
        self.npyscreen_app.NEXT_ACTIVE_FORM = view_id

    def get_view(self, view_cls: Type[ScreenFormBaseNew] | str) -> ViewIDView:
        if type(view_cls) == str:
            test = (lambda view: view.view.__class__.__name__)
        else:
            test = lambda view: view.view.__class__

        for view in self.views:
            if test(view) == view_cls:
                return view

    def on_start(self):
        pass

    def run(self):
        self.npyscreen_app.run()

    def exit(self):
        self.navigator.view_exit()
