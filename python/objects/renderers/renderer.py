from enum import Enum, auto
from dataclasses import dataclass


class Colors(Enum):
    BLACK = auto()
    WHITE = auto()
    BLUE = auto()
    RED = auto()


class Shapes(Enum):
    CIRCLE = auto()
    SQUARE = auto()


@dataclass
class Renderer:
    window_width: int
    window_height: int

    window_bgcolor: Colors = Colors.WHITE

    def add_shape_to_frame(self, x: int, y: int,
                           shape_width: int,
                           shape_height: int,
                           shape: Shapes = Shapes.SQUARE,
                           shape_color: Colors = Colors.BLACK):
        pass

    def reset_frame(self):
        pass

    def draw_frame(self):
        pass
