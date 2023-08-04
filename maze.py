from graphics import *
from maze_tile import Tile
from goal_marker import GoalMarker
from mouse import Mouse
from colors import *
import random
import math
from time import sleep
from variables_to_change import *

random.seed(seed)

class Maze:
    def __init__(self, side_length, win_size, edges_hidden, color_tiles):
        self.marked_tiles = {}
        self.color_tiles = color_tiles
        self.edges_hidden = edges_hidden
        self.window_length = win_size
        self.side_length = side_length
        self.generate_maze()
        
    def mouse(self):
        #do mouse stuff
        self.micromouse()

    def make_mouse(self):
        #create and draw mouse
        self.win.changeTitle("Micromouse Maze: Generating Mouse...")
        tile = self.start_tile
        goal_coords = self.goal_tile.coords
        grid_size = self.side_length
        self.mouse = Mouse(tile, goal_coords, grid_size, self.win, self.tile_length)
        self.mouse.draw()

    def micromouse(self):
        #mouse stuff
        self.make_mouse()
        self.do_solve()
        
    def do_solve(self):
        #do n laps through maze
        for i in range(laps_to_take):
            self.win.changeTitle("Lap {}".format(i+1))
            self.mouse.move_to_tile(self.start_tile)
            self.reveal_edges(self.start_tile)
            self.color_visited_tile(self.start_tile)
            self.run_maze()
            if show_best_found:
                self.show_best_path()

            if print_floodfill_grid_at_end_of_run:
                self.mouse.display_grid()
        
    def run_maze(self):
        #loops through moving mouse and asking mouse what tile it wants to move to
        self.mouse.undraw()
        self.mouse.draw()
        new_tile = None
        move_coords = self.mouse.choose_next_move()
        new_tile = self.tile_grid[move_coords[0]][move_coords[1]]
        while new_tile != self.goal_tile:
            self.mouse.move_to_tile(new_tile)
            self.reveal_edges(new_tile)
            self.color_visited_tile(new_tile)
            move_coords = self.mouse.choose_next_move()
            new_tile = self.tile_grid[move_coords[0]][move_coords[1]]

    def color_visited_tile(self, tile):
        if self.color_tiles:
            tile.color(visited_tile_color)

    def show_best_path(self):
        #shows best path bfs
        for tile in self.tile_list:
            tile.unshow_marker()
        for node in self.mouse.optimal:
            coords = node.coords
            tile = self.tile_grid[coords[0]][coords[1]]
            tile.show_best_marker()

    def reveal_edges(self, tile):
        for edge in tile.edges_list:
            if edge.placed == True:
                edge.draw()

    def generate_maze(self):
        #all the steps of generating maze window
        self.make_window()
        self.tiles_info()
        self.make_tiles()
        self.set_all_neighbors()
        self.update_all_neighbors()
        self.make_edges()
        self.set_start_and_goal()
        self.draw_goal_marker()
        self.place_all_edges()
        self.create_maze_layout()
        self.hide_edges()

    def hide_edges(self):
        #makes edges invisible without removing them from maze
        if self.edges_hidden:
            self.win.changeTitle("Micromouse Maze: Hiding Walls...")
            sleep(delay_before_walls_vanish)
            for edge in self.all_edges:
                edge.undraw()

    def create_maze_layout(self):
        #draws path_num paths through maze and then removes random edges and edges in un-pathed areas
        self.visited = {}
        for i in range(path_num):
            self.make_path(i+1)        
        self.pick_out_edges()

    def pick_out_edges(self):
        #removes edges from tiles
        self.win.changeTitle("Micromouse Maze: Filling Gaps...")
        opts = [1,1,1,1,1,1,2,2,2,2]
        to_pick_at = self.get_unvisited()
        #tiles that path visited
        for tile in self.visited:
            chance = random.randint(0, wall_gaps)
            if chance == 0:
                to_pick_at.append(tile)
        #overlooked areas
        for tile in to_pick_at:
            reps = opts[random.randint(0, len(opts)-1)]
            i = 0
            while i < reps:
                num = random.randint(0, len(tile.edges)-1)
                edge = tile.edges[num]
                if edge != None:
                    edge.remove()
                i += 1
        
    def get_unvisited(self):
        #get overlooked areas
        pickees = self.tile_list[:]
        for tile in self.tile_list:
            if tile in self.visited:
                pickees.remove(tile)
        return pickees


    def make_path(self, number):
        #makes a path through maze (from start to finish if that is avaliable)
        self.win.changeTitle("Micromouse Maze: Generating Path {}...".format(number))
        self.random_direction = random.randint(0,3)
        
        current_tile = self.start_tile
        while current_tile != self.goal_tile:
            self.dont_clear = False
            chance_of_heading_to_goal = random.randint(0, directness)
            change_direction = random.randint(0, straightness)
            if chance_of_heading_to_goal == 0:
                next_tile = self.direct_step(current_tile)
            else:
                next_tile = self.random_step(current_tile, change_direction)
            if not self.dont_clear:
                self.remove_edge(current_tile, next_tile)

            self.visited[current_tile] = True
            current_tile = next_tile
        self.visited[self.goal_tile] = True
     

    def remove_edge(self, tile1, tile2):
        edge = tile1.get_common_edge(tile2)
        edge.remove()

    def random_step(self, ct, cd):
        #add a random step to path (based on chance of direction changing)
        current_tile = ct
        change_direction = cd

        if change_direction == 0:
            self.random_direction = random.randint(0,3)

        neighbor = current_tile.neighbors_directed[self.random_direction]
        if neighbor != None and neighbor not in self.visited:
            return neighbor
        else:
            neighbors = current_tile.neighbors
            option_tiles = neighbors[:]
            for neighbor in neighbors:
                if neighbor in self.visited:
                    option_tiles.remove(neighbor)
            if len(option_tiles) == 0:
                option_tiles = neighbors
                self.dont_clear = True
            return option_tiles[random.randint(0,len(option_tiles)-1)]

    def direct_step(self, current_tile):
        #adds step to path that is closest to goal tile (if possible)
        neighbors = current_tile.neighbors
        option_tiles = neighbors[:]
        for neighbor in neighbors:
            if neighbor in self.visited:
                option_tiles.remove(neighbor)
        if len(option_tiles) == 0:
            self.dont_clear = True
            option_tiles = neighbors
        random.shuffle(option_tiles)
        best_distance = 1000
        best_tile = None
        for option_tile in option_tiles:
            distance = self.get_distance(self.goal_tile, option_tile)
            if best_distance > distance:
                best_tile = option_tile
                best_distance = distance
        return best_tile
                        
                    
    def get_distance(self, tile1, tile2):
        #distance between two tiles
        deltax = tile2.coords[0] - tile1.coords[0]
        deltay = tile2.coords[1] - tile1.coords[1]
        dist = math.sqrt(deltax**2 + deltay**2)
        return dist

    def draw_goal_marker(self):
        #draws red X
        coords = self.goal_tile.center_coords
        marker = GoalMarker(self.tile_length, self.win, coords)
        marker.draw()

    def set_start_and_goal(self):
        #sets start and goal tiles (tries to keep them decently far apart)
        dist = 0
        i = 0
        while dist < self.side_length * 0.75 and i < 16:
            self.set_goal_tile()
            self.set_start_tile()
            dist = self.get_distance(self.start_tile, self.goal_tile)
            i += 1
        p = Point(self.start_tile.center_coords[0], self.start_tile.center_coords[1])
        circle = Circle(p, self.tile_length*0.2)  
        circle.setOutline(start_marker_color)
        circle.setWidth(self.tile_length*0.18)
        circle.draw(self.win)

    def set_goal_tile(self):
        x = random.randint(0,self.side_length-1)
        y = random.randint(0,self.side_length-1)
        self.goal_tile = self.tile_grid[x][y]

    def set_start_tile(self):
        self.start_tile = self.goal_tile
        while self.start_tile == self.goal_tile:
            x = random.randint(0,self.side_length-1)
            y = random.randint(0,self.side_length-1)
            self.start_tile = self.tile_grid[x][y]
        
    def place_all_edges(self):
        #places all tiles on maze
        self.win.changeTitle("Micromouse Maze: Generating Walls...")
        for edge in self.all_edges:
            edge.place()
    
    def make_edges(self):
        #makes list of all edges in maze
        self.all_edges = []
        counter = 0
        for row in self.tile_grid:
            start = counter % 2
            for i in range(start, len(row), 2):
                tile = row[i]
                self.all_edges += tile.create_edges()
            counter += 1
        
    def update_all_neighbors(self):
        for tile in self.tile_list:
            tile.update_neighbors()
        
    def set_all_neighbors(self):
        #creates neighbor relationships between appropiate tiles in maze
        self.win.changeTitle("Micromouse Maze: Generating Tiles Adjacencies...")
        for i in range(len(self.tile_list)):
            tile = self.tile_list[i]
            self.get_tile_neighbors(tile)

    def get_tile_neighbors(self, tile):
        #determines which tiles should be neighbors to input tile and sets them as such
        x = tile.coords[0]
        y = tile.coords[1]
        coords_lst = [(x, y+1),(x+1, y),(x, y-1),(x-1, y)]
        for i in range(4):
            neighbor = self.get_tile(coords_lst[i])
            position = i
            tile.set_neighbor(position, neighbor)
        
    def get_tile(self, coords):
        #given a set of coordinates, returns tile
        for value in coords:
            if value < 0 or value > self.side_length-1:
                return None
        return self.tile_grid[coords[0]][coords[1]]
        
    def tiles_info(self):
        #sets length of graphics object tiles
        self.tile_length = self.window_length/self.side_length

    def make_tiles(self):
        #creates and populates grid with tile objects
        self.win.changeTitle("Micromouse Maze: Generating Tiles...")
        self.tile_list = []
        self.tile_grid = empty_grid(self.side_length)
        for x in range(self.side_length):
            for y in range(self.side_length):
                tile = Tile(self.tile_length, (x,y), self.win, self.side_length)
                self.tile_grid[x][y] = tile
                self.tile_list.append(tile)
        
    def make_window(self):
        #makes UI window
        self.win = GraphWin("Micromouse Maze", self.window_length, self.window_length)
        sleep(1)

def empty_grid(length):
    #creates empty list
    lst1 = []
    for x in range(length):
        lst2 = []
        for y in range(length):
            content = None
            lst2.append(content)
        lst1.append(lst2)
    return lst1
