from enum import Enum
from .renderer import Renderer, Colors
from .turtle_renderer import TurtleRenderer
from .terminal_renderer import TerminalRenderer


class RendererType(Enum):
    TURTLE = TurtleRenderer
    TERMINAL = TerminalRenderer


class RendererFactory:
    def get_renderer(window_width: int,
                     window_height: int,
                     window_bgcolor: Colors = Colors.WHITE,
                     type: RendererType = RendererType.TURTLE) -> Renderer:
        renderer_consturctor = type.value
        return renderer_consturctor(window_width=window_width,
                                    window_height=window_height,
                                    window_bgcolor=window_bgcolor)
