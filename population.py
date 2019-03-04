from genome import Genome
import numpy as np
class Population:
    def __init__(self, size, inputs, outputs):
        self.size = size
        self.genomes = []
        for i in range(size):
            self.genomes.append(Genome(inputs, outputs))

    def mean_fitness_score(self):
        # get all fitness scores as a list
        fitness = list(map(lambda genome: genome.fitness_score, self.genomes))
        print(fitness)
        # find the max fitness score
        max_fitness = 1 if max(fitness) == 0 else max(fitness)
        # normalize all the fitness scores
        fitness = list(map(lambda x: x/max_fitness, fitness))
        # calculate the mean
        try:
            return np.mean(fitness)
        except:
            return 0