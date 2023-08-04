from graphics import *
from colors import *

class GoalMarker:
    def __init__(self, size, win, coords):
        #simply a red X
        self.size = size
        self.win = win
        self.coords = coords
        self.scale_factor = 0.8
        self.make_shape()
       
    
    def make_shape(self):
        p1 = Point(self.coords[0]-0.25*self.size, self.coords[1]-0.25*self.size)
        p2 = Point(self.coords[0]+0.25*self.size, self.coords[1]-0.25*self.size)
        p3 = Point(self.coords[0]+0.25*self.size, self.coords[1]+0.25*self.size)
        p4 = Point(self.coords[0]-0.25*self.size, self.coords[1]+0.25*self.size)
        circles = []
        for point in [p1,p2,p3,p4]:
            circle = Circle(point, 0.1*self.scale_factor*self.size)
            circle.setFill(goal_marker_color)
            circle.setWidth(0)
            circles.append(circle)
            
        line1 = Line(p1, p3)
        line2 = Line(p2, p4)
        lines = [line1, line2]
        for line in lines:
            line.setOutline(goal_marker_color)
            line.setWidth(0.2*self.scale_factor*self.size)
        self.shape = circles + lines

    def draw(self):
        for part in self.shape:
            part.draw(self.win)