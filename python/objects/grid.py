from dataclasses import dataclass
from .renderers.renderer import Renderer
from .tiles import Tile
from typing import Dict, Tuple, List

import logging

log = logging.getLogger(__package__)


@dataclass
class Grid:
    row_count: int
    col_count: int

    renderer: Renderer

    def __post_init__(self):
        self.tile_width = self.renderer.window_width / self.col_count
        self.tile_height = self.renderer.window_height / self.row_count
        self.tiles: Dict[Tuple[int, int], Tile] = dict()
        self.updated_tiles: List[Tile] = list()
        self.empty_positions: List[Tuple[int, int]] = [
            (x, y) for x in range(self.row_count) for y in range(self.col_count)]

    def add_tile(self, tile: Tile):
        self.tiles[(tile.x, tile.y)] = tile
        self.empty_positions.remove((tile.x, tile.y))
        self.updated_tiles.append(tile)

    def remove_tile(self, x: int, y: int):
        empty_tile = Tile(x=x, y=y)
        self.tiles[(x, y)] = empty_tile
        self.empty_positions.append((x, y))
        self.updated_tiles.append(empty_tile)

    def __convert_coord_to_pixel(self, x: int, y: int) -> Tuple[int, int]:
        pixel_x = x * self.tile_width
        pixel_y = y * self.tile_height
        return pixel_x, pixel_y

    def draw(self):
        for tile in self.updated_tiles:
            if tile.shape:
                log.debug(f"updating following tile: {self.updated_tiles}")
                x, y = self.__convert_coord_to_pixel(x=tile.x, y=tile.y)
                self.renderer.add_shape_to_frame(
                    x=x, y=y, shape_width=self.tile_width, shape_height=self.tile_height, shape=tile.shape, shape_color=tile.color)
        self.updated_tiles.clear()
        self.renderer.draw_frame()
