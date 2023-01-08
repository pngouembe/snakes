#! python3
"""Snake game's python version"""

from dataclasses import dataclass
from enum import Enum, auto

from objects.renderers.rendererfactory import RendererFactory, RendererType
from objects.renderers.renderer import Renderer, Colors, Shapes

from objects.grid import Grid
from objects.snake import Snake, SnakeDirection
from objects.food import FoodFactory

from time import sleep

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("SnakeGame")


class GameState(Enum):
    GAME_INIT = auto()
    GAME_RUNNING = auto()
    GAME_PAUSED = auto()
    GAME_STOPPED = auto()


@dataclass
class SnakeGame:
    grid: Grid
    snake: Snake
    food_facory: FoodFactory
    game_loop_frequency: float = None

    def __post_init__(self):
        self.game_state = GameState.GAME_INIT
        for tile in self.snake.segments:
            self.grid.add_tile(tile=tile)

    def __draw(self):
        self.grid.draw()

    def __update(self):
        snake_prev_state = [tile for tile in self.snake.segments]
        log.debug(snake_prev_state)
        self.snake.update()
        to_add = [
            tile for tile in self.snake.segments if tile not in snake_prev_state]
        to_remove = [
            tile for tile in snake_prev_state if tile not in self.snake.segments]

        log.debug(self.snake.segments)

        for tile in to_add:
            self.grid.add_tile(tile=tile)
        for tile in to_remove:
            self.grid.remove_tile(x=tile.x, y=tile.y)

    def __get_inputs(self):
        pass

    def __game_loop(self):
        game_loop_counter = 0
        while self.game_state != GameState.GAME_STOPPED:
            game_loop_counter += 1
            log.debug(f"Launching the game loop number {game_loop_counter}")

            self.__get_inputs()
            self.__update()
            self.__draw()
            # TODO: Replace by real frequency logic
            if self.game_loop_frequency:
                sleep(1/self.game_loop_frequency)

    def start(self):
        self.game_state = GameState.GAME_RUNNING
        self.snake.direction = SnakeDirection.RIGHT
        self.__game_loop()

    def stop(self):
        pass


def main():
    renderer_config = {
        "window_width": 600,
        "window_height": 600,
        "window_bgcolor": Colors.WHITE,
        "type": RendererType.TURTLE
    }

    renderer: Renderer = RendererFactory.get_renderer(**renderer_config)
    grid = Grid(row_count=21, col_count=21, renderer=renderer)
    snake = Snake(initial_x=10, initial_y=10, speed=1, growth_rate=1)

    game_obj = SnakeGame(grid=grid, snake=snake,
                         food_facory=None, game_loop_frequency=1)

    game_obj.start()


if __name__ == "__main__":
    main()
