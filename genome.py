from node import *
from link import Link
import math
from random import choice
class Genome:
    def __init__(self, num_inputs, num_outputs):
        # create the input and output nodes
        self.hidden_nodes = []
        self.input_nodes = []
        for i in range(num_inputs):
            self.input_nodes.append(Node(NodeType.INPUT, 0))

        self.output_nodes = []
        for i in range(num_outputs):
            self.output_nodes.append(Node(NodeType.OUTPUT, 0))

        # create the links for a simple feedforward neural network
        self.connections = []
        innov_counter = 0
        for inode in self.input_nodes:
            for onode in self.output_nodes:
                innov_counter = self.add_connection(inode, onode, random(), innov_counter)

    def add_connection(self, inode, onode, weight, innov_number):
        link = Link(inode, onode, weight, innov_number)
        inode.add_outgoing(link)
        onode.add_incoming(link)
        self.connections.append(link)
        return innov_number + 1
    
    def mutate_add_link(self, innov_number):
        possible_outputs = self.hidden_nodes + self.output_nodes
        onode = choice(possible_outputs)
        possible_inputs = possible_outputs + self.input_nodes
        inode = choice(possible_inputs)

        # make sure the connection does not exist
        for link in self.connections:
            if link.in_node == inode and link.out_node == onode:
                return False
        
        # ensure that both nodes are not output nodes
        if onode in self.output_nodes and inode in self.output_nodes:
            return False
        
        # Allow recurrent links for now
        # create new connection
        return self.add_connection(inode, onode, random(), innov_number)
    
    def mutate_add_node(self, innov_number):
        # find random link
        link = choice(self.connections)
        # create new node
        bias = random()
        node = Node(NodeType.HIDDEN, bias)
        # create 2 new links
        innov_number = self.add_connection(link.in_node, node, random(), innov_number)
        innov_number = self.add_connection(node, link.out_node, random(), innov_number)
        # disable the original link
        link.enable = False
        return innov_number

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
                