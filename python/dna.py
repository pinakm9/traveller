import numpy as np
from classes import Walk
import copy
from random import sample 

def crossover_wrapper(crossover):
	
	def symmetric_crossover(*args, **kwargs):
		args = list(args)
		cross_pts, sep = None, None
		if len(args) == 2:
			chrom1, chrom2 = args
		elif len(args) == 3:
			chrom1, chrom2, sep = args
		elif len(args) == 4:
			chrom1, chrom2, sep, cross_pts = args
		chrom1, chrom2 = chrom1.split(sep), chrom2.split(sep)
		if cross_pts is None:
			cross_pts = np.random.choice(len(chrom1), 2, replace=False)
			cross_pts.sort()
		if sep is None:
			sep = crossover.__defaults__[0]
		child1 = crossover(chrom1, chrom2, sep, cross_pts)
		child2 = crossover(chrom2, chrom1, sep, cross_pts)
		return [child1, child2]

	return symmetric_crossover


@crossover_wrapper
def partially_mapped(chrom1, chrom2, sep = '_', cross_pts = [0, 0]):
	low, high = cross_pts
	child = copy.deepcopy(chrom2)
	child[low: high + 1] = chrom1[low: high + 1] 
	chars = set(chrom2[low: high + 1]) - set(chrom1[low: high + 1])
	for c in chars:
		ch = c
		while True:
			i = chrom2.index(ch)
			ch_ = chrom1[i]
			j = chrom2.index(ch_)
			if j >= low and j <= high:
				ch = ch_
			else:
				child[j] = c
				break
	return sep.join(child)

@crossover_wrapper
def order(chrom1, chrom2, sep = '_', cross_pts = [0, 0]):
	low, high = cross_pts
	j = high + 1 if low == 0 else 0 
	if j == len(chrom1):
		return sep.join(chrom1)
	cut = chrom1[low: high + 1]
	for ch in chrom2:
		if ch not in cut:		
			chrom1[j] = ch
			j += 1
			if j == low:
				j = high + 1
			if j == len(chrom1):
				return sep.join(chrom1)
	return sep.join(chrom1)

@crossover_wrapper
def order_based(chrom1, chrom2, sep = '_', cross_pts = [0, 0]):
	low, high = cross_pts
	part1 = sample(chrom1, low)
	child = ['?']*len(chrom1)
	indices = [chrom2.index(ch) for ch in part1]
	indices.sort()
	for i,j in enumerate(indices):
		child[j] = part1[i]
	idx = [0]*(len(chrom1)-low)
	j = 0
	for i in range(len(chrom1)):
		if i not in indices:
			idx[j] = i
			j += 1
	j = 0
	for ch in chrom2:
		if ch not in part1:
			child[idx[j]] = ch
			j += 1 
	return sep.join(child)

@crossover_wrapper
def position_based(chrom1, chrom2, sep = '_', cross_pts = [0, 0]):
	low, high = cross_pts
	indices = np.random.choice(len(chrom1), low, replace=False)
	chars, j = [chrom1[i] for i in indices], 0
	for ch in chrom2:
		if ch in chars:
			chrom1[indices[j]] = ch
			j += 1
	return sep.join(chrom1)


def swap(chrom, sep, probability):
	if np.random.rand() < probability:
		chrom = chrom.split(sep)
		i, j = np.random.choice(len(chrom), 2, replace=False)
		chrom[i], chrom[j] = chrom[j], chrom[i]
		return sep.join(chrom)
	else:
		return chrom

def two_opt(chrom, map_, sep, probability, max_itr = 50):
	if np.random.rand() < probability:
		length = Walk(chrom, map_, sep).length
		new_length, itr = length + 1, 0
		chrom_ = chrom.split(sep)
		while new_length > length and itr < max_itr:
			ints = np.random.choice(len(chrom_), 2, replace=False)
			i, j = min(ints), max(ints)	
			half1 = chrom_[i: j+1]
			half1.reverse() 
			half2 = chrom_[j+1:] + chrom_[:i]
			new_chrom = sep.join(half1 + half2)
			new_length = Walk(new_chrom, map_, sep).length
			itr += 1
		return new_chrom
	return chrom	

"""
c1 = '8 4 7 3 6 2 5 1 9 0'
c2 = '0 1 2 3 4 5 6 7 8 9'
print(pmx(c1, c2, ' ', [3,7]))
"""