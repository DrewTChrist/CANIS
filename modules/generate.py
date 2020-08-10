"""Generate new star patterns and names."""
import itertools
import time
from enum import Enum

import networkx as nx
import nltk
import numpy as np
import spacy
import lemminflect
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
        if gen_type == 'full':
            for i, j in itertools.combinations(self.node_keys, 2):
                graph.add_edge(i, j, weight=euclidean(self.nodes[i], self.nodes[j]))

        # Randomly choose a subset of stars resulting in a different pattern
        # after each generation
        elif gen_type == 'subset':
            subset = np.random.choice(range(1, len(self.node_keys)), np.random.randint(7, 15), replace=False)
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
        print('NameGenerator class created')
        self.hyponym = topic
        self.concept_inquirer = ConceptInquirer(topic)
        self.pos_templates = [['VBG', 'NN'], ['JJ', 'NN'], ['JJ', 'VBG', 'NN']]
        self.current_template = np.random.choice(self.pos_templates)
        print("spacy.load('en_core_web_md')")
        self.nlp = spacy.load('en_core_web_md')

    def generate_name(self):
        print('Generating name')
        temps = [x for x in self.Templates]
        rand_temp = np.random.choice(temps)

        if rand_temp == self.Templates.HYPERNYM:
            # convert to latin
            return self.get_hypernym()
        elif rand_temp == self.Templates.BIGRAM:
            # get semantically related adjective or verb
            # add it to topic, translate to latin       randomly chose adjective or verb
            verb_or_adj = np.random.choice(['adjective', 'verb'])
            if verb_or_adj == 'adjective':
                best_adjective = self.find_related_adjective(10, 0.55, 15.0)
                return f'{best_adjective[0]} {self.hyponym}'
            else:
                best_verb = self.find_related_verb(10, 0.55, 15.0)
                return f'{best_verb[0]} {self.hyponym}'
        elif rand_temp == self.Templates.TRIGRAM:
            if len(self.get_hypernym().split(' ')) > 1:
                # if hypernym has two words add adjective
                best_adjective = self.find_related_adjective(10, 0.55, 15.0)
                return f'{best_adjective[0]} {self.hyponym}'
            else:
                # if hypernym has one word add adjective
                # and add a semantically related verb
                # translate to latin
                best_verb = self.find_related_verb(10, 0.55, 15.0)
                best_adjective = self.find_related_adjective(10, 0.55, 15.0)
                return f'{best_adjective[0]} {best_verb[0]} {self.hyponym}'

    def get_synsets(self):
        return wn.synsets(self.hyponym)

    def get_hypernym(self):
        choices = list(self.concept_inquirer.get_IsA_nodes(1000).keys())
        if len(choices) >= 1:
            return np.random.choice(choices)
        else:
            return self.hyponym

    def find_related_verb(self, sample_size, similarity_threshold, timeout):
        print('Finding related verb')
        all_wn_verbs = list(wn.all_synsets('v'))

        greatest_similarity = 0.0
        most_similar_verb = ''
        start_time = time.time()

        while greatest_similarity < similarity_threshold:
            runtime = time.time() - start_time
            if runtime > timeout:
                break
            else:
                print(f'Verb search current runtime: {runtime}')

            verb_sample = [x.lemmas()[0].name() for x in np.random.choice(all_wn_verbs, sample_size)]
            tokens = self.nlp(f'{self.hyponym} ' + ' '.join(verb_sample))

            for token in tokens:
                if token and token.vector_norm and token.text != self.hyponym:
                    if token.similarity(tokens[0]) > greatest_similarity:
                        greatest_similarity = token.similarity(tokens[0])
                        most_similar_verb = token

        return most_similar_verb._.inflect('VBG'), greatest_similarity

    def find_related_adjective(self, sample_size, similarity_threshold, timeout):
        print('Finding related adjective')
        all_wn_adjectives = list(wn.all_synsets('a'))

        greatest_similarity = 0.0
        most_similar_adj = ''
        start_time = time.time()

        while greatest_similarity < similarity_threshold:
            runtime = time.time() - start_time
            if runtime > timeout:
                break
            else:
                print(f'Adjective search current runtime: {runtime}')

            adj_sample = [x.lemmas()[0].name() for x in np.random.choice(all_wn_adjectives, sample_size)]
            tokens = self.nlp(f'{self.hyponym} ' + ' '.join(adj_sample))

            for token in tokens:
                if token and token.vector_norm and token.text != self.hyponym:
                    if token.similarity(tokens[0]) > greatest_similarity:
                        greatest_similarity = token.similarity(tokens[0])
                        most_similar_adj = token.text

        return most_similar_adj, greatest_similarity

    class Templates(Enum):
        HYPERNYM = 1
        BIGRAM = 2
        TRIGRAM = 3
