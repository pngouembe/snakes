#! python3
"""Snake game's python version"""

import logging
import math
import sys
from dataclasses import dataclass
from enum import Enum, auto
from queue import Queue
from time import time
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
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("SnakeGame")


class GameState(Enum):
    GAME_INIT = auto()
    GAME_RUNNING = auto()
    GAME_PAUSED = auto()
    GAME_STOPPED = auto()


class GameEvent(Enum):
    SPEED_UP = auto()
    GAME_OVER = auto()
    NO_EVENT = auto()


@dataclass
class SnakeGame:
    grid: Grid
    snake: Snake
    food_facory: FoodFactory
    input_handler: InputHandler
    snake_speed: float = 1  # in moves/sec
    snake_acceleration_factor: float = 0.7

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

        self.inputs = Queue(maxsize=2)
        self.speed_level = 0

    def __speed_up(self):
        self.speed_level += 1
        self.snake_speed += self.snake_acceleration_factor * math.log10(1 + self.speed_level)

    def __draw(self):
        self.grid.draw()

    def __game_over(self):
        log.info("Game over")
        sys.exit()

    def __update(self) -> GameEvent:
        ret = GameEvent.NO_EVENT
        snake_prev_state = [tile for tile in self.snake.segments]

        if not self.inputs.empty():
            self.snake.direction = self.key_to_direction_map[self.inputs.get_nowait()]

        snake_event: SnakeEvent = self.snake.update(
            food_x=self.food.x, food_y=self.food.y)

        if snake_event == SnakeEvent.SELF_BITE:
            return GameEvent.GAME_OVER

        if self.snake.x >= self.grid.col_count or self.snake.x < 0:
            return GameEvent.GAME_OVER

        if self.snake.y >= self.grid.row_count or self.snake.y < 0:
            return GameEvent.GAME_OVER


        to_add = [
            tile for tile in self.snake.segments if tile not in snake_prev_state]
        to_remove = [
            tile for tile in snake_prev_state if tile not in self.snake.segments]

        if snake_event == SnakeEvent.ATE_FOOD:
            self.food = self.food_facory.spawn_food(self.grid.empty_positions)
            to_add.append(self.food)
            log.info(f"Spawning new food at: {(self.food.x, self.food.y)}")
            ret = GameEvent.SPEED_UP

        for tile in to_add:
            self.grid.add_tile(tile=tile)
        for tile in to_remove:
            self.grid.remove_tile(x=tile.x, y=tile.y)

        return ret

    def __get_inputs(self):
        inputs: List[Inputs] = self.input_handler.get_latest_inputs()
        if Inputs.QUIT in inputs:
            sys.exit()
        # TODO: Provide input queue
        for input in inputs:
            if not self.inputs.full():
                self.inputs.put_nowait(input)
                log.debug(f"Added {input} to input queue")

    def __game_loop(self):
        game_loop_counter = 0
        start_time = time()
        self.__draw()
        while self.game_state != GameState.GAME_STOPPED:
            game_loop_counter += 1

            self.__get_inputs()
            if time() - start_time >= (1 / self.snake_speed):
                game_event: GameEvent = self.__update()
                if game_event == GameEvent.GAME_OVER:
                    self.__game_over()
                if game_event == GameEvent.SPEED_UP:
                    self.__speed_up()
                    log.debug(
                        f"Increasing speed to {self.snake_speed} moves/seconds")

                self.__draw()
                start_time = time()

    def start(self):
        self.game_state = GameState.GAME_RUNNING
        self.snake.direction = SnakeDirection.STOPPED
        self.__game_loop()

    def stop(self):
        pass


def main():
    nb_col = 21
    nb_row = 21
    tile_size = 30

    renderer_config = {
        "window_width": nb_col * tile_size,
        "window_height": nb_row * tile_size,
        "window_bgcolor": Colors.WHITE,
        "type": RendererType.PYGAME
    }

    renderer: Renderer = RendererFactory.get_renderer(**renderer_config)
    grid = Grid(row_count=nb_row, col_count=nb_col, renderer=renderer)
    snake = Snake(initial_x=10, initial_y=10)
    input_handler = PygameKeyboardHandler()
    food_factory = FoodFactory()

    game_obj = SnakeGame(grid=grid, snake=snake,
                         food_facory=food_factory, input_handler=input_handler, snake_speed=2)

    game_obj.start()


if __name__ == "__main__":
    main()
