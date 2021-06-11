from random import randint
from typing import List, Union

from pygame.surface import Surface, SurfaceType

from helper import get_2d_list
from classes.terrain_square import TerrainSquare


def generate_squares(screen_width: int, screen_height: int, square_size: int,
                     display_surface: Union[Surface, SurfaceType], grass_chance: int) -> List[List[TerrainSquare]]:
    """
    This function creates list of terrain squares which have been assigned a value of grass,
    or water randomly based on a given chance threshold.

    :param screen_width:     Width of screen surface as a number of pixels
    :param screen_height:    Height of screen surface as a number of pixels
    :param square_size:      Size of an individual terrain square as a number of pixels
    :param display_surface:  The display surface to draw onto
    :param grass_chance:     The chance that a given terrain square should represent grass

    :return: The finished list of random terrain squares.
    """

    start_x = 0
    start_y = 0

    x = start_x
    y = start_y

    squares_list = get_2d_list(screen_width, screen_height, square_size)

    # Loop over the list of squares and randomly assign each square to be either grass or water and draw each square
    # to the display surface
    for i in range(0, len(squares_list)):
        for j in range(0, len(squares_list[i])):

            rand_type = randint(0, 100)
            if rand_type >= grass_chance:
                terrain_type = ('Grass', (0, 255, 0))
            else:
                terrain_type = ('Water', (0, 0, 255))

            new_square = TerrainSquare(x, y, terrain_type, square_size)

            new_square.draw_square(display_surface)
            squares_list[i][j] = new_square

            x += square_size

        x = start_x
        y += square_size

    # Loop over the list of squares again and tell each terrain square who it's neighbours are
    # (vital for performing the cellular automata functions on the squares)
    for i in range(0, len(squares_list)):
        for j in range(0, len(squares_list[i])):
            if i != 0:
                try:
                    squares_list[i][j].add_neighbour(squares_list[i - 1][j - 1])
                except IndexError:
                    continue
                try:
                    squares_list[i][j].add_neighbour(squares_list[i - 1][j])
                except IndexError:
                    continue
                try:
                    squares_list[i][j].add_neighbour(squares_list[i - 1][j + 1])
                except IndexError:
                    continue
            try:
                squares_list[i][j].add_neighbour(squares_list[i][j - 1])
            except IndexError:
                continue
            try:
                squares_list[i][j].add_neighbour(squares_list[i][j + 1])
            except IndexError:
                continue

            if i != (len(squares_list) - 1):
                try:
                    squares_list[i][j].add_neighbour(squares_list[i + 1][j - 1])
                except IndexError:
                    continue
                try:
                    squares_list[i][j].add_neighbour(squares_list[i + 1][j])
                except IndexError:
                    continue
                try:
                    squares_list[i][j].add_neighbour(squares_list[i + 1][j + 1])
                except IndexError:
                    continue

    return squares_list

