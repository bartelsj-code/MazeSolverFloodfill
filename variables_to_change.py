# Graphics:
walls_vanish = False
path_highlighted = True
delay_before_walls_vanish = 3  #if they do
window_size = 950
fps = 20   #fps for mouse movement
show_best_found = True    #shows result of BFS (that is confined to explored squares)  
#(mouse may not always follow this even after optimal path is found because there may be multiple same distance paths)


# Mouse:
time_taken_per_step = 0.4 #inverse relation to speed of mouse. (0 is fine)
laps_to_take = 1000   #times the mouse will complete maze
print_floodfill_after_each_move = False   #small maze and very slow mouse advised
print_floodfill_grid_at_end_of_run = False  #makes more sense for smaller mazes



# Maze Generation
seed = "EmmaGamb"
maze_size = 40 #size of maze  (bigger than like 50 works but generation slowed by graphics library)
directness = 15  #the lower this is, the shorter the path  (must stay positive or 0)
wall_gaps = 50  #likelihood of gaps in walls: (inverse relationship: chance = 1/wall_gaps)
straightness = 3   #relates to how long paths try to follow one direction during generation, changes shape of maze a bit
path_num = 25   # number of paths (not solutions) to try to form during generation. (must be 1 or greater to guarantee solution exists, will break things if not)


