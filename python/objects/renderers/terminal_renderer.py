from dataclasses import dataclass
from .renderer import Renderer, Shapes, Colors

TERMINAL_SHAPE_DICT = {
    Shapes.CIRCLE: "o",
    Shapes.SQUARE: "■",
}

TERMINAL_COLORS_DICT = {
    Colors.WHITE: "white",
    Colors.BLACK: "black",
    Colors.BLUE: "blue",
    Colors.RED:  "red",
}


@dataclass
class TerminalRenderer(Renderer):
    def __post_init__(self):
        self.frame_buffer = [" "] * self.window_width * self.window_height

    def add_shape_to_frame(self, x: int, y: int, shape: Shapes = Shapes.CIRCLE, shape_width: int = None, shape_height: int = None, shape_color: Colors = Colors.BLACK):
        character = TERMINAL_SHAPE_DICT[shape]
        index = int(y * self.window_width + x)

        print(x, y, index)
        print()

        self.frame_buffer[index] = character

    def draw_frame(self):
        print("\033[2J")
        frame_border = "#" * (self.window_width + 2)
        print(frame_border)
        for line in range(self.window_height):
            line_start = line * self.window_height
            line_end = line_start + self.window_width
            line_str = "".join(self.frame_buffer[line_start:line_end])
            print(f"#{line_str}#")
        print(frame_border)
