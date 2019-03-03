from node import *
from link import Link
import math
class Genome:
    def __init__(self, num_inputs, num_outputs):
        # create the input and output nodes
        self.nodes = []
        self.input_nodes = []
        for i in range(num_inputs):
            node = Node(NodeType.INPUT, 0)
            self.nodes.append(node)
            self.input_nodes.append(node)
            print('creating input node: ', i)

        self.output_nodes = []
        for i in range(num_outputs):
            node = Node(NodeType.OUTPUT, 0)
            self.nodes.append(node)
            self.output_nodes.append(node)
            print('creating output node:', i)

        
        # create the links for a simple feedforward neural network
        self.connections = []
        self.innov_counter = 0
        for i in range(num_inputs):
            for j in range(num_inputs, num_inputs + num_outputs):
                weight = random()
                inode = self.nodes[i]
                onode = self.nodes[j]
                connection = Link(inode, onode, weight, self.innov_counter)
                self.connections.append(connection)
                inode.add_outgoing(connection)
                onode.add_incoming(connection)
                self.innov_counter += 1
        print(self.connections)

    def activate(self, inputs):
        # pass inputs into input nodes
        for idx, inode in enumerate(self.input_nodes):
            inode.active_sum = inputs[idx]

        complete = False
        # TODO: maybe a do while loop?
        while not complete:
            complete = True
            for node in self.nodes:
                if node.type != NodeType.INPUT:
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

        for node in self.nodes:
            node.active_flag = False
        
        return list(map(lambda node: node.active_sum, self.output_nodes))
                