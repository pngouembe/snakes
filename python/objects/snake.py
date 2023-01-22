import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from .renderers.renderer import Colors, Shapes
from .tiles import Tile

log = logging.getLogger(__package__)


class SnakeDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOPPED = auto()


class SnakeEvent(Enum):
    SELF_BITE = auto()
    ATE_FOOD = auto()
    NO_EVENT = auto()


@dataclass
class SnakeTile(Tile):
    shape: Shapes = Shapes.SQUARE
    color: Colors = Colors.BLACK


@dataclass
class Snake:
    initial_x: int
    initial_y: int

    segments: List[Tile] = field(default_factory=list)

    def __post_init__(self):
        self.__direction: SnakeDirection = SnakeDirection.STOPPED
        if not self.segments:
            self.segments.append(SnakeTile(x=self.initial_x, y=self.initial_y))

        self.movement_deltas = {
            SnakeDirection.UP: (0, -1),
            SnakeDirection.DOWN: (0, 1),
            SnakeDirection.LEFT: (-1, 0),
            SnakeDirection.RIGHT: (1, 0),
            SnakeDirection.STOPPED: (0, 0),
        }

        self.length = 1

        self.forbiden_moves = {
            SnakeDirection.UP: SnakeDirection.DOWN,
            SnakeDirection.DOWN: SnakeDirection.UP,
            SnakeDirection.LEFT: SnakeDirection.RIGHT,
            SnakeDirection.RIGHT: SnakeDirection.LEFT,
            SnakeDirection.STOPPED: SnakeDirection.STOPPED
        }


    @property
    def x(self):
        return self.segments[0].x

    @property
    def y(self):
        return self.segments[0].y

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction: SnakeDirection):
        if self.forbiden_moves[self.direction] != direction:
            self.__direction = direction

    def __move(self, food_x: int, food_y: int) -> SnakeEvent:
        ret = SnakeEvent.NO_EVENT

        log.debug(
            f"Moving snake, direction: {self.direction}")

        food_touched = False

        head: Tile = self.segments[0]

        x_delta, y_delta = self.movement_deltas[self.direction]

        new_head = SnakeTile(x=(head.x + x_delta), y=(head.y + y_delta))

        if new_head.x == food_x and new_head.y == food_y:
            food_touched = True

        for x, y in [(tile.x, tile.y) for tile in self.segments]:
            if new_head.x == x and new_head.y == y:
                ret = SnakeEvent.SELF_BITE
                break

        self.segments.insert(0, new_head)

        if food_touched:
            self.length += 1
            ret = SnakeEvent.ATE_FOOD
            log.info(f"Snake ate food at {(new_head.x, new_head.y)}")
            # To grow, don't erase the last bit of tail
        else:
            # Removing the tail
            self.segments.pop()

        log.debug(f"Snakes coordinates: {(self.x, self.y)}, Snake lenght: {self.length}")
        return ret

    def update(self, food_x: int, food_y: int) -> SnakeEvent:
        log.debug("Updating the snake")
        if self.direction != SnakeDirection.STOPPED:
            return self.__move(food_x, food_y)
        else:
            return SnakeEvent.NO_EVENT
