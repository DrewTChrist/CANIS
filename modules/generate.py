"""Generate new star patterns and names."""
import itertools
import random

import networkx as nx
import nltk
import numpy as np
from nltk.corpus import wordnet as wn
from scipy.spatial.distance import euclidean

from modules.concept_query import ConceptInquirer


class PatternGenerator:

    def __init__(self, nodes):
        self.nodes = nodes
        self.node_keys = self.nodes.keys()
        self.s_vertices = []
        self.s_nodes = {}
        self.pattern = []

    def generate_pattern(self, gen_type='subset'):
        candidate = self._mst_pattern(gen_type)

        for i in range(2):
            if np.random.uniform(0, 1) >= 0.5:
                edge = self._get_cycle(candidate)
                if edge is not None:
                    candidate.append(edge)

        self.pattern = candidate

        node_list = []
        s_vertices = []
        for edge in self.pattern:
            for node in edge:
                if node not in node_list:
                    node_list.append(node)
                    s_vertices.append(self.nodes[node])

        self.s_nodes = {k: v for k, v in self.nodes.items() if k in node_list}
        self.s_vertices = s_vertices

    def _mst_pattern(self, gen_type='subset'):
        graph = nx.Graph()

        # Utilize the full set of stars resulting in the same pattern after
        # each generation for a given image
        if gen_type is 'full':
            for i, j in itertools.combinations(self.node_keys, 2):
                graph.add_edge(i, j, weight=euclidean(self.nodes[i], self.nodes[j]))

        # Randomly choose a subset of stars resulting in a different pattern
        # after each generation
        elif gen_type is 'subset':
            subset = np.random.choice(range(1, len(self.node_keys)), np.random.randint(5, 12), replace=False)
            for i, j in itertools.combinations(subset, 2):
                graph.add_edge(i, j, weight=euclidean(self.nodes[i], self.nodes[j]))

        return list(nx.minimum_spanning_edges(graph, data=False))

    def _get_cycle(self, candidate):
        node_list = []
        for edge in candidate:
            for node in edge:
                if node not in node_list:
                    node_list.append(node)

        np.random.shuffle(node_list)

        for i, j in itertools.combinations(node_list, 2):
            a, b = self.nodes[i], self.nodes[j]
            for edge in candidate:
                c, d = self.nodes[edge[0]], self.nodes[edge[1]]
                intersect = _intersection(a, b, c, d)
                if intersect:
                    break
            else:
                return i, j


# Credit: https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
# Return true if line segments AB and CD intersect
def _intersection(a, b, c, d):
    return _ccw(a, c, d) != _ccw(b, c, d) and _ccw(a, b, c) != _ccw(a, b, d)


# Determine if A, B, C are oriented counterclockwise
def _ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


class NameGenerator:

    def __init__(self, topic):
        self.hyponym = topic
        self.concept_inquirer = ConceptInquirer(topic)
        self.pos_templates = [['VBG', 'NN'], ['JJ', 'NN'], ['JJ', 'VBG', 'NN']]
        self.current_template = random.choice(self.pos_templates)

    def generate_name(self):
        template = random.choice(self.pos_templates)
        name = ''

        for pos in template:
            if pos is 'JJ':
                name += self.get_adjective() + ' '
            elif pos is 'VBG':
                name += self.get_gerund_verb() + ' '
            elif pos is 'NN':
                name += self.get_hypernym()

        return name

    def get_synsets(self):
        return wn.synsets(self.hyponym)

    def get_hypernym(self):
        return random.choice(
            list(self.concept_inquirer.get_IsA_nodes(1000).keys()))

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
