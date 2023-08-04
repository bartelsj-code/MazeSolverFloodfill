from graphics import *
from colors import *
from variables_to_change import *

class Edge:
    def __init__(self, points, win, tile1, tile2, size):
        #walls between maze tiles
        self.size_scaler = 1
        self.placed = False
        self.size = size
        self.tile1 = tile1
        self.tile2 = tile2
        self.tiles = [tile1, tile2]
        self.win = win
        self.points = points
        self.drawn = False
        self.make_shape()

    def place(self):
        #place down in maze
        self.placed = True
        self.tile1.disconnect_from(self.tile2)
        self.tile2.disconnect_from(self.tile1)
        self.draw()

    def remove(self):
        #remove from maze
        self.placed = False
        self.tile1.connect_to(self.tile2)
        self.tile2.connect_to(self.tile1)
        self.undraw()

    def make_shape(self):
        
        end1 = Circle(self.points[0],0.09*self.size_scaler*self.size)
        end1.setFill(edge_color)
        end1.setWidth(0)
        end2 = Circle(self.points[1],0.09*self.size_scaler*self.size)
        end2.setFill(edge_color)
        end2.setWidth(0)
        line = Line(self.points[0],self.points[1])
        line.setOutline(edge_color)
        line.setWidth(0.2*self.size_scaler*self.size)
        self.shape = [end1, end2, line]

    def undraw(self):
        if self.drawn:
            for part in self.shape:
                part.undraw()
            self.drawn = False

    def draw(self):
        if not self.drawn:
            for part in self.shape:
                part.draw(self.win)
            self.drawn = True
