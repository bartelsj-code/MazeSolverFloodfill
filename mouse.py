from graphics import *
from colors import *
import math
from time import sleep, perf_counter
from tile_node import TileNode
from collections import deque
from variables_to_change import *


class Mouse:
    def __init__(self, tile, goal_coords, grid_size, window, size):
        self.checked = {}
        self.move_duration = time_taken_per_step
        self.fps = 20
        self.start_coords = tile.coords
        self.current_tile = tile
        self.goal_coords = goal_coords
        self.grid_size = grid_size
        self.win = window
        self.scale_size = size
        self.real_coords = self.current_tile.center_coords
        self.set_nodes = {}
        self.explored = {}
        self.optimal = {}
        self.make_node_grid()
        self.make_shape()
        self.goal_reached = False

    def set_current_node(self):
        #identify node that matches tile mouse is on in maze
        x = self.current_tile.coords[0]
        y = self.current_tile.coords[1]
        self.current_node = self.node_grid[x][y]
        self.explored[self.current_node] = True


    def choose_next_move(self):
        #returns a tuple that has coordinates of square mouse will move to
        self.set_current_node()
        nodes_to_propogate = [self.current_node] + self.update_connections()
        self.execute_propogation(nodes_to_propogate)
        # if consider_risk:
        #     node = self.choose_risk_node()
        # else:
        #     node = self.choose_move_node()
        node = self.choose_move_node()
        if node.coords == self.goal_coords:
            self.when_done()
        if print_floodfill_after_each_move:
            self.display_grid()
        return node.coords
    
    def when_done(self):
        #remembers optimal path and notes completion
        self.remember_optimal()
        self.goal_reached = True



# this did not work
    # def choose_risk_node(self):
    #     if self.current_node in self.optimal and self.goal_reached:
    #         best_value = 50000000
    #         best_node = None
    #         for node in self.current_node.neighbors:
    #             if node in self.optimal:
    #                 value = node.distance_to_goal
    #             else:
    #                 value = node.value * risk_aversion
    #             if value <= best_value:
    #                 if value < best_value:
    #                     best_value = value
    #                     best_node = node
    #                 else:
    #                     if best_node not in self.explored:
    #                         best_node = node
    #         return best_node
    #     else:
    #         best_value = 50000000
    #         best_node = None
    #         for node in self.current_node.neighbors:
    #             value = node.value
    #             if node in self.optimal:
    #                 value = node.distance_to_goal / risk_aversion
                    
    #             if value <= best_value:
    #                 if value < best_value:
    #                     best_value = value
    #                     best_node = node
    #                 else:
    #                     if best_node in self.explored:
    #                         best_node = node
    #         return best_node
        
        

    def choose_move_node(self):
        # goes through nodes neighboring current node and identifies best to move to
        best_value = 50000000
        best_node = None
        for node in self.current_node.neighbors:
            value = node.value
            if node in self.optimal:
                value -= 0.2
            if node in self.explored:
                value -= 0.1
            if value <= best_value:
                if value < best_value:
                    best_value = value
                    best_node = node
                else:
                    if best_node not in self.explored:
                        best_node = node
        return best_node
    

    def remember_optimal(self):
        # uses BFS to find best path within explored tiles 
        for node in self.optimal:
            node.distance_to_goal = 50000
        self.optimal = {}
        self.checked = {}
        self.explored[self.node(self.goal_coords)] = True
        self.path_found = False
        start = self.node(self.start_coords)
        start.parent = None
        queue = deque([start])
        while len(queue) > 0:
            node = queue.popleft()
            if node.coords == self.goal_coords:
                self.path_found = True
                break
            self.checked[node] = True
            for neighbor in node.neighbors:
                if neighbor in self.explored:
                    if neighbor not in self.checked:
                        neighbor.parent = node
                        queue.append(neighbor)

        node = self.node(self.goal_coords)
        while node.parent != None:
            self.optimal[node] = True
            node = node.parent
        for node in self.node_list:
            node.parent = None


    def execute_propogation(self, nodes2):
        # takes in a list of severed nodes and executes propogation procedure on them.
        nodes = nodes2[:]
        done = False
        i = 0
        while not done and i < 50:
            revisit = self.propogate(nodes)
            nodes = revisit
            if len(nodes) == 0:
                done = True
            i += 1

    def propogate(self, nodes2):
        # takes in list of nodes requiring updating and updates them and neighbors 
        nodes = nodes2[:]
        revisit = []
        queue = deque(nodes)
        while len(queue) > 0:
            node = queue.popleft()
            if node.flood_update_value():
                for neighbor in node.neighbors:
                    queue.append(neighbor)
                if node in nodes2:
                    revisit.append(node)
        return revisit
        
    def display_grid(self):
        # displays current 2d node grid in terminal
        string = ""
        for y in range(self.grid_size-1, -1, -1):
            for x in range(0, self.grid_size):
                string += repr(self.node_grid[x][y]) + ","
            string += "\n"
        print(string)

    def update_connections(self):
        # severs connections between nodes based upon walls in maze
        to_block_coords = self.current_tile.get_illegal_neighbor_coords()
        blockees = []
        for coords in to_block_coords:
            blockee = self.node_grid[coords[0]][coords[1]]
            blockees.append(blockee)
            self.current_node.block_node(blockee)
        return blockees

    def make_node_grid(self):
        #generates grid of nodes to represent tiles in maze
        self.make_nodes()
        self.neighbor_nodes()
        self.populate_values()

    def node(self, coords):
        #takes in coordinates tuple and returns node at that location
        return self.node_grid[coords[0]][coords[1]]

    def populate_values(self):
        #goes through and radially updates values from from goal node such that they get larger going outwards. 
        has_been_queued = {}
        goal_node = self.node(self.goal_coords)
        goal_node.set_value(0)
        has_been_queued[goal_node] = True
        queue = deque([])
        for neighbor in goal_node.neighbors:
            queue.append(neighbor)
            has_been_queued[neighbor] = True
        while len(queue) > 0:
            current = queue.popleft()
            current.set_start_value()
            for neighbor in current.neighbors:
                if neighbor not in has_been_queued:
                    queue.append(neighbor)
                    has_been_queued[neighbor] = True
            
    def get_neighbor_coords(self, coords):
        # returns set of four or less coordinates tuples that are the coordinates neighboring a coordinate tuple
        x = coords[0]
        y = coords[1]
        coords_list = [(x,y+1),(x,y-1),(x-1,y),(x+1,y)]
        valid_coords = []
        for coords in coords_list:
            if are_valid_coords(coords, self.grid_size):
                valid_coords.append(coords)
        return valid_coords

    def neighbor_nodes(self):
        #goes through all nodes and adds their neighboring nodes to a local list "connecting them"
        for node in self.node_list:
            neighbor_coords = self.get_neighbor_coords(node.coords)
            for coords in neighbor_coords:
                node.neighbors.append(self.node_grid[coords[0]][coords[1]])

    def make_nodes(self):
        #makes and fills grid with nodes
        self.node_list = []
        self.node_grid = empty_grid(self.grid_size)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                node = TileNode((x,y))
                self.node_grid[x][y] = node
                self.node_list.append(node)

    def make_shape(self):
        #creates shape of mouse for graphics
        coords = self.real_coords
        self.shape = Circle(Point(coords[0],coords[1]), self.scale_size/3)
        self.shape.setFill(mouse_color)
        self.shape.setWidth(0)

    def undraw(self):
        #undraws mouse
        self.shape.undraw()

    def draw(self):
        #draws mouse
        self.shape.draw(self.win)

    def move_to_tile(self, tile):
        #moves the mouse and updates current tile location
        self.current_tile = tile
        self.move()

    def move(self):
        #animates mouse between tiles of maze
        frames = max(1,math.floor(self.move_duration*self.fps))
        change_x = self.current_tile.center_coords[0] - self.real_coords[0]
        change_y = self.current_tile.center_coords[1] - self.real_coords[1]
        step_change_x = change_x/frames
        step_change_y = change_y/frames
        
        for i in range(frames):
            time1 = perf_counter()
            self.shape.move(step_change_x, step_change_y)
            time2 = perf_counter()
            sleep(max(0,(self.move_duration/self.fps) - (time2-time1)))
        self.real_coords = self.current_tile.center_coords

def empty_grid(length):
    #creates and empty grid to fill with nodes
    lst1 = []
    for x in range(length):
        lst2 = []
        for y in range(length):
            content = None
            lst2.append(content)
        lst1.append(lst2)
    return lst1

def are_valid_coords(coords, max):
    #checks a set of coords to see if they lie within the maze
    x = coords[0]
    y = coords[1]
    if x < 0 or x > max-1:
        return False
    if y < 0 or y > max-1:
        return False
    return True
