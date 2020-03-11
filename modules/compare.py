import itertools
import numpy as np
from modules.knowledge_extractor import KnowledgeExtractor
from scipy.spatial.distance import directed_hausdorff
from scipy.spatial.distance import euclidean


class Comparator:

    def __init__(self, s_vertices):
        self.s_vertices = s_vertices
        self.s_center = self._calculate_center(self.s_vertices)

        self.t_vertices = []
        self.best = []
        self.t_center = [0, 0]

        self.score = 0
        self.object = ""

    def reset_fields(self, s_vertices):
        self.s_vertices = s_vertices
        self.s_center = self._calculate_center(self.s_vertices)

        self.t_vertices = []
        self.t_center = [0, 0]

        self.score = 0
        self.object = ""

    def fit(self):
        # Use a local knowledge extractor for now
        knowext = KnowledgeExtractor("test1.png")
        knowext.thin_contours(step=20)
        self.t_vertices = knowext.contours
        self._scale_coordinates()
        self._convert_coordinates()

        self.score = directed_hausdorff(self.s_vertices, self.t_vertices)[0]
        score_state = np.copy(self.t_vertices)

        for i in range(23):
            self._rotate_coordinates(np.pi/12)
            current = directed_hausdorff(self.s_vertices, self.t_vertices)[0]

            if current < self.score:
                self.score = current
                score_state = np.copy(self.t_vertices)
                self.object = "object name here"

        self.t_vertices = score_state

    def _calculate_center(self, vertices):
        # Calculates the center of a set of vertices by taking the average x and
        # average y values
        x_center, y_center = 0, 0

        for vertex in vertices:
            x_center += vertex[0]
            y_center += vertex[1]

        return [x_center / len(vertices), y_center / len(vertices)]

    def _scale_coordinates(self):
        # Calculate the longest distance between any two vertices in each set
        s_longest = self._calculate_longest(self.s_vertices)
        t_longest = self._calculate_longest(self.t_vertices)

        # Take the ratio of these two distances
        scalar = s_longest / t_longest

        # Apply the scaling to each coordinate in the topic set
        for vertex in self.t_vertices:
            vertex[0] *= scalar
            vertex[1] *= scalar

    def _calculate_longest(self, vertices):
        # Returns the distance between the two furthest apart vertices in a set
        # of vertices
        longest = 0

        for i, j in itertools.combinations(vertices, 2):
            new_distance = euclidean(i, j)
            if new_distance > longest:
                longest = new_distance

        return longest

    def _convert_coordinates(self):
        # Calculate the topic center
        self.t_center = self._calculate_center(self.t_vertices)

        # Get the relative coordinates of each topic vertex to the topic center
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] -= self.t_center[0]
            self.t_vertices[i][1] -= self.t_center[1]

        # Offset each relative coordinate by the center of the star image to
        # convert the vertices to image space
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] += self.s_center[0]
            self.t_vertices[i][1] += self.s_center[1]

    def _rotate_coordinates(self, radians=np.pi/6):
        # Rotate the topic vertices by some angle in radians, defaults to 30
        # degrees
        ox, oy = self.s_center[0], self.s_center[1]
        c, s = np.cos(radians), np.sin(radians)
        for vertex in self.t_vertices:
            px, py = vertex[0], vertex[1]
            vertex[0] = c * (px - ox) - s * (py - oy) + ox
            vertex[1] = s * (px - ox) + c * (py - oy) + oy
