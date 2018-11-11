from classes import *
from dna import *

map_ = Map('../data/City_Coordinates.txt')
salesman = Traveller(map_)
walk = salesman.search(200, 150, position_based, lambda x, y, z: two_opt(x, map_, y, z), 0.05)
print(len(walk.route.split('_')))
print(walk.is_hamiltonian)
print(walk.route)