from enum import Enum
from random import random

class NodeType(Enum):
    INPUT = 0
    HIDDEN = 1
    OUTPUT = 2

class Node:
    def __init__(self, node_type, bias, node_id):
        self.id = node_id
        self.type = node_type
        self.bias = bias
        self.incoming = []
        self.outgoing = []
        self.active_flag = False
        self.active_sum = 0

    def mutate(self):
        self.bias = random()

    def add_incoming(self, link):
        self.incoming.append(link)

    def add_outgoing(self, link):
        self.outgoing.append(link)
