from __future__ import annotations

from typing import Tuple, Union

import pygame
from pygame.surface import Surface, SurfaceType


class TerrainSquare:
    """
    A square of pixels that represents an area of terrain on the map.

    Attributes:
        terrain_type:   A text description of the type of terrain the square represents and it's RGB colour value
        top_left:       The x and y position of the top left vertex
        top_right:      The x and y position of the top right vertex
        bottom_left:    The x and y position of the bottom left vertex
        bottom_right:   The x and y position of the bottom right vertex
        neighbours:     A list of all the squares that neighbour this square

    Methods:
        draw_square:    Draws the terrain square to a given display surface
        add_neighbour:  Adds a terrain square to the list of this square's neighbours
    """

    def __init__(self, x_pos: int, y_pos: int, terrain_type: Tuple[str, Tuple[int, int, int]], size: int):
        self.terrain_type = terrain_type

        # Vertices information
        self.top_left = (x_pos, y_pos)
        self.top_right = (x_pos + size, y_pos)
        self.bottom_left = (x_pos, y_pos + size)
        self.bottom_right = (x_pos + size, y_pos + size)

        self.neighbours = []

    def draw_square(self, display_surface: Union[Surface, SurfaceType]) -> None:
        pygame.draw.polygon(display_surface, self.terrain_type[1], (self.top_left, self.top_right,
                            self.bottom_right, self.bottom_left), 0)

        pygame.draw.polygon(display_surface, (0, 0, 0), (self.top_left, self.top_right,
                                                         self.bottom_right, self.bottom_left), 1)

    def add_neighbour(self, neighbour_square: TerrainSquare) -> None:
        self.neighbours.append(neighbour_square)
