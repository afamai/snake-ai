from node import *
from link import Link
import math
from random import choice, randint
import time
import copy
class Genome:
    connections = []
    def __init__(self, num_inputs = 0, num_outputs = 0):
        self.fitness_score = 0

        # create the input and output nodes
        self.hidden_nodes = []
        self.input_nodes = []
        self.node_number = 0
        for i in range(num_inputs):
            self.add_node(NodeType.INPUT, 0)

        self.output_nodes = []
        for i in range(num_outputs):
            self.add_node(NodeType.OUTPUT, 0)

        # create the links for a simple feedforward neural network
        self.connections = []
        for inode in self.input_nodes:
            for onode in self.output_nodes:
                self.add_link(inode, onode, random())

    def add_link(self, inode, onode, weight):
        # check to see if link already exist
        try:
            innov_number = Genome.connections.index((inode.id, onode.id))
        except:
            innov_number = len(Genome.connections)
            Genome.connections.append((inode.id, onode.id))
        
        link = Link(inode, onode, weight, innov_number)
        inode.add_outgoing(link)
        onode.add_incoming(link)
        self.connections.append(link)
    
    def add_node(self, node_type, bias):
        node = Node(node_type, bias, self.node_number)
        if node_type == NodeType.INPUT:
            self.input_nodes.append(node)
        elif node_type == NodeType.OUTPUT:
            self.output_nodes.append(node)
        elif node_type == NodeType.HIDDEN:
            self.hidden_nodes.append(node)
        self.node_number += 1
        return node
    
    def mutate_add_link(self):
        possible_outputs = self.hidden_nodes + self.output_nodes
        onode = choice(possible_outputs)
        possible_inputs = possible_outputs + self.input_nodes
        inode = choice(possible_inputs)

        # make sure that a duplicate connection is not already created
        for link in self.connections:
            if link.in_node == inode and link.out_node == onode:
                link.enable = True
                return
        
        # ensure that both nodes are not output nodes
        if onode in self.output_nodes and inode in self.output_nodes:
            return

        # make sure that the 2 nodes are not the same
        if onode == inode:
            return
        
        # Allow recurrent links for now
        # create new connection
        self.add_link(inode, onode, random())
    
    def mutate_add_node(self):
        # find random link
        link = choice(self.connections)
        # create new node
        node = self.add_node(NodeType.HIDDEN, random())
        # create 2 new links
        self.add_link(link.in_node, node, random())
        self.add_link(node, link.out_node, random())
        # disable the original link
        link.enable = False
    
    @staticmethod
    def single_point_crossover(genome1, genome2):
        # find all matching genes
        g1_innov = set(map(lambda link: link.innovation, genome1.connections))
        g2_innov = set(map(lambda link: link.innovation, genome2.connections))

        matching = g1_innov & g2_innov

        # select a random point
        rand_point = randint(0, len(matching))

        # perform cross over on matching genes
        g1_matching_genes = list(filter(lambda link: link.innovation in matching, genome1.connections))
        g2_matching_genes = list(filter(lambda link: link.innovation in matching, genome2.connections))
        genes = copy.deepcopy(g1_matching_genes[:rand_point])
        genes += copy.deepcopy(g2_matching_genes[rand_point:])

        # determine which parent is the better one
        if genome1.fitness_score == genome2.fitness_score:
            # add both parents disjoint and excess genes
            genes += list(filter(lambda link: link.innovation not in matching, genome1.connections + genome2.connections))
        else:
            # add only the better parent's disjoin and excess genes
            if genome1.fitness_score > genome2.fitness_score:
                genes += list(filter(lambda link: link.innovation not in matching, genome1.connections))
            else:
                genes += list(filter(lambda link: link.innovation not in matching, genome2.connections))

        # create new Genome
        new_genome = Genome()
        new_genome.connections = genes

        # set the input, hidden and output nodes for the new Genome
        all_nodes = []
        for link in genes:
            all_nodes += [link.in_node, link.out_node]
        # remove all duplicate nodes
        all_nodes = list(set(all_nodes))
        # place all the nodes in their respected type
        for node in all_nodes:
            if node.type == NodeType.INPUT:
                new_genome.input_nodes.append(node)
            elif node.type == NodeType.OUTPUT:
                new_genome.output_nodes.append(node)
            elif node.pty == NodeType.HIDDEN:
                new_genome.hidden_nodes.append(node)

        return new_genome

    def activate(self, inputs):
        # pass inputs into input nodes
        for idx, inode in enumerate(self.input_nodes):
            inode.active_sum = inputs[idx]

        nodes = self.hidden_nodes + self.output_nodes
        complete = False
        # TODO: maybe a do while loop?
        while not complete:
            complete = True
            for node in nodes:
                active_sum = 0
                for link in node.incoming:
                    # the in_node within the link must be active first
                    if link.enable:
                        if link.in_node.active_flag or link.in_node.type == NodeType.INPUT:
                            active_sum += link.weight * link.in_node.active_sum
                        else:
                            complete = False
                            break
                if not complete:
                    continue
                if node.type != NodeType.OUTPUT:
                    active_sum += node.bias
                # pass the sum through activation function (sigmoid)
                node.active_sum = 1 / (1 + math.exp(-active_sum))
                node.active_flag = True
        for node in nodes:
            node.active_flag = False
        return list(map(lambda node: node.active_sum, self.output_nodes))
                