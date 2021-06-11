import sys

import pygame
from pygame.locals import *

import generate_squares
import input
import pygame_setup
import transform

# Declare setup variables ----------------------------------------------------------------------------------------------
from classes.key_input import KeyInput

screen_width = 1600
screen_height = 800
square_size = 12
land_chance = 50
running = True

# Debug shows the output of each iteration, but results in vastly decreased performance of the terrain generation
# as the overhead for the greatly increased amount of drawing to the display surface is quite high.
debug = False
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    # If command line arguments are given, set them to their variables
    if len(sys.argv) > 1:
        try:
            screen_width = int(sys.argv[1])
        except IndexError:
            pass
        try:
            screen_height = int(sys.argv[2])
        except IndexError:
            pass
        try:
            square_size = int(sys.argv[3])
        except IndexError:
            pass
        try:
            land_chance = int(sys.argv[4])
        except IndexError:
            pass
        try:
            debug = sys.argv[5].lower() == 'true'
        except IndexError:
            pass

    # Set up the screen
    display_surface = pygame_setup.setup(screen_width, screen_height)
    terrain_surf = pygame.Surface((screen_width * 2, screen_height * 2), 0, 32)

    # Set up the screen with a random assortment of land and water tiles, return that as a list and assign
    # the neighbours of each tile to one another.
    squares_list = generate_squares.generate_squares(
        screen_width,
        screen_height,
        square_size,
        terrain_surf,
        land_chance
    )
    if debug:
        display_surface.blit(terrain_surf, (0, 0))

    # Prune the tiles based on a rule set, give the land and water definition
    for i in range(0, 7):
        squares_list = transform.transform(squares_list, screen_width, screen_height, square_size, terrain_surf, debug)
        if debug:
            display_surface.blit(terrain_surf, (0, 0))

    # Set up the input script, blit the screen surface for the
    # land and water tiles to the display surface and set the game clock
    key_input = KeyInput(land_chance, terrain_surf, screen_width, screen_height)
    display_surface.blit(terrain_surf, (0, 0))
    clock = pygame.time.Clock()

    # Main loop to keep it running until the user quits
    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False

            # Check user inputs for actions
            terrain_surf = input.compute_input_actions(
                screen_width,
                screen_height,
                square_size,
                display_surface,
                terrain_surf,
                key_input,
                debug
            )

        pygame.display.update()

    pygame.quit()
