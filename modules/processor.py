"""Process an image and extract star vertices."""
import networkx as nx
import numpy as np
from datetime import datetime
from modules.geometry import distance
from PIL import Image


class ImageProcessor:

    def __init__(self, original, threshold=200):
        # The original image before processing
        self.original = Image.open(original)

        # Image dimensions
        self.width = self.original.width
        self.height = self.original.height

        # The processed image
        self.processed = self.original

        # Brightness threshold
        self.threshold = threshold

        # An empty array to hold new vertices
        self.vertices = np.empty((0, 2), dtype=int)

        # A dictionary of labelled nodes
        self.nodes = {}

        # A star graph containing the coordinates of each star
        self.graph = nx.Graph()

    def process(self, save_processed_img=False):
        # The image is first converted to grayscale which replaces each
        # pixel's RGB values with just a single brightness value
        self.processed = self.original.convert('L')

        # For each pixel, if the brightness value is below the brightness
        # threshold then set the pixel to black, else set the pixel white
        self.processed = self.processed.point(
            lambda x: 0 if x < self.threshold else 255, '1')

        # Optionally save the processed image
        if save_processed_img:
            now = datetime.now()
            self.processed.save('saved_figures/processed-' + now.strftime(
                "%d%m%Y%H%M%S") + '.jpg')

    def extract_vertices(self):
        # Extract vertices from the image by searching for white pixels. If
        # a white pixel is within 5 pixels of another white pixel, then the
        # pixel is treated as a duplicate and the star is not counted twice
        for x in range(self.processed.width):
            for y in range(self.processed.height):
                if self.processed.getpixel((x, y)) == 255:
                    # Get the indices of all vertices that fall within |x| <
                    # 5 or |y| < 5
                    duplicates = np.where(np.logical_or(
                        np.logical_and(self.vertices[:, 0] < x + 5,
                                       self.vertices[:, 0] > x - 5),
                        np.logical_and(self.vertices[:, 1] < y + 5,
                                       self.vertices[:, 1] > y - 5)))
                    if len(self.vertices) == 0:
                        self.vertices = np.concatenate(
                            (self.vertices, [[x, y]]), axis=0)
                    elif len(duplicates) > 0:
                        found = False
                        for vertex in self.vertices[duplicates]:
                            if distance(vertex, [x, y]) < 10:
                                found = True
                        if not found:
                            self.vertices = np.concatenate(
                                (self.vertices, [[x, y]]), axis=0)
                    else:
                        self.vertices = np.concatenate(
                            (self.vertices, [[x, y]]), axis=0)

    def build_graph(self):
        # Convert vertices into a labelled dictionary of nodes
        count = 1
        for vertex in self.vertices:
            self.nodes[count] = [vertex[0], vertex[1]]
            count += 1

        # Build the star graph from the extracted nodes
        self.graph.add_nodes_from(self.nodes.keys())
        for n, p in self.nodes.items():
            self.graph.nodes[n]['pos'] = p
