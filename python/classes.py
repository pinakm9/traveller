import numpy as np
from time import time
import random

# Timing wrapper
def timer(func):
	def new_func(*args,**kwargs):
		start = time()
		val = func(*args,**kwargs)
		end = time()
		duration = end-start
		print('Time taken by function {} is {} seconds'.format(func.__name__, duration))
		return val, duration
	return new_func

class City(object):
	"""
	Id refers to its id in the map, coords is a 2D vector
	"""
	def __init__(self, coords):
			self.coords = np.array(coords)

	def __sub__(self, other):
		difference = self.coords - other.coords
		return np.linalg.norm(difference)

class Reader(object):
	"""
	Reader object for reading city coordinates from a file
	"""
	def __init__(self, file):
		self.file = file
		self.city_dict = []
		with open(self.file, 'r') as cities:
			for line in cities:
				self.city_dict.append(City(list(map(float, line.split(',')))))

class Map(Reader):
	"""
	Creates map of the cities from coordinates file
	"""
	def __init__(self, file):
		super().__init__(file)
		self.best_path_length = 'nan'
		self.num_cities = len(self.city_dict)
		self.matrix  = [] # triangular distance matrix
		for i in range(self.num_cities):
			self.matrix.append([ self.city_dict[i]-self.city_dict[j] for j in range(i) ])

class Walk(object):

	def __init__(self, route, map_, sep = '_'):
		self.length = 0
		self.route = route
		ids = list(map(int, route.split(sep)))
		for i, id_ in enumerate(ids):
			ma, mi = max(id_, ids[i-1]), min(id_, ids[i-1])
			self.length += map_.matrix[ma][mi]
		#self.reproduction_score = 0
		self.is_hamiltonian = len(ids) == map_.num_cities

	def __lt__(self, other):
		return self.length < other.length

	 
class Traveller(object):

	def __init__(self, map_, sep = '_'):
		self.map = map_
		self.num_cities = map_.num_cities
		self.sep = sep
	
	def walk(self):
		return Walk(self.sep.join(list(map(str, np.random.permutation(self.map.num_cities)))), self.map, self.sep)

	def generate_initial_routes(self, num_routes):
		self.routes = []
		self.max_routes = num_routes
		for n in range(num_routes):
			self.routes.append(self.walk())
		self.routes.sort()
		self.map.best_path_length = self.routes[0].length

	def generate_next_routes(self, mating_pool_size, crossover, mutation, mutation_prob, elitism = True):
		new_routes = []
		# Select pairs for mating
		if elitism is True:
			pool = np.array(self.routes[:mating_pool_size]).reshape(-1, 2)
		else:
			pool = np.array(random.sample(self.routes, mating_pool_size)).reshape(-1, 2)
		for pair in pool:
			route1, route2 = crossover(pair[0].route, pair[1].route, self.sep)
			route1, route2 = mutation(route1, self.sep, mutation_prob), mutation(route1, self.sep, mutation_prob)
			new_routes += [Walk(route1, self.map, self.sep), Walk(route2, self.map, self.sep)]
			self.routes += new_routes
			self.routes.sort()
			self.routes = self.routes[:self.max_routes]
		self.map.best_path_length = self.routes[0].length

	@timer
	def search(self, num_routes, mating_pool_size, crossover, mutation, mutation_prob, elitism = True, stagnation_threshold = 100,\
	           improvement_threshold = 1e-6):
		self.generate_initial_routes(num_routes)
		length = self.map.best_path_length
		improvement, stagnation_period, itr = 1, 0, 0
		while stagnation_period < stagnation_threshold:
			self.generate_next_routes(mating_pool_size, crossover, mutation, mutation_prob, elitism)
			improvement = 1 - self.map.best_path_length/length
			if improvement < improvement_threshold:
				stagnation_period += 1
			else:
				stagnation_period = 0
			length = self.map.best_path_length
			itr += 1
			print('Length of best Hamiltonian cycle at generation {} is {:.5f}'.format(itr, length), end = "\r")
		print('\nPopulation has reached stagnation.')
		return self.routes[0], length, itr

	@timer
	def test(self, num_routes, mating_pool_size, crossover, mutation, mutation_prob, elitism = True, stagnation_threshold = 100,\
	           improvement_threshold = 1e-6, num_trials = 10, log = False, file_path = ''):
		print('{0}\nSearching with crossover = {1} and {2} elitism\n{0}'.format('#'*60, crossover.__name__, 'with' if elitism else 'without'))
		avg = lambda x: sum(x)/float(len(x))
		durs, lens, itrs, truth = [0]*num_trials, [0]*num_trials, [0]*num_trials, [0]*num_trials
		for i in range(num_trials):
			print('Trial #{}'.format(i+1))
			res, dur = self.search(num_routes, mating_pool_size, crossover, mutation, mutation_prob, elitism, stagnation_threshold,\
	           improvement_threshold)
			durs[i] = dur
			lens[i] = res[1]
			itrs[i] = res[2]
			truth[i] = res[0].is_hamiltonian
		print('Average best length = {:.4f} units'.format(avg(lens)))
		print('Average time taken = {:.4f} seconds'.format(avg(durs)))
		print('Average number of generations = {:.4f}'.format(avg(itrs)))
		print('All solutions are {}'.format('not correct' if avg(truth) < 1 else 'correct'))
		if log is True:
			with open(file_path, 'a+') as file:
				file.write('{}{}{:.2f}{}{:.2f}{}{:.2f}{}{}\n'\
					.format(crossover.__name__.ljust(16), ' '*2, avg(lens), ' '*10, avg(durs), ' '*12, avg(itrs), ' '*16, 'Yes' if elitism else 'No'))