import logging
from dataclasses import dataclass

import pygame

from .renderer import Colors, Renderer, Shapes

log = logging.getLogger(__package__)


@dataclass
class PygameRenderer(Renderer):
    def __post_init__(self):
        if not pygame.display.get_init():
            pygame.display.init()
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))

        self.shape_constructors = {
            Shapes.CIRCLE: self._draw_circle,
            Shapes.SQUARE: self._draw_square
        }

        self.color_map = {
            Colors.BLACK: "black",
            Colors.BLUE: "blue",
            Colors.RED: "red",
            Colors.WHITE: "white"
        }

        self.window.fill(self.color_map[self.window_bgcolor])
        self.draw_frame()

    def _draw_circle(self, x: int, y: int,
                     shape_width: int,
                     shape_height: int,
                     shape_color: Colors = Colors.BLACK):
        log.debug(f"Drawing circle at: {(x, y)} in {shape_color}")
        rect = pygame.Rect(x, y, shape_width, shape_height)
        pygame.draw.ellipse(self.window, self.color_map[shape_color], rect)


    def _draw_square(self, x: int, y: int,
                     shape_width: int,
                     shape_height: int,
                     shape_color: Colors = Colors.BLACK):
        log.debug(f"Drawing square at: {(x, y)} in {shape_color}")
        rect = pygame.Rect(x, y, shape_width, shape_height)
        pygame.draw.rect(self.window, self.color_map[shape_color], rect)

    def add_shape_to_frame(self, x: int, y: int,
                           shape_width: int,
                           shape_height: int,
                           shape: Shapes = Shapes.SQUARE,
                           shape_color: Colors = Colors.BLACK):
        if shape_color is None:
            shape_color = self.window_bgcolor
        return self.shape_constructors[shape](x, y, shape_width, shape_height, shape_color)

    def draw_frame(self):
        pygame.display.flip()
