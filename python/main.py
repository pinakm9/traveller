from classes import *
from dna import *

# Initialize variables
map_ = Map('../data/City_Coordinates.txt')
salesman = Traveller(map_)
crossovers = [modified, cycle, order, order_based, position_based, partially_mapped]
file_path = '../results/results_demo.txt'
with open(file_path, 'w') as file:
	file.write('crossover{0}avg best length{0}avg time(s){0}avg no of generations{0}elitism\n{1}\n'.format(' '*4, '_'*80))
max_pop = 300
mating_pool_size = 200
mutation_probability = 0.07
num_trials = 1
# Test crossover operators
for crossover in crossovers:
	salesman.test(max_pop, mating_pool_size, crossover, lambda x, y, z: two_opt(x, map_, y, z), mutation_probability,\
	 elitism = True, num_trials = num_trials, log = True, file_path = file_path)
	salesman.test(max_pop, mating_pool_size, crossover, lambda x, y, z: two_opt(x, map_, y, z), mutation_probability,\
	 elitism = False, num_trials = num_trials, log = True, file_path = file_path)
