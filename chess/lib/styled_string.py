# Styled string is the object which contain the string and console styling attributes: weight, blinking, underline ...

import curses

BOLD = 'bold'
DIM = 'dim'
BLINK = 'blink'
UNDERLINE = 'underline'
INVISIBLE = 'invisible'
REVERSE = 'reverse'
HORIZONTAL = 'horizontal'
LEFT = 'left'
LOW = 'low'
TOP = 'top'
VERTICAL = 'vertical'
STANDOUT = 'standout'
PROTECT = 'protect'
NORMAL = 'normal'
ALTCHARSET = 'altcharset'
ITALIC = 'italic'
COLOR = 'color'


class StyledChunk:
    attr_list: dict

    def __init__(self, text) -> None:
        self.text = text

        self.bold = False
        self.dim = False
        self.blink = False
        self.underline = False
        self.italic = False
        self.invisible = False
        self.reverse = False
        self.horizontal = False
        self.left = False
        self.low = False
        self.top = False
        self.vertical = False
        self.standout = False
        self.protect = False
        self.normal = False
        self.altcharset = False
        self.color = None

    def get_attr_list(self):
        return {
            BOLD: self.bold,
            DIM: self.dim,
            BLINK: self.blink,
            UNDERLINE: self.underline,
            ITALIC: self.italic,
            INVISIBLE: self.invisible,
            REVERSE: self.reverse,
            HORIZONTAL: self.horizontal,
            LEFT: self.left,
            LOW: self.low,
            TOP: self.top,
            VERTICAL: self.vertical,
            STANDOUT: self.standout,
            PROTECT: self.protect,
            NORMAL: self.normal,
            ALTCHARSET: self.altcharset,
            COLOR: self.color
        }

    def __str__(self) -> str:
        return f'{self.text}'

    def __repr__(self) -> str:
        return f'"{str(self)}"'

    def __add__(self, val):
        return StyledString(val, chunks=[self])

    def __iadd__(self, val):
        return StyledString(val, chunks=[self])


def styled(text, **kargs):
    if type(text) == str:
        text = StyledString(text)
    for k, v in kargs.items():
        for chunk in text.chunks:
            setattr(chunk, k, v)
    return text


def bold(text):
    return styled(text, bold=True)


def dim(text):
    return styled(text, dim=True)


def blink(text):
    return styled(text, blink=True)


def underline(text):
    return styled(text, underline=True)


def reverse(text):
    return styled(text, reverse=True)


def altcharset(text):
    return styled(text, altcharset=True)


def color(text, color):
    return styled(text, color=color)


def normal(text):
    return styled(text,
                  bold=False,
                  dim=False,
                  blink=False,
                  underline=False,
                  italic=False,
                  invisible=False,
                  reverse=False,
                  horizontal=False,
                  left=False,
                  low=False,
                  top=False,
                  vertical=False,
                  standout=False,
                  protect=False,
                  normal=False,
                  altcharset=False,
                  color=None
                  )


class StyledString:
    def __init__(self, text='') -> None:
        self.chunks = []
        if type(text) == str:
            if len(text) != 0:
                self.chunks.append(StyledChunk(text))
        elif type(text) == StyledChunk:
            self.chunks.append(text)
        elif type(text) == StyledString:
            self.chunks = text.chunks.copy()

    def __add__(self, val):
        a = self
        b = StyledString(val)
        rchunks = a.chunks + b.chunks
        b.chunks = rchunks
        return b

    def __str__(self) -> str:
        return "".join(map(lambda chunk: chunk.text, self.chunks))

    def __repr__(self):
        return f'"{str(self)}"'


ATTR_MAP = {
    DIM: curses.A_DIM,
    BOLD: curses.A_BOLD,
    BLINK: curses.A_BLINK,
    UNDERLINE: curses.A_UNDERLINE,
    REVERSE: curses.A_REVERSE,
    HORIZONTAL: curses.A_HORIZONTAL,
    LEFT: curses.A_LEFT,
    LOW: curses.A_LOW,
    TOP: curses.A_TOP,
    VERTICAL: curses.A_VERTICAL,
    STANDOUT: curses.A_STANDOUT,
    PROTECT: curses.A_PROTECT,
    NORMAL: curses.A_NORMAL,
    ALTCHARSET: curses.A_ALTCHARSET,
}


def addstr(scr, text, relx=0, rely=0):
    """Add styled string to screen
        text: str
    """
    text = styled(text)
    cursor_pos = 0
    for chunk in text.chunks:
        attributes = 0
        for attr_name, attr_value in chunk.get_attr_list().items():
            if attr_name == COLOR and attr_value:
                attributes |= attr_value
            elif attr_value:
                attributes |= ATTR_MAP[attr_name]

        line_shift = 0
        row = ''
        for idx, i in enumerate(str(chunk)):
            row = row + i if i != '\n' else row
            if i == '\n' or idx == len(str(chunk)) - 1:
                scr.addstr(rely + line_shift, relx + cursor_pos, row, attributes)
                row = ''
                line_shift += 1
                continue

        cursor_pos += len(chunk.text)