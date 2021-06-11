from typing import Union

from pygame.surface import SurfaceType, Surface


class KeyInput:
    """
        A helper class to assist with management of user input actions

        Attributes:
            land_chance:          The percentage chance that a terrain square should represent grass
            old_mouse_pos:        The position of the mouse in the last frame
            diff:                 The difference between the old mouse position and the new position
            current_surface_pos:  The x and y position of the top left vertex of the display surface
            terrain_surf_copy:    A copy of the terrain surface
            screen_width:         Width of screen surface as a number of pixels
            screen_height:        Height of screen surface as a number of pixels

        Methods:
            get_width:              Get the width of the terrain surface
            get_height:             Get the heigh of the terrain surface
            new_x_pos:              Get the new x position of the mouse
            new_y_pos:              Get the new y position of the mouse
            is_new_pos_in_x_bound:  Determine if the new x position of the mouse is in a legal area
            is_new_pos_in_y_bound:  Determine if the new y position of the mouse is in a legal area
        """

    def __init__(self, land_chance: int, terrain_surf_copy: Union[Surface, SurfaceType], screen_width: int,
                 screen_height: int):
        self.land_chance = land_chance
        self.old_mouse_pos = (0, 0)
        self.diff = (0, 0)
        self.current_surface_pos = (0, 0)
        self.terrain_surf_copy = terrain_surf_copy
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_width(self):
        return self.terrain_surf_copy.get_width()

    def get_height(self):
        return self.terrain_surf_copy.get_height()

    def new_x_pos(self):
        return self.current_surface_pos[0] + self.diff[0]

    def new_y_pos(self):
        return self.current_surface_pos[1] + self.diff[1]

    def is_new_pos_in_x_bound(self):
        return (
                0 - self.get_width() < self.new_x_pos() <
                0 < self.new_x_pos() + (self.get_width() / 2) < self.screen_width * 2
        )

    def is_new_pos_in_y_bound(self):
        return (
                0 - self.get_height() < self.new_y_pos() <
                0 < self.new_y_pos() + (self.get_height() / 2) < self.screen_height * 2
        )

    def get_new_surface_pos(self):
        return self.current_surface_pos[0] + self.diff[0], self.current_surface_pos[1] + self.diff[1]