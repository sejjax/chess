import random
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..lib.view import ScreenFormBaseNew


def generate_view_id(view: Type['ScreenFormBaseNew']):
    ID_SIZE = 8
    name = view.__class__.__name__
    _id = hex(int.from_bytes(random.randbytes(ID_SIZE), byteorder='little'))
    return f'{name}_{_id}'
