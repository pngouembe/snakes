from dataclasses import dataclass
import turtle

from .snake import Snake
from .food import FoodFactory


@dataclass
class Map:
    width: int
    height: int

    snake: Snake
    food_factory: FoodFactory

    def update(self):
        pass

    def draw(self):
        pass
