# Genetic Algorithm
# Michael Peres
# 5/11/23
import timeit
from functools import partial
# Imports
from typing import List, Callable, Tuple
import math
import hashlib
import string
import random
from password_fitness import get_normalised_fitness, MAX_VALUE, distance_function


# 1) We need to find out how to represent the problem as a genome.
# Luckily a fitness function is already provided for us.
Genome = str
Population = List[Genome]
STUDENT_PASSWORD = "H4QL2HDL9J"
OPTIONS = string.digits + string.ascii_uppercase + "_"

def generate_genome(length: int) -> Genome:
	"""Function to generate a random genome of length k."""

	return ''.join(random.choices(OPTIONS, k=length))


def generate_population(population_size: int, genome_length: int=10) -> Population:
	"""Function to generate a population of genomes of size n."""
	return [generate_genome(genome_length) for _ in range(population_size)]


# Fitness Function is luckily already provided for us.
def fitness_function(genome: Genome) -> int:
	"""Function to determine the fitness of a genome."""
	fitness = 1 - distance_function(genome, STUDENT_PASSWORD) / MAX_VALUE
	# print("fitness", fitness)
	return fitness


def selection_pair(population: Population, fitness_func: Callable[[Genome], int]) -> Population:
	"""Function to select two genomes from the population, based on their fitness."""
	return random.choices(
		population=population,
		weights=[fitness_func(genome) for genome in population],
		k=2
	)


def single_point_crossover(a: Genome, b: Genome) -> tuple[Genome, Genome]:
	"""We want to take a random slice of the genome so we can make the children"""
	# Make sure the genomes are at least of length 2 to be able to perform cross over,
	# Make sure both genome are of the same length.
	if len(a) != len(b):
		raise("Genomes are of different lengths or length is less than 2")
	if len(a) < 2:
		return a, b  # just return parents.
	split_index = random.randint(1,len(a)-1)  # A value between 1 and p-1
	child_1 = a[:split_index]+b[split_index:]
	child_2 = b[:split_index]+a[split_index:]
	return child_1, child_2


def mutation(genome:Genome, num:int=1, probability:float = 0.5) -> Genome:
	"""

	:param genome: Genome in Qquestion
	:param num: Number of mutations to genome.
	:param probability: Probability of changing genome.
	:return: A new genome.
	"""
	genome = [char for char in genome]
	for _ in range(num):
		index = random.randrange(len(genome))
		genome[index] = genome[index] if random.random() > probability else random.choice(OPTIONS)  # We flipped a bit.
	genome = ''.join(genome)
	return genome


def run_evolution(
		populate_func,
		fitness_func: Callable[[Genome], int],
		fitness_limit: int=MAX_VALUE,  # Termination Condition.
		selection_func = selection_pair,
		crossover_func = single_point_crossover,
		mutation_func = mutation,
		generation_limit: int = 100   # Make generation iterations before fitness is determined.
) -> Tuple[Population, int]:

	population = populate_func()  # Get population

	# Loop for generation limit times
	for i in range(generation_limit):
		if i % 10 == 0:
			print(f"Generation {i} | Best Solution: {population[0]} | Fitness: {fitness_function(population[0])}")
		population = sorted(
			population,
			key = lambda genome: fitness_func(genome),
			reverse=True
		)
		if fitness_func(population[0]) >= fitness_limit or fitness_func(population[0]) == 0:
			break

		next_generation = population[:2]  # Top 2 genomes from population

		# Generate all other solutions for our next generation. Already have 2 top solutions, save loops.
		for j in range(int(len(population) / 2) -1):
			parents = selection_func(population, fitness_func)  # Select to random parents based on fitness function.
			offspring_a, offspring_b = crossover_func(parents[0], parents[1])  # We will have offspring from the parents.
			# In order to expand the variety of solutions we have, we use the variation function.
			offspring_a = mutation_func(offspring_a)
			offspring_b = mutation_func(offspring_b)
			next_generation += [offspring_a, offspring_b]

		population = next_generation  # the new population will include top 2 parents and 98 offspring from the parents.


	# Lastly we can return the population sorted.
	population = sorted(
		population,
		key=lambda genome: fitness_func(genome),
		reverse=True
	)
	return population, i


if __name__ == "__main__":
	# start = timeit.timeit()
	# population = generate_population(10)
	# selection = selection_pair(population, distance_function)
	# print("selection", selection)

	print("Running Genetic Algorithm")
	start = timeit.timeit()
	population, generations = run_evolution(
		populate_func=partial(
			generate_population, population_size=10000
		),
		fitness_func=fitness_function,
		fitness_limit=MAX_VALUE,
		generation_limit=500
	)
	end = timeit.timeit()
	print(f"Generations: {generations}")
	print(f"Best Solution: {population[0]}")
	print("Solution Timing: ", end - start, " seconds")