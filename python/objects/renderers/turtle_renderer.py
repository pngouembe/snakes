from dataclasses import dataclass
from .renderer import Renderer, Shapes, Colors

import turtle

TURTLE_COLORS_DICT = {
    Colors.WHITE: "white",
    Colors.BLACK: "black",
    Colors.BLUE: "blue",
    Colors.RED:  "red",
}


@dataclass
class TurtleRenderer(Renderer):
    def _draw_square(self, x_top_left: int, y_top_left: int, x_bot_right: int, y_bot_right: int):
        self.turtle.goto(x_top_left, y_top_left)
        print(f"turtle at {(x_top_left, y_top_left)}")

        self.turtle.setheading(0)
        self.turtle.pendown()

        x_delta = x_bot_right - x_top_left
        y_delta = y_bot_right - y_top_left

        for _ in range(2):
            self.turtle.forward(x_delta)
            self.turtle.left(90)
            self.turtle.forward(y_delta)
            self.turtle.left(90)

        self.turtle.penup()

    def _draw_circle(self, x_top_left: int, y_top_left: int, x_bot_right: int, y_bot_right: int):
        x = x_top_left + int((x_bot_right - x_top_left)/2)
        y = y_top_left
        self.turtle.goto(x, y)
        print(f"turtle at {(x, y)}")
        self.turtle.setheading(180)
        self.turtle.pendown()
        self.turtle.circle((x_bot_right - x_top_left)/2)
        self.turtle.penup()

    def __post_init__(self):
        self.window = turtle.Screen()
        self.window.title("Snake Game")
        self.window.bgcolor(TURTLE_COLORS_DICT[self.window_bgcolor])
        self.window.setup(width=self.window_width, height=self.window_height)
        self.window.tracer(0)

        self.turtle_shape_dict = {
            Shapes.CIRCLE: self._draw_circle,
            Shapes.SQUARE: self._draw_square,
        }

    def add_shape_to_frame(self, x: int, y: int, shape_width: int, shape_height: int, shape: Shapes = Shapes.CIRCLE, shape_color: Colors = Colors.BLACK):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.hideturtle()
        if shape_color == None:
            self.turtle.pencolor(TURTLE_COLORS_DICT[self.window_bgcolor])
        else:
            self.turtle.pencolor(TURTLE_COLORS_DICT[shape_color])
        self.turtle.fillcolor(self.turtle.pencolor())

        # Move (0,0) coordonates in the top left corner and invert the y axis
        x = x - int(self.window_width/2)
        y = int(self.window_height/2) - y

        print(f"shape color: {shape_color}")

        self.turtle.begin_fill()
        self.turtle_shape_dict[shape](x_top_left=x,
                                      y_top_left=y,
                                      x_bot_right=(x + shape_width),
                                      y_bot_right=(y - shape_height))
        self.turtle.end_fill()

    def reset_frame(self):
        self.window.clearscreen()

    def draw_frame(self):
        self.window.update()
