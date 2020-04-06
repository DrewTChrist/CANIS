"""Generate and evaluate new patterns and names."""
import itertools
import random
import networkx as nx
import numpy as np
import nltk
from modules.concept_query import ConceptInquirer
from nltk.corpus import wordnet as wn
from scipy.spatial.distance import euclidean


class PatternGenerator:

    def __init__(self, nodes):
        # A labelled dictionary of each star in the image
        self.all_nodes = nodes

        # An array of each key in all_nodes
        self.node_keys = []
        for i in self.all_nodes.keys():
            self.node_keys.append(i)

        # An array of raw coordinates to only the nodes that the pattern uses
        self.s_vertices = []

        self.s_nodes = {}

        # The final generated pattern
        self.pattern = []

        # Revisit when ready to implement the neural network.
        # Semi-supervised neural network for generated pattern evaluation
        # self.evaluator = Evaluator("pattern_eval.h5")

    def generate_pattern(self, gen_type="subset", mode="off"):
        candidate = self._mst_pattern(gen_type)

        for i in range(2):
            if np.random.uniform(0, 1) > 0.5:
                edge = self._get_cycle(candidate)

                if edge is not None:
                    candidate.append(edge)

        self.pattern = candidate

        # Revisit when ready to implement the neural network.
        # while not self._evaluate_pattern(candidate, mode):
        #    candidate = self._next_pattern(gen_type)

        node_list = []
        for edge in self.pattern:
            for node in edge:
                if node not in node_list:
                    node_list.append(node)
                    self.s_vertices.append(self.all_nodes[node])

        self.s_nodes = {k: v for k, v in self.all_nodes.items() if k in node_list}

    def _mst_pattern(self, gen_type="subset"):
        graph = nx.Graph()

        # Utilize the full set of stars resulting in the same pattern after
        # each generation for a given image
        if gen_type == "full":
            for i, j in itertools.combinations(self.node_keys, 2):
                graph.add_edge(i, j, weight=euclidean(self.all_nodes[i], self.all_nodes[j]))

        # Randomly choose a subset of stars resulting in a different pattern
        # after each generation
        elif gen_type == "subset":
            subset = list(np.random.choice(range(1, len(self.node_keys)), np.random.randint(5, 15), replace=False))
            for i, j in itertools.combinations(subset, 2):
                graph.add_edge(i, j, weight=euclidean(self.all_nodes[i], self.all_nodes[j]))

        return list(nx.minimum_spanning_edges(graph, data=False))

    def _get_cycle(self, candidate):
        node_list = []
        for edge in candidate:
            for node in edge:
                if node not in node_list:
                    node_list.append(node)

        np.random.shuffle(node_list)

        for i, j in itertools.combinations(node_list, 2):
            angle, intersection = False, False
            A, B = self.all_nodes[i], self.all_nodes[j]

            for edge in candidate:
                C, D = self.all_nodes[edge[0]], self.all_nodes[edge[1]]
                intersection = self._intersection(A, B, C, D)
                angle = self._angle(A, B, C, D)

            if angle == False and intersection == False:
                return i, j

    # Credit: https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    # Return true if line segments AB and CD intersect
    def _intersection(self, A, B, C, D):
        return self._ccw(A, C, D) != self._ccw(B, C, D) and self._ccw(A, B, C) != self._ccw(A, B, D)

    # Determine if A, B, C are oriented counterclockwise
    def _ccw(self, A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    def _angle(self, A, B, C, D):
        vector1 = [(A[0] - B[0]), (A[1] - B[1])]
        vector2 = [(C[0] - D[0]), (C[1] - D[1])]
        vector1 /= np.sqrt((np.power(vector1[0], 2) + np.power(vector1[1], 2)))
        vector2 /= np.sqrt((np.power(vector2[0], 2) + np.power(vector2[1], 2)))
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        if dot_product < -1:
            dot_product = -1
        elif dot_product > 1:
            dot_product = 1

        angle = np.degrees(np.arccos(dot_product))

        if angle > 180:
            angle = 360 - angle

        if 80 > angle < 110:
            return True
        else:
            return False

    # TODO: Revisit when ready to implement the neural network.
    # def _evaluate_pattern(self, pattern, mode="off"):
    # Utilize a semi-supervised neural network to determine if a pattern is
    # allowed to be used or not. Evaluation is disabled when mode="off"
    # constellation = ConstellationBuilder(self.processed, self.nodes)
    # constellation.add_edges(pattern)

    # if mode == "off":
    # return True
    # elif mode == "predict":
    # Plot the current pattern, convert the plot to an array, and feed
    # the result to the evaluator for approval
    # if self.evaluator.predict(constellation.visualize(to_array=True)) > 0.6:
    # return True
    # else:
    # return False
    # elif mode == "train":
    # Do some training stuff here
    # return True


class NameGenerator:

    def __init__(self, topic):
        self.hyponym = topic
        self.concept_inquirer = ConceptInquirer(topic)
        self.pos_templates = [['VBG', 'NN'],
                              ['JJ', 'NN'],
                              ['JJ', 'VBG', 'NN']]

        self.current_template = random.choice(self.pos_templates)

    def generate_name(self):
        template = random.choice(self.pos_templates)
        name = ''

        for pos in template:
            if pos == 'JJ':
                name += self.get_adjective() + ' '
            elif pos == 'VBG':
                name += self.get_gerund_verb() + ' '
            elif pos == 'NN':
                name += self.get_hypernym()

        return name

    def get_synsets(self):
        return wn.synsets(self.hyponym)

    def get_hypernym(self):
        return random.choice(list(self.concept_inquirer.get_IsA_nodes(1000).keys()))

    def get_adjective(self):
        related_to_nodes = self.concept_inquirer.get_RelatedTo_nodes(1000)

        randnode = random.choice(list(related_to_nodes.keys()))
        while nltk.pos_tag([randnode])[0][1] != 'JJ':
            randnode = random.choice(list(related_to_nodes.keys()))

        return randnode

    def get_gerund_verb(self):
        related_to_nodes = self.concept_inquirer.get_RelatedTo_nodes(1000)

        randnode = random.choice(list(related_to_nodes.keys()))
        while nltk.pos_tag([randnode])[0][1] != 'VBG':
            randnode = random.choice(list(related_to_nodes.keys()))

        return randnode
