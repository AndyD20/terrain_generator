from random import randint
from typing import List, Union

import pygame
from pygame.surface import Surface, SurfaceType

from helper import get_2d_list
from classes.terrain_square import TerrainSquare


def transform(original_list: List[List[TerrainSquare]], screen_width: int, screen_height: int, square_size: int,
              display_surface: Union[Surface, SurfaceType], show_process: bool) -> List[List[TerrainSquare]]:
    """
    This function acts as the cellular automata algorithm; it takes the list of terrain squares and transforms each
    square according to the state of it's neighbours. With successive iterations this smooths out the terrain into
    more well defined areas.

    :param original_list:    The starting list of terrain squares
    :param screen_width:     Width of screen surface as a number of pixels
    :param screen_height:    Height of screen surface as a number of pixels
    :param square_size:      Size of an individual terrain square as a number of pixels
    :param display_surface:  The display surface to draw onto
    :param show_process:     Debug variable which, when set to true,
                             shows the output of each iteration of running the transform

    :return: The transformed list of terrain squares
    """

    squares_list = get_2d_list(screen_width, screen_height, square_size)

    for i in range(0, len(original_list)):
        for j in range(0, len(original_list[i])):

            # Land pruning ----------------------------------------------------------------------------------

            if original_list[i][j].terrain_type[0] == "Grass":

                # Set neighbour counts
                neighbour_count = 0
                mountain_neighbour_count = 0

                # Find neighbours
                for neighbour in original_list[i][j].neighbours:
                    if neighbour.terrain_type[0] == "Grass":
                        neighbour_count += 1

                for neighbour in original_list[i][j].neighbours:
                    if neighbour.terrain_type[0] == "Mountain":
                        mountain_neighbour_count += 1

                # Create mountains
                mountain_true = randint(0, 1000)
                if neighbour_count > 7 and mountain_true > 999:
                    set_as_mountain(i, j, squares_list, original_list, display_surface, show_process)
                elif neighbour_count + mountain_neighbour_count > 3:
                    squares_list[i][j] = original_list[i][j]
                else:
                    set_as_water(i, j, squares_list, original_list, display_surface, show_process)

                # Turn grass to mountain if right amount of neighbours are mountain
                mountain_chance = randint(0, 1000)
                if 3 > mountain_neighbour_count >= 1 and mountain_chance > 900:
                    set_as_mountain(i, j, squares_list, original_list, display_surface, show_process)
                else:
                    squares_list[i][j] = original_list[i][j]
            # ------------------------------------------------------------------------------------------------

            # Water pruning ----------------------------------------------------------------------------------
            elif original_list[i][j].terrain_type[0] == "Water":
                neighbour_count = 0
                for neighbour in original_list[i][j].neighbours:
                    if neighbour.terrain_type[0] == "Grass" or neighbour.terrain_type[0] == "Mountain":
                        neighbour_count += 1
                if neighbour_count > 4:
                    set_as_grass(i, j, squares_list, original_list, display_surface, show_process)
                else:
                    squares_list[i][j] = original_list[i][j]
            # -------------------------------------------------------------------------------------------------

            # Mountain pruning --------------------------------------------------------------------------------
            elif original_list[i][j].terrain_type[0] == "Mountain":
                water_neighbour_count = 0

                for neighbour in original_list[i][j].neighbours:
                    if neighbour.terrain_type[0] == "Water":
                        water_neighbour_count += 1

                if water_neighbour_count > 6:
                    set_as_grass(i, j, squares_list, original_list, display_surface, show_process)
                else:
                    squares_list[i][j] = original_list[i][j]
            # -------------------------------------------------------------------------------------------------

    return squares_list


def set_as_mountain(i, j, squares_list, original_list, display_surface, show_process):
    set_as_type(("Mountain", (146, 146, 135)), i, j, squares_list, original_list, display_surface, show_process)


def set_as_water(i, j, squares_list, original_list, display_surface, show_process):
    set_as_type(("Water", (0, 0, 255)), i, j, squares_list, original_list, display_surface, show_process)


def set_as_grass(i, j, squares_list, original_list, display_surface, show_process):
    set_as_type(("Grass", (0, 255, 0)), i, j, squares_list, original_list, display_surface, show_process)


def set_as_type(terrain_type, i, j, squares_list, original_list, display_surface, show_process):
    squares_list[i][j] = original_list[i][j]
    squares_list[i][j].terrain_type = terrain_type
    squares_list[i][j].draw_square(display_surface)
    if show_process:
        pygame.display.update()
