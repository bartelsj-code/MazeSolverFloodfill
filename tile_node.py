from variables_to_change import *

class TileNode:
    def __init__(self, coords):
        self.coords = coords
        self.value = "*"
        self.neighbors = []

    def block_node(self, node):
        #disconnects a node from its previous neighbor
        if node in self.neighbors:
            self.neighbors.remove(node)
        if self in node.neighbors:
            node.neighbors.remove(self)

    def __repr__(self):
        string = "<{}>".format(self.value)
        return string
    
    def set_value(self, value):
        self.value = value

    def set_start_value(self):
        #sets a node to its starting value based on neighbor values
        lowest = 10000000000
        for neighbor in self.neighbors:  
            if neighbor.value != "*":
                lowest = min(lowest, neighbor.value)
        self.set_value(lowest + 1)
        
    def flood_update_value(self):
        #set own value of self to one greater than the value of the lowest still connected neighbor
        if self.value == 0:
            return False
        lowest = 100000
        for neighbor in self.neighbors:
            if neighbor.value < self.value:
                return False
            lowest = min(neighbor.value, lowest)
        self.value = lowest + 1
        return True

    


