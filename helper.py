import math

from typing import List, Any


def get_2d_list(screen_width: int, screen_height: int, square_size: int) -> List[List[Any]]:
    """
    Get a 2d list of zeros, corresponding to double the values of the screen width and height.
    The list is double the size of the screen size so that we have extra available map area and can
    therefore drag the view around the map and look at it zoomed in or out.

    :param screen_width:   Width of screen surface as a number of pixels
    :param screen_height:  Height of screen surface as a number of pixels
    :param square_size:    Size of an individual terrain square as a number of pixels

    :return: The complete 2d list of zeros
    """

    max_x = math.ceil(screen_width / square_size) * 2
    max_y = (math.ceil(screen_height / square_size) + 20) * 2

    # Could use numpy.zeros((max_y, max_x), dtype=int).tolist() here instead, but I'm not sure if the speed
    # difference justifies bringing in the numpy requirement?
    squares_list = [[0 for x in range(max_x)] for y in range(max_y)]
    return squares_list
