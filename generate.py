"""Generate and evaluate new patterns and names."""
from random import randint


# Calculate the fitness score of a given pattern
def evaluate_pattern(pattern):
    # Fitness tests will go here, but a random score is assigned for now
    return randint(1, 100)


# Mutate a new pattern from the existing patterns, keep the best 10
def mutate_pattern(nodes, candidates):
    mutated = []

    for i in range(len(candidates)):
        for j in range(10):
            if randint(0, 101) > 50:
                mutated.append(candidates[randint(0, 9)][1])
            else:
                mutated.append((str(randint(1, len(nodes) + 1)),
                                str(randint(1, len(nodes) + 1))))

    score = evaluate_pattern(mutated)
    candidates.append([score, mutated])
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[0:10]


class Generator:

    def __init__(self, vertex_nodes):
        self.vertex_nodes = vertex_nodes
        self.used_vertices = []
        self.path = []

    # Genetic algorithm for generating a new pattern
    def generate_pattern(self, num_candidates=10, min_fitness=60):
        candidates = []

        for i in range(num_candidates):
            random_path = []
            for j in range(10):
                random_path.append((
                                   str(randint(1, len(self.vertex_nodes + 1))),
                                   str(randint(1,
                                               len(self.vertex_nodes + 1)))))

            candidates.append([0, random_path])

        for i in range(len(candidates)):
            candidates[i][0] = evaluate_pattern(candidates[i][1])

        candidates.sort(reverse=True, key=lambda x: x[0])
        high_score = candidates[0][0]

        while high_score < min_fitness:
            candidates = mutate_pattern(self.vertex_nodes, candidates)
            high_score = candidates[0][0]
        self.path = candidates[0][1]
        return self.path
