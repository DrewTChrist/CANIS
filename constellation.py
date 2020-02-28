"""Build a graph of nodes given a list of vertices and a source image."""
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx


class ConstellationBuilder:

    def __init__(self, img, graph, vertex_nodes):

        # The star graph generated during the processing stage
        self.G = nx.create_empty_copy(graph)
        self.img = img
        self.nodes = vertex_nodes

    def add_edges(self, edges=[]):
        # Takes an array of edges to draw
        self.G.add_edges_from(edges)

    def visualize(self, color='w', save_fig=False, labels=False, size=0):
        # Setup a new plot
        layout = nx.spring_layout(self.G, pos=self.nodes, fixed=self.nodes.keys())
        plt.figure(1, figsize=(15, 15))
        plt.axis([0, self.img.width, 0, self.img.height])

        # Important to invert the y axis since the vertex coordinates came
        # from an image, and image coordinates have their origin in the top
        # left rather than the bottom left
        plt.gca().invert_yaxis()
        plt.margins(0, 0)
        plt.imshow(self.img)
        nx.draw_networkx(self.G, pos=layout, with_labels=labels, node_size=size, edge_color=color)

        if save_fig:
            now = datetime.now()
            save_path = 'saved_figures/constellation-'
            plt.savefig(save_path + now.strftime("%d%m%Y%H%M%S") + '.jpg', bbox_inches='tight', pad_inches=0)

        plt.show()
