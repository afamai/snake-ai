from genome import Genome
import numpy as np
from operator import itemgetter
from random import randint, choice
class Population:
    def __init__(self, size, inputs, outputs):
        self.size = size
        self.genomes = []
        for i in range(size):
            self.genomes.append(Genome(inputs, outputs))

    def get_best(self):
        fitness = [(i, genome.fitness_score) for i, genome in enumerate(self.genomes)]
        fitness.sort(key=itemgetter(1), reverse=True)
        return self.genomes[fitness[0][0]]

    def mean_fitness_score(self):
        # get all fitness scores as a list
        fitness = list(map(lambda genome: genome.fitness_score, self.genomes))
        # find the max fitness score
        max_fitness = 1 if max(fitness) == 0 else max(fitness)
        # normalize all the fitness scores
        fitness = list(map(lambda x: x/max_fitness, fitness))
        # calculate the mean
        try:
            return np.mean(fitness)
        except:
            return 0
    
    def generate_new_generation(self):
        # == selection ==
        fitness = [(i, genome.fitness_score) for i, genome in enumerate(self.genomes)]
        fitness.sort(key=itemgetter(1), reverse=True)
        top = 5
        best = [ i for i, s in fitness[:top]]
        new_genomes = []
        # crossover
        for i in range(self.size):
            # select 2 random parents
            parent1 = choice(best)
            parent2 = choice(best)
            while parent1 == parent2:
                parent2 = choice(best)
            
            new_genome = Genome.single_point_crossover(self.genomes[parent1], self.genomes[parent2])
            # mutations
            new_genome.mutate()
            # print(len(new_genome.input_nodes))
            new_genomes.append(new_genome)
        
        self.genomes = new_genomes