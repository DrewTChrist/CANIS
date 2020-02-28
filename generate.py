"""Generate and evaluate new patterns and names."""
import geometry
import itertools
import networkx as nx
import numpy as np


class Generator:

    def __init__(self, graph, vertex_nodes):
        # Unconnected star graph
        self.G_empty = graph

        # Connected star graph
        self.G_populated = graph

        # Dictionary of the nodes
        self.nodes = vertex_nodes

        # An array of each key in nodes
        self.node_keys = []

        for i in self.nodes.keys():
            self.node_keys.append(i)

        # The generated pattern
        self.pattern = []

        # Currently not implemented, might be useful for comparison
        self.used_vertices = []

    def _get_dividing_factor(self, total):
        # The range 3 to 21 is used because real constellations have anywhere
        # from 3 to 20 edges
        return int(total / np.random.randint(3, 21))

    def generate_pattern(self, type="subset", num_candidates=10, min_fitness=0):
        # Initialize an empty array of the correct format and size. The first
        # value of each index corresponds to that path's fitness score
        candidates = []

        # Populate each index of candidates with a new random set of edges
        for i in range(num_candidates):
            G_copy = self.G_empty

            if type == "full":
                for j, k in itertools.combinations(self.nodes.keys(), 2):
                    G_copy.add_edge(j, k, weight=geometry.distance(self.nodes[j], self.nodes[k]))
            elif type == "subset":
                key_len = len(self.nodes.keys())
                subset = list(np.random.choice(range(1, key_len + 1), int(key_len / self._get_dividing_factor(key_len)), replace=False))
                for j, k in itertools.combinations(subset, 2):
                    G_copy.add_edge(j, k, weight=geometry.distance(self.nodes[j], self.nodes[k]))

            candidates.append([0, list(nx.minimum_spanning_edges(G_copy, data=False))])

        # TODO: Evaluate each candidate here when evaluate_pattern is fixed

        # Sort the paths by fitness and store the highest fitness score
        candidates.sort(reverse=True, key=lambda x: x[0])
        high_score = candidates[0][0]

        # Generation loop, continue mutating until we have an artefact that
        # exceeds the specified minimum fitness
        while high_score < min_fitness:
            candidates = self._mutate_pattern(candidates)
            high_score = candidates[0][0]
            # TODO: Make it an optional flag to print scores
            print(f'fitness={high_score}')

        self.pattern = candidates[0][1:][0]
        return self.pattern

    def _evaluate_pattern(self, pattern):
        # Calculate the fitness score of a given pattern
        # TODO: Start from scratch

        score = 0

        return np.random.randint(1, 11)

    # Mutate a new pattern from the existing patterns
    def _mutate_pattern(self, candidates):
        # Initialize a new array with 0 being the first element
        mutated = [0]

        # Populate mutated with a new random path
        for i in range(self.num_edges):
            mutated.append((np.random.choice(self.node_keys, 1)[0],
                            np.random.choice(self.node_keys, 1)[0]))

        # Evaluate the fitness of the new path and return the top 10 candidates
        mutated[0] = self._evaluate_pattern(mutated[1:])
        candidates.append(mutated)
        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[:10]
