from dataclasses import dataclass
from .renderers.renderer import Shapes, Colors


@dataclass
class Tile:
    x: int
    y: int
    shape: Shapes = Shapes.SQUARE
    color: Colors = None
