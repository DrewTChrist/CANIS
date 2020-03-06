"""Generate and evaluate new patterns and names."""

import itertools
import networkx as nx
import numpy as np
from constellation import ConstellationBuilder
from geometry import distance
from neuralnet import Evaluator


class Generator:

    def __init__(self, ip):
        # ImageProcessor object containing graph and node data
        self.ip = ip

        # An array of each key in nodes
        self.node_keys = []
        for i in self.ip.nodes.keys():
            self.node_keys.append(i)

        # Semi-supervised neural network for generated pattern evaluation
        self.evaluator = Evaluator("pattern_eval.h5")

        # The final generated pattern
        self.pattern = []

        # An array of raw coordinates to stars used in the generated pattern
        self.used_vertices = []

    def _get_dividing_factor(self, total):
        # The range 5 to 20 constrains the number of nodes to be selected
        return int(total / np.random.randint(5, 20)) + 1

    def _next_pattern(self, gen_type="subset"):
        graph_copy = self.ip.graph

        # Utilize the full set of stars resulting in the same pattern after
        # each generation for a given image
        if gen_type == "full":
            for j, k in itertools.combinations(self.ip.nodes.keys(), 2):
                graph_copy.add_edge(j, k, weight=distance(self.ip.nodes[j], self.ip.nodes[k]))

        # Randomly choose a subset of stars resulting in a different pattern
        # after each generation
        elif gen_type == "subset":
            key_len = len(self.ip.nodes.keys())
            subset = list(np.random.choice(range(1, key_len + 1), int(key_len / self._get_dividing_factor(key_len)), replace=False))
            for j, k in itertools.combinations(subset, 2):
                graph_copy.add_edge(j, k, weight=distance(self.ip.nodes[j], self.ip.nodes[k]))

        return list(nx.minimum_spanning_edges(graph_copy, data=False))

    def _mutate_pattern(self, candidate):
        # TODO: Random chance to add a cycle to a pattern.
        # TODO: Random chance to reduce edges to a node from 4 to 3.
        return 0

    def generate_pattern(self, gen_type="subset", mode="off"):
        # Start with a new generation. While the evaluator returns True,
        # continue generating new patterns.
        candidate = self._next_pattern(gen_type)

        while not self._evaluate_pattern(candidate, mode):
            candidate = self._next_pattern(gen_type)

        self.pattern = candidate

        node_list = []
        for edge in self.pattern:
            for node in edge:
                if node not in node_list:
                    node_list.append(node)
                    self.used_vertices.append(self.ip.nodes[node])

        return self.pattern

    def _evaluate_pattern(self, pattern, mode="off"):
        # Utilize a semi-supervised neural network to determine if a pattern is
        # allowed to be used or not. Evaluation is disabled when mode="off"
        constellation = ConstellationBuilder(self.ip.processed, self.ip.graph, self.ip.nodes)
        constellation.add_edges(pattern)

        if mode == "off":
            return True
        elif mode == "predict":
            # Plot the current pattern, convert the plot to an array, and feed
            # the result to the evaluator for approval
            if self.evaluator.predict(constellation.visualize(to_array=True)) > 0.6:
                return True
            else:
                return False
        elif mode == "train":
            # Do some training stuff here
            return True
