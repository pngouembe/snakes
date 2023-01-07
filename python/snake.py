#! python3
"""Snake game's python version"""

from objects.renderers.rendererfactory import RendererFactory, RendererType
from objects.renderers.renderer import Renderer, Colors, Shapes

from objects.grid import Grid
from objects.tiles import Tile

from time import sleep


def update():
    pass


def draw():
    pass


def gameLoop():
    while True:
        update()
        draw()


def main():
    renderer_config = {
        "window_width": 600,
        "window_height": 600,
        "window_bgcolor": Colors.WHITE,
        "type": RendererType.TURTLE
    }

    renderer: Renderer = RendererFactory.get_renderer(**renderer_config)
    grid = Grid(row_count=21, col_count=21, renderer=renderer)
    tile = Tile(x=0, y=0, shape=Shapes.SQUARE, color=Colors.BLACK)
    tile2 = Tile(x=1, y=0, shape=Shapes.CIRCLE, color=Colors.RED)
    grid.add_tile(tile=tile)
    grid.add_tile(tile=tile2)
    grid.draw()

    tile3 = Tile(x=1, y=2, shape=Shapes.SQUARE, color=Colors.BLUE)
    grid.add_tile(tile=tile3)
    grid.remove_tile(x=tile.x, y=tile.y)

    sleep(2)
    grid.draw()

    while True:

        gameLoop()


if __name__ == "__main__":
    main()
