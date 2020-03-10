import itertools
import numpy as np
from modules.geometry import distance
from modules.knowledge_extractor import KnowledgeExtractor
from scipy.spatial.distance import directed_hausdorff


class Comparator:

    def __init__(self, star_vertices):
        self.s_vertices = star_vertices
        self.s_center = self.get_center(self.s_vertices)

        self.t_vertices = []
        self.t_center = [0, 0]

    def get_center(self, vertices):
        # Calculates the center of a set of vertices by taking the average x and
        # average y values
        num_vertices = len(vertices)
        center_x = 0
        center_y = 0

        for vertex in vertices:
            center_x += vertex[0]
            center_y += vertex[1]

        return [int(round(center_x / num_vertices)), int(round(center_y / num_vertices))]

    def get_furthest_distance(self, vertices):
        # Returns the distance between the two furthest apart vertices in a set
        # of vertices
        furthest = 0

        for i, j in itertools.combinations(vertices, 2):
            if distance(i, j) > furthest:
                furthest = distance(i, j)

        return furthest

    def convert_coordinates(self):
        # Calculate the topic center
        self.t_center = self.get_center(self.t_vertices)

        # Get the relative coordinates of each topic vertex to the topic center
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] -= self.t_center[0]
            self.t_vertices[i][1] -= self.t_center[1]

        # Offset each relative coordinate by the center of the star image to
        # convert the vertices to image space
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] += self.s_center[0]
            self.t_vertices[i][1] += self.s_center[1]

    def scale_coordinates(self):
        # Calculate the distance between the furthest two vertices in the star
        # set and the topic set
        s_furthest = self.get_furthest_distance(self.s_vertices)
        t_furthest = self.get_furthest_distance(self.t_vertices)

        # Take the ratio of these two distances
        scalar = s_furthest / t_furthest

        # Apply the scaling to each coordinate in the topic set
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] *= scalar
            self.t_vertices[i][1] *= scalar

    def rotate_coordinates(self, radians=np.pi/6):
        # Rotate the topic vertices by some angle in radians, defaults to 30
        # degrees
        ox, oy = self.s_center[0], self.s_center[1]
        c, s = np.cos(radians), np.sin(radians)
        for i in range(len(self.t_vertices)):
            px, py = self.t_vertices[i][0], self.t_vertices[i][1]
            self.t_vertices[i][0] = c * (px - ox) - s * (py - oy) + ox
            self.t_vertices[i][1] = s * (px - ox) + c * (py - oy) + oy

    def best_fit(self):
        # Use a local knowledge extractor for now
        knowext = KnowledgeExtractor("test1.png")
        knowext.thin_contours(step=22)
        self.t_vertices = knowext.contours
        self.scale_coordinates()
        self.convert_coordinates()

        best = directed_hausdorff(self.s_vertices, self.t_vertices)

        for i in range(23):
            self.rotate_coordinates(np.pi/12)
            current = directed_hausdorff(self.s_vertices, self.t_vertices)

            if current < best:
                best = current

        print(best)
