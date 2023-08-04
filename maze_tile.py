from graphics import *
from maze_edge import Edge
from colors import *
from variables_to_change import *


class Tile:
    def __init__(self, size, coords, win, maze_length):
        self.edges = {0:None,1:None,2:None,3:None}
        self.edges_list = []
        self.maze_length = maze_length
        self.win = win
        self.size = size
        self.coords = coords
        #all adjacent tiles
        self.neighbors = []
        #all adjacent tiles true/false for blocked by edge
        self.neighbor_visitable = {}
        #adjacent tiles (in order clockwise)
        self.neighbors_directed = [0,0,0,0]
        self.neighbor_edge_dict = {}
        self.drawnb = False
        self.set_real_coords()
        self.set_center_coords()
        self.set_shape()
        self.draw()
        self.best_marker()
        pass

    def unshow_marker(self):
        #removes best path marker
        if self.drawnb:
            self.marker.undraw()
            self.drawnb = False


    def show_best_marker(self):
        #draws best path marker
        if self.drawnb == False:
            self.marker.draw(self.win)
            self.drawnb = True

    def best_marker(self):
        #best path marker
        point = Point(self.center_coords[0],self.center_coords[1])
        radius = self.size * 0.08
        self.marker = Circle(point, radius)
        self.marker.setFill(best_found_color)
        self.marker.setWidth(0)

    def get_illegal_neighbor_coords(self):
        #returns list of coordinates for neighbors that cannot be reached due to walls.
        #this is the input the mouse gets regarding a tile
        lst = []
        for tile in self.neighbors:
            if self.neighbor_visitable[tile] == False:
                lst.append(tile.coords)
        return lst

    def get_common_edge(self, neighbor):
        #takes in neighbor tile, gets common edge
        return self.neighbor_edge_dict[neighbor]

    def disconnect_from(self, neighbor):
        self.neighbor_visitable[neighbor] = False
        
    def connect_to(self, neighbor):
        self.neighbor_visitable[neighbor] = True
        
    def set_edge_point_pairs(self):
        #creates pairs of points for walls/edges to use in generating
        p1 = Point(self.real_coords[0], self.real_coords[1])
        p2 = Point(self.real_coords[0] + self.size, self.real_coords[1])
        p3 = Point(self.real_coords[0] + self.size, self.real_coords[1]  + self.size)
        p4 = Point(self.real_coords[0], self.real_coords[1]  + self.size)
        top = (p1, p2)
        right = (p2, p3)
        bottom = (p3, p4)
        left = (p4, p1)
        self.point_pairs = [top, right, bottom, left]

    def add_edge(self, edge_number, edge):
        #adds an edge
        self.edges_list.append(edge)
        self.edges[edge_number] = edge
        
    def create_edges(self):
        #generates edges. done to every second tile. tiles share edge objects with neighbors
        edges = []
        self.set_edge_point_pairs()
        for i in range(4):
            point_pair = self.point_pairs[i]
            neighbor = self.neighbors_directed[i]
            if neighbor != None:
                edge = Edge(point_pair, self.win, self, neighbor, self.size)
                self.neighbor_edge_dict[neighbor] = edge
                self.add_edge(i, edge)
                neighbor.add_edge(((i+2)%4), edge)
                neighbor.neighbor_edge_dict[self] = edge
                edges.append(edge)
        return edges
            
    def update_neighbors(self):
        for neighbor in self.neighbors_directed:
            if neighbor != None:
                self.neighbors.append(neighbor)
                self.neighbor_visitable[neighbor] = True


    def set_neighbor(self, position, tile):
        self.neighbors_directed[position] = tile

    def set_shape(self):
        p1 = Point(self.real_coords[0], self.real_coords[1])
        p2 = Point(self.real_coords[0] + self.size, self.real_coords[1] + self.size)
        self.shape = Rectangle(p1, p2)
        self.shape.setFill(tile_color)
        self.shape.setWidth(0)

    def set_center_coords(self):
        #gets pixel coordinates (for graphic objects) of center of tile. 
        x = self.real_coords[0] + self.size/2
        y = self.real_coords[1] + self.size/2
        self.center_coords = (x, y)

    def draw(self):
        self.shape.draw(self.win)
        
    def color(self, color):
        self.shape.setFill(color)

    def set_real_coords(self):
        self.real_coords = (self.coords[0] * self.size, ((self.maze_length-1)-self.coords[1]) * self.size)


