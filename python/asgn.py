from classes import *
from dna import *

map_ = Map('../data/City_Coordinates.txt')
salesman = Traveller(map_)
walk = salesman.test(300, 200, modified, lambda x, y, z: two_opt(x, map_, y, z), 0.07)
