#! python3
"""Snake game's python version"""

import logging
import sys
from dataclasses import dataclass
from enum import Enum, auto
from time import sleep
from typing import List

from objects.food import FoodFactory
from objects.grid import Grid
from objects.inputs.input_handler import InputHandler, Inputs
from objects.inputs.pygame_keyboard_handler import PygameKeyboardHandler
from objects.renderers.renderer import Colors, Renderer
from objects.renderers.rendererfactory import RendererFactory, RendererType
from objects.snake import Snake, SnakeDirection, SnakeEvent
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
    input_handler: InputHandler
    game_loop_frequency: float = None

    def __post_init__(self):
        self.game_state = GameState.GAME_INIT
        for tile in self.snake.segments:
            self.grid.add_tile(tile=tile)

        self.food = self.food_facory.spawn_food(self.grid.empty_positions)
        self.grid.add_tile(self.food)

        self.key_to_direction_map = {
            Inputs.UP: SnakeDirection.UP,
            Inputs.RIGHT: SnakeDirection.RIGHT,
            Inputs.LEFT: SnakeDirection.LEFT,
            Inputs.DOWN: SnakeDirection.DOWN,
            Inputs.PAUSE: SnakeDirection.STOPPED,
            Inputs.QUIT: SnakeDirection.STOPPED
        }

    def __draw(self):
        self.grid.draw()

    def __game_over(self):
        log.info("Game over")
        sys.exit()

    def __update(self):
        snake_prev_state = [tile for tile in self.snake.segments]
        log.debug(snake_prev_state)
        snake_event: SnakeEvent = self.snake.update(
            food_x=self.food.x, food_y=self.food.y)

        if snake_event == SnakeEvent.SELF_BITE:
            return self.__game_over()

        to_add = [
            tile for tile in self.snake.segments if tile not in snake_prev_state]
        to_remove = [
            tile for tile in snake_prev_state if tile not in self.snake.segments]

        if snake_event == SnakeEvent.ATE_FOOD:
            self.food = self.food_facory.spawn_food(self.grid.empty_positions)
            to_add.append(self.food)
            log.info(f"Spawning new food at: {(self.food.x, self.food.y)}")

        for tile in to_add:
            self.grid.add_tile(tile=tile)
        for tile in to_remove:
            self.grid.remove_tile(x=tile.x, y=tile.y)

    def __get_inputs(self):
        inputs: List[Inputs] = self.input_handler.get_latest_inputs()
        for input in inputs:
            if input == Inputs.QUIT:
                sys.exit()
            self.snake.direction = self.key_to_direction_map[input]

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
        self.snake.direction = SnakeDirection.STOPPED
        self.__game_loop()

    def stop(self):
        pass


def main():
    renderer_config = {
        "window_width": 600,
        "window_height": 600,
        "window_bgcolor": Colors.WHITE,
        "type": RendererType.PYGAME
    }

    renderer: Renderer = RendererFactory.get_renderer(**renderer_config)
    grid = Grid(row_count=21, col_count=21, renderer=renderer)
    snake = Snake(initial_x=10, initial_y=10, speed=1, growth_rate=1)
    input_handler = PygameKeyboardHandler()
    food_factory = FoodFactory()

    game_obj = SnakeGame(grid=grid, snake=snake,
                         food_facory=food_factory, input_handler=input_handler, game_loop_frequency=2)

    game_obj.start()


if __name__ == "__main__":
    main()
