"""Compare a star pattern to several topic images to find a best fit."""
import itertools
import math
from copy import deepcopy

from scipy.spatial.distance import directed_hausdorff, euclidean


class Comparator:

    def __init__(self, s_vertices, knowledge):
        self.s_vertices = s_vertices
        self.s_center = _calculate_center(self.s_vertices)
        self.knowledge = knowledge
        self.best_label = ''
        self.best_center = []
        self.best_vertices = []
        self.t_center = [0, 0]
        self.score = math.inf

    def fit(self):
        for topic in self.knowledge:
            temp = topic.vertices
            self._scale_coordinates(temp)
            self._convert_coordinates(temp)
            for i in range(24):
                current = directed_hausdorff(self.s_vertices, temp)[0]
                if current < self.score:
                    self.score = current
                    self.best_label = topic.label
                    self.best_center = _calculate_center(temp)
                    self.best_vertices = deepcopy(temp)

                self._rotate_coordinates(temp)

    def _scale_coordinates(self, t_vertices):
        # Calculate the longest distance between any two vertices in each set
        s_longest = _calculate_longest(self.s_vertices)
        t_longest = _calculate_longest(t_vertices)

        # Take the ratio of these two distances
        scalar = s_longest / t_longest

        # Apply the scaling to each coordinate in the topic set
        for vertex in t_vertices:
            vertex[0] *= scalar
            vertex[1] *= scalar

    def _convert_coordinates(self, t_vertices):
        self.t_center = _calculate_center(t_vertices)
        x_offset = self.s_center[0] - self.t_center[0]
        y_offset = self.s_center[1] - self.t_center[1]
        for vertex in t_vertices:
            vertex[0] += x_offset
            vertex[1] += y_offset

    def _rotate_coordinates(self, t_vertices, radians=math.pi / 12):
        # Rotate the topic vertices by some angle in radians, defaults to 30
        # degrees
        ox, oy = self.s_center
        c, s = math.cos(radians), math.sin(radians)

        for vertex in t_vertices:
            px, py = vertex[0], vertex[1]
            vertex[0] = c * (px - ox) - s * (py - oy) + ox
            vertex[1] = s * (px - ox) + c * (py - oy) + oy


def _calculate_longest(vertices):
    # Returns the distance between the two furthest apart vertices in a set
    # of vertices
    longest = 0

    for i, j in itertools.combinations(vertices, 2):
        new_distance = euclidean(i, j)
        if new_distance > longest:
            longest = new_distance

    return longest


def _calculate_center(vertices):
    # Calculates the center of a set of vertices by taking the average x and
    # average y values
    x_center, y_center = 0, 0

    for vertex in vertices:
        x_center += vertex[0]
        y_center += vertex[1]

    return [x_center / len(vertices), y_center / len(vertices)]
