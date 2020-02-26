"""Generate and evaluate new patterns and names."""
import geometry
import itertools
import numpy as np


class Generator:

    def __init__(self, nodes, num_edges=10):
        self.vertex_nodes = nodes
        self.node_keys = []

        for i in self.vertex_nodes.keys():
            self.node_keys.append(i)

        self.num_edges = num_edges
        self.used_vertices = []
        self.pattern = []

    # Genetic algorithm for generating a new pattern
    def generate_pattern(self, num_candidates=10, min_fitness=30):
        # Initialize an empty array of the correct format and size. The first
        # value of each index corresponds to that path's fitness score
        candidates = [[0, [() for i in range(self.num_edges + 1)]] for i in range(num_candidates)]

        # Populate each index of candidates with a new random set of edges
        for i in range(num_candidates):
            random_pattern = []
            for j in range(self.num_edges):
                random_pattern.append((np.random.choice(self.node_keys, 1)[0], np.random.choice(self.node_keys, 1)[0]))

            candidates[i][1:] = random_pattern

        # Evaluate the fitness of each initial random path
        for i in range(num_candidates):
            candidates[i][0] = self._evaluate_pattern(candidates[i][1:])

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

        self.pattern = candidates[0][1:]
        return self.pattern

    # Calculate the fitness score of a given path
    # TODO: Create more metrics, tune the existing metrics
    def _evaluate_pattern(self, pattern):
        score = 0

        # Evaluate edge distances
        for i in range(len(pattern)):
            difference = geometry.distance(
                self.vertex_nodes.get(pattern[i][0]),
                self.vertex_nodes.get(pattern[i][1]))
            if difference == 0:
                score = score + 0
            elif 0 < difference <= 200:
                score = score + 1
            elif 200 < difference <= 400:
                score = score + 1
            elif 400 < difference <= 600:
                score = score + 2
            elif 600 < difference <= 800:
                score = score + 1
            elif 800 < difference <= 1000:
                score = score + 1
            else:
                score = score + 0

        # Evaluate interceptions
        for i, j in itertools.combinations(pattern, 2):
            if geometry.has_intersection(self.vertex_nodes.get(i[0]), self.vertex_nodes.get(i[1]), self.vertex_nodes.get(j[0]), self.vertex_nodes.get(j[1])):
                score = 0
            else:
                score = score + 1

        return score

    # Mutate a new pattern from the existing patterns
    def _mutate_pattern(self, candidates):
        # Initialize a new array with 0 being the first element
        mutated = [0]

        # Populate mutated with a new random path
        for i in range(self.num_edges):
            mutated.append((np.random.choice(self.node_keys, 1)[0], np.random.choice(self.node_keys, 1)[0]))

        # Evaluate the fitness of the new path and return the top 10 candidates
        mutated[0] = self._evaluate_pattern(mutated[1:])
        candidates.append(mutated)
        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[:10]
