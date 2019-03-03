from random import random
class Link:
    def __init__(self, in_node, out_node, weight, innovation):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.innovation = innovation
        self.enable = True

    def mutate(self):
        self.weight = random()

