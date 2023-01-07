from dataclasses import dataclass, field
from typing import List
from .tiles import Tile


@dataclass
class SnakeTile(Tile):
    pass


@dataclass
class Snake:
    x: int
    y: int

    speed: float
    growth_rate: int

    segments: List[Tile] = field(default_factory=list)

    def __post_init__(self):
        if not self.segments:
            self.segments.append(Tile(x=self.x, y=self.y))

    def update(self):
        pass

    def draw(self):
        for segment in self.segments:
            segment.draw()

    def grow(self):
        pass
