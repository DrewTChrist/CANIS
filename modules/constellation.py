"""Build and visualize a new constellation given image and edge data."""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from datetime import datetime
from PIL import Image


class ConstellationBuilder:

    def __init__(self, img, used_nodes):
        self.graph = nx.Graph()
        self.img = img
        self.nodes = used_nodes

    def add_edges(self, edges=[]):
        # Takes an array of edges and applies them to the graph
        self.graph.add_edges_from(edges)

    def _plot_to_array(self, fig):
        # Converts a matplotlib figure to a 360 x 360 image to an array for
        # analysis with a neural network.
        fig.canvas.draw()
        buffer = fig.canvas.tostring_rgb()
        cols, rows = fig.canvas.get_width_height()
        temp_img = Image.fromarray(np.fromstring(buffer, dtype=np.uint8).reshape(rows, cols, 3))
        temp_img = temp_img.resize((360, 360), Image.ANTIALIAS)
        return np.array(temp_img)

    def visualize(self, color='w', show_fig=True, save_fig=False, to_array=False, labels=False, size=0, center=[0, 0], t_vertices=[]):
        # Initialize a new figure from the image and graph data
        layout = nx.spring_layout(self.graph, pos=self.nodes, fixed=self.nodes.keys())
        fig = plt.figure(1, figsize=(15, 15))
        plt.axis([0, self.img.width, 0, self.img.height])

        # Invert the y axis so that image coordinates are oriented properly
        plt.gca().invert_yaxis()
        plt.margins(0, 0)
        plt.imshow(self.img)
        nx.draw_networkx(self.graph, pos=layout, with_labels=labels, node_size=size, edge_color=color)

        if center != [0, 0]:
            plt.plot(center[0], center[1], color='r', marker='x', markersize=20)

        if len(t_vertices) > 0:
            for t_vertex in t_vertices:
                plt.plot(t_vertex[0], t_vertex[1], color='y', marker='o', markersize=10)

        if to_array:
            return self._plot_to_array(fig)

        if save_fig:
            now = datetime.now()
            save_path = 'saved_figures/constellation-'
            plt.savefig(save_path + now.strftime("%d%m%Y%H%M%S") + '.jpg', bbox_inches='tight', pad_inches=0)

        if show_fig:
            plt.show()
