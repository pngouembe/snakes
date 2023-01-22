from dataclasses import dataclass
from random import randrange
from typing import List, Tuple

from .renderers.renderer import Colors, Shapes
from .tiles import Tile


@dataclass
class FoodTile(Tile):
    shape: Shapes = Shapes.CIRCLE
    color: Colors = Colors.RED


@dataclass
class FoodFactory:
    def spawn_food(self, available_spots: List[Tuple[int, int]]) -> Tile:
        x, y = available_spots[randrange(len(available_spots))]
        return FoodTile(x=x, y=y)
