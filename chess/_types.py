from abc import ABC, abstractmethod
from chess.models.chess.figure import FigureColor


class IChess(ABC):

    @abstractmethod
    def make_step(self, pos_from, pos_to):
        pass


class AbstractModel(ABC):
    pass


class AbstractController(ABC):
    @abstractmethod
    def __init__(self, model: AbstractModel) -> None:
        self.model = model


class AbstractView(ABC):
    @abstractmethod
    def __init__(self, controller: AbstractController) -> None:
        self.controller = controller

    @abstractmethod
    def run(self):
        pass


class Modular(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def build(self) -> 'AbstractModule':
        pass


class AbstractModule(Modular, ABC):
    @abstractmethod
    def __init__(self, model: AbstractModel, controller: AbstractController, view: AbstractView) -> None:
        self.view = view
        self.controller = controller
        self.model = model


class AbstractApp(Modular, ABC):
    @abstractmethod
    def __init__(self, modules: list[AbstractModule]) -> None:
        self.modules = modules


