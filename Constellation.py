# Build a graph of nodes given a list of vertices and a source image.
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx


class GraphBuilder:
    def __init__(self, img, vertices):
        self.img = img
        self.vertex_nodes = {}
        count = 1

        # Convert the array of vertices to a dictionary of nodes that networkx can understand.
        for vertex in vertices:
            self.vertex_nodes[str(count)] = [vertex[0], vertex[1]]
            count += 1

        # Initialize a new graph and populate it with vertices.
        self.G = nx.Graph()
        self.G.add_nodes_from(self.vertex_nodes.keys())
        for n, p in self.vertex_nodes.items():
            self.G.nodes[n]['pos'] = p

    def add_edges(self, edges=[]):
        # Takes an array of edges to draw
        self.G.add_edges_from(edges)

    def visualize(self, color='w', save_fig=False):
        # Setup a new plot.
        layout = nx.spring_layout(self.G, pos=self.vertex_nodes, fixed=self.vertex_nodes.keys())
        plt.figure(1, figsize=(15, 15))
        plt.axis([0, self.img.width, 0, self.img.height])

        # Important to invert the y axis since the vertex coordinates came from an image, and image coordinates have
        # their origin in the top left rather than the bottom left.
        plt.gca().invert_yaxis()
        plt.margins(0, 0)
        plt.imshow(self.img)
        nx.draw_networkx(self.G, pos=layout, node_size=0, edge_color=color)

        if save_fig:
            now = datetime.now()
            plt.savefig('saved_figures/constellation-' + now.strftime("%d%m%Y%H%M%S") + '.jpg', bbox_inches='tight', pad_inches=0)

        plt.show()

