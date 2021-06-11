import math
from typing import Union

import pygame
from pygame.locals import *
from pygame.surface import Surface, SurfaceType

import generate_squares
import transform
from classes.key_input import KeyInput


def compute_input_actions(screen_width: int, screen_height: int, square_size: int,
                          display_surface: Union[Surface, SurfaceType], terrain_surf: Union[Surface, SurfaceType],
                          k_inp: KeyInput, debug: bool) -> Surface:
    """
    This function evaluates any user input from key presses and carries out the related processes

    :param screen_width:     Width of screen surface as a number of pixels
    :param screen_height:    Height of screen surface as a number of pixels
    :param square_size:      Size of an individual terrain square as a number of pixels
    :param display_surface:  The display surface to draw onto
    :param terrain_surf:     The display surface containing the map information
    :param k_inp:            A KeyInput helper
    :param debug:            Debug variable for showing process steps

    :return: The terrain surface with any changes made to it
    """
    # Get all pressed keys
    key = pygame.key.get_pressed()

    # Regenerate the map
    if key[K_r]:
        regen_map(screen_width, screen_height, square_size, terrain_surf, k_inp, debug)

    # Regenerate the map with a decreased land spawning chance
    if key[K_UP]:
        k_inp.land_chance += 1
        regen_map(screen_width, screen_height, square_size, terrain_surf, k_inp, debug)

    # Regenerate the map with an increased land spawning chance
    if key[K_DOWN]:
        k_inp.land_chance -= 1
        regen_map(screen_width, screen_height, square_size, terrain_surf, k_inp, debug)

    # Save the map to an image
    if key[K_s]:
        pygame.image.save(terrain_surf, 'map.png')

    # Check if the user tried to drag the screen view around
    drag_screen(k_inp, display_surface)

    # Zoom out
    if key[K_MINUS]:
        zoom_out(k_inp, screen_width, screen_height, terrain_surf, display_surface, square_size)

    # Zoom in
    if key[K_EQUALS]:
        zoom_in(k_inp, screen_width, screen_height, terrain_surf, display_surface, square_size)

    return terrain_surf


def regen_map(screen_width: int, screen_height: int, square_size: int, terrain_surf: Union[Surface, SurfaceType],
              k_inp: KeyInput, debug: bool) -> None:
    """
    This function regenerates the terrain map with a new random seed

    :param screen_width:     Width of screen surface as a number of pixels
    :param screen_height:    Height of screen surface as a number of pixels
    :param square_size:      Size of an individual terrain square as a number of pixels
    :param terrain_surf:     The display surface containing the map information
    :param k_inp:            A KeyInput helper
    :param debug:            Debug variable for showing process steps
    """
    squares_list = generate_squares.generate_squares(screen_width, screen_height, square_size, terrain_surf,
                                                     k_inp.land_chance)

    for i in range(0, 7):
        squares_list = transform.transform(squares_list, screen_width, screen_height, square_size,
                                           terrain_surf, debug)
    k_inp.terrain_surf_copy = terrain_surf


def drag_screen(k_inp: KeyInput, display_surface: Union[Surface, SurfaceType]) -> None:
    """
    This function allows the user to drag the view around to show different areas of the terrain map

    :param display_surface:  The display surface to draw onto
    :param k_inp:            A KeyInput helper
    """
    if pygame.mouse.get_pressed(3)[0]:
        try:
            mouse_pos = pygame.mouse.get_pos()
            if k_inp.old_mouse_pos != (0, 0):
                k_inp.diff = (mouse_pos[0] - k_inp.old_mouse_pos[0], mouse_pos[1] - k_inp.old_mouse_pos[1])
                k_inp.old_mouse_pos = mouse_pos
            else:
                k_inp.old_mouse_pos = mouse_pos

        except AttributeError:
            print("Something went wrong d")
    else:
        k_inp.old_mouse_pos = (0, 0)
        k_inp.diff = (0, 0)

    # Set changes made to the current position of the display surface to enable the view dragging behaviour,
    # trying to ensure that the screen surface doesn't exceed the bounds of the terrain surface.
    # TODO make this work properly when the view is zoomed in or out, currently only works properly for default view
    if k_inp.is_new_pos_in_x_bound() and k_inp.is_new_pos_in_y_bound():
        k_inp.current_surface_pos = k_inp.get_new_surface_pos()

    blit_to_display(display_surface, k_inp)


def zoom_out(k_inp: KeyInput, screen_width: int, screen_height: int, terrain_surf: Union[Surface, SurfaceType],
             display_surface: Union[Surface, SurfaceType], square_size: int) -> None:
    """
    This function allows the user to zoom the view out to see a larger amount of the terrain map

    :param k_inp:            A KeyInput helper
    :param screen_width:     Width of screen surface as a number of pixels
    :param screen_height:    Height of screen surface as a number of pixels
    :param terrain_surf:     The display surface containing the map information
    :param display_surface:  The display surface to draw onto
    :param square_size:      Size of an individual terrain square as a number of pixels
    """
    if k_inp.terrain_surf_copy.get_width() > screen_width + math.ceil(terrain_surf.get_width() / 5):
        k_inp.terrain_surf_copy = pygame.transform.smoothscale(
            terrain_surf,
            (
                k_inp.get_width() - square_size * math.ceil(screen_width / 20),
                k_inp.get_height() - square_size * math.ceil(screen_height / 20)
            )
        )

        blit_to_display(display_surface, k_inp)


def zoom_in(k_inp: KeyInput, screen_width: int, screen_height: int, terrain_surf: Union[Surface, SurfaceType],
            display_surface: Union[Surface, SurfaceType], square_size: int) -> None:
    """
        This function allows the user to zoom the view in to see a smaller amount of the terrain map

        :param k_inp:            A KeyInput helper
        :param screen_width:     Width of screen surface as a number of pixels
        :param screen_height:    Height of screen surface as a number of pixels
        :param terrain_surf:     The display surface containing the map information
        :param display_surface:  The display surface to draw onto
        :param square_size:      Size of an individual terrain square as a number of pixels
        """

    if k_inp.get_width() < screen_width * 3:
        k_inp.terrain_surf_copy = pygame.transform.smoothscale(
            terrain_surf,
            (
                k_inp.get_width() + square_size * math.ceil(screen_width / 20),
                k_inp.get_height() + square_size * math.ceil(screen_height / 20)
            )
        )

        blit_to_display(display_surface, k_inp)


def blit_to_display(display_surface: Union[Surface, SurfaceType], k_inp: KeyInput) -> None:
    """
    Function to blit terrain position changes to the display
    e.g. when the user drags the map around, or zooms in or out

    :param display_surface:  The display surface to draw onto
    :param k_inp:            A KeyInput helper
    """
    display_surface.blit(
        k_inp.terrain_surf_copy,
        (
            k_inp.current_surface_pos[0],
            k_inp.current_surface_pos[1]
        )
    )