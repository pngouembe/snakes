from enum import Enum

from .pygame_renderer import PygameRenderer
from .renderer import Colors, Renderer
from .terminal_renderer import TerminalRenderer
from .turtle_renderer import TurtleRenderer


class RendererType(Enum):
    TURTLE = TurtleRenderer
    TERMINAL = TerminalRenderer
    PYGAME = PygameRenderer


class RendererFactory:
    @staticmethod
    def get_renderer(window_width: int,
                     window_height: int,
                     window_bgcolor: Colors = Colors.WHITE,
                     type: RendererType = RendererType.TURTLE) -> Renderer:
        renderer_consturctor = type.value
        return renderer_consturctor(window_width=window_width,
                                    window_height=window_height,
                                    window_bgcolor=window_bgcolor)
