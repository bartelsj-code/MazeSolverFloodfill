from variables_to_change import *

from maze import Maze
from graphics import *

if __name__ == "__main__":
    #thought this would be a bigger file. runs maze.
    side_length = maze_size
    window_length = window_size
    maze = Maze(side_length, window_length, edges_hidden = walls_vanish, color_tiles = path_highlighted)
    maze.mouse()
    g = input("hit enter to close")