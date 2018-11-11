from tsp_solver.greedy import solve_tsp
from classes import *

map_ = Map('../data/City_Coordinates.txt')
walk = Walk("_".join(list(map(str, solve_tsp(map_.matrix)))), map_)
print(walk.length)
print(len(walk.route.split('_')))