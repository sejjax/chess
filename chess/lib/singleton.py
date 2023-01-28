from typing import TypeVar

T = TypeVar('T')


def singleton(class_: T):
    instances = {}

    def getinstance(*args, **kwargs) -> T:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
