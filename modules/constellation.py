"""Build and visualize a new constellation given image and edge data."""
from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Constellation:

    def __init__(self, img, nodes):
        self.graph = nx.Graph()
        self.img = img
        self.nodes = nodes
        self.node_keys = self.nodes.keys()

    def add_edges(self, edges=None):
        if edges is not None:
            self.graph.add_edges_from(edges)

    def visualize(self, show_fig=True, save_fig=False, labels=False, size=0, t_center=None, t_label='', t_vertices=None):
        # Initialize a new figure from the image and graph data
        layout = nx.spring_layout(self.graph, pos=self.nodes, fixed=self.node_keys)
        plt.figure(1, figsize=(15, 15))
        plt.axis([0, self.img.width, 0, self.img.height])

        # Invert the y axis so that image coordinates are oriented properly
        plt.gca().invert_yaxis()
        plt.margins(0, 0)
        plt.imshow(self.img)
        nx.draw_networkx(self.graph, pos=layout, with_labels=labels, node_size=size, edge_color='w')
        plt.title(t_label)

        if t_center is not None:
            plt.plot(t_center[0], t_center[1], color='r', marker='x', markersize=20)

        if t_vertices is not None:
            #plt.plot(*zip(*t_vertices), color='y', marker='o', markersize=4)
            t_vertices = np.array(t_vertices)
            plt.plot(t_vertices[:, 0], t_vertices[:, 1], color='y', marker='o', markersize=4)

        if save_fig:
            now = datetime.now()
            formatted = now.strftime('%d%m%Y%H%M%S')
            plt.savefig(f'saved_figures/constellation-{formatted}.jpg', bbox_inches='tight', pad_inches=0)

        if show_fig:
            plt.show()
