from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto

from .tiles import Tile
from .renderers.renderer import Shapes, Colors

import logging

log = logging.getLogger(__package__)


class SnakeDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOPPED = auto()


@dataclass
class SnakeTile(Tile):
    shape: Shapes = Shapes.SQUARE
    color: Colors = Colors.BLACK


@dataclass
class Snake:
    initial_x: int
    initial_y: int

    speed: float
    growth_rate: int

    direction: SnakeDirection = SnakeDirection.STOPPED
    segments: List[Tile] = field(default_factory=list)

    def __post_init__(self):
        if not self.segments:
            self.segments.append(SnakeTile(x=self.initial_x, y=self.initial_y))

        self.movement_deltas = {
            SnakeDirection.UP: (0, -1),
            SnakeDirection.DOWN: (0, 1),
            SnakeDirection.LEFT: (-1, 0),
            SnakeDirection.RIGHT: (1, 0),
            SnakeDirection.STOPPED: (0, 0),
        }

    @property
    def x(self):
        return self.segments[0].x

    @property
    def y(self):
        return self.segments[0].y

    def __move(self):

        log.debug(
            f"Moving snake, speed: {self.speed}, direction: {self.direction}")

        for _ in range(self.speed):
            head: Tile = self.segments[0]

            x_delta, y_delta = self.movement_deltas[self.direction]

            new_head = SnakeTile(x=(head.x + x_delta), y=(head.y + y_delta))

            self.segments.insert(0, new_head)

            # Removing the tail
            self.segments.pop()

        log.debug(f"Snakes coordinates: {(self.x, self.y)}")

    def update(self):
        log.debug("Updating the snake")
        self.__move()

    def draw(self):
        for segment in self.segments:
            segment.draw()

    def grow(self):
        pass
