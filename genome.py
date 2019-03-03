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
        self.innov_counter = 0
        for inode in self.input_nodes:
            for onode in self.output_nodes:
                weight = random()
                connection = Link(inode, onode, weight, self.innov_counter)
                self.connections.append(connection)
                inode.add_outgoing(connection)
                onode.add_incoming(connection)
                self.innov_counter += 1
    
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
        weight = random()
        new_link = Link(inode, onode, weight, innov_number)
        innov_number += 1
        inode.add_outgoing(new_link)
        onode.add_incoming(new_link)
        self.connections.append(new_link)
        return innov_number
    
    def mutate_add_node(self, innov_number):
        # find random link
        link = choice(self.connections)
        # create new node
        bias = random()
        node = Node(NodeType.HIDDEN, bias)
        # create 2 new links
        weight = random()
        link1 = Link(link.in_node, node, weight, innov_number)
        innov_number += 1
        link.in_node.add_outgoing(link1)
        node.add_incoming(link1)
        weight = random()
        link2 = Link(node, link.out_node, weight, innov_number)
        node.add_outgoing(link2)
        link.out_node.add_incoming(link2)
        innov_number += 1
        self.connections += [link1, link2]
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
                