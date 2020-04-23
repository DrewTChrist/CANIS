"""Process an image and extract star vertices."""
from datetime import datetime

import numpy as np
from PIL import Image
from scipy.spatial.distance import euclidean


class ImageProcessor:

    def __init__(self, original):
        self.original = Image.open(original)
        self.processed = self.original
        self.vertices = np.empty((0, 2), dtype=int)
        self.s_nodes = {}

    def process(self, save_processed_img=False, threshold=220):
        self.processed = self.processed.convert('L')
        self.processed = self.processed.point(
            lambda x: 0 if x < threshold else 255, '1')

        if save_processed_img:
            self.processed.save(f'saved_figures/processed-{datetime.now().strftime("%d%m%Y%H%M%S")}.jpg')

        self._extract_vertices()
        self._build_dictionary()

    def _extract_vertices(self):
        for x in range(self.processed.width):
            for y in range(self.processed.height):
                if self.processed.getpixel((x, y)) == 255:
                    possible_duplicates = np.where(np.any(np.abs(self.vertices - [x, y]) < 7, axis=1))
                    if len(possible_duplicates) > 0:
                        for vertex in self.vertices[possible_duplicates]:
                            if euclidean(vertex, [x, y]) < 10:
                                break
                        else:
                            self.vertices = np.concatenate((self.vertices, [[x, y]]), axis=0)
                    else:
                        self.vertices = np.concatenate((self.vertices, [[x, y]]), axis=0)

    def _build_dictionary(self):
        for count, vertex in enumerate(self.vertices):
            self.s_nodes[count] = [vertex[0], vertex[1]]
