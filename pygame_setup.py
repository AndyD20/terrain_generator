from typing import Union

import pygame
from pygame.surface import Surface, SurfaceType


def setup(screen_width: int, screen_height: int) -> Union[Surface, SurfaceType]:
    """
    Do some basic pygame setup to give us the display surface filled with black pixels, and set the window caption to
    the application name

    :param screen_width:   Width of screen surface as a number of pixels
    :param screen_height:  Height of screen surface as a number of pixels

    :return: The display surface that was set up
    """
    pygame.init()

    display_surface = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption("Terrain Gen")
    display_surface.fill((255, 255, 255))

    return display_surface
