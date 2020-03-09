import numpy as np
from modules.knowledge_extractor import KnowledgeExtractor
from scipy.spatial.distance import directed_hausdorff

class Comparator:

    def __init__(self, star_vertices):
        self.s_vertices = star_vertices
        self.s_center = self.get_center(self.s_vertices)

        self.t_vertices = []
        self.t_center = [0, 0]

    def get_center(self, vertices):
        num_vertices = len(vertices)
        center_x = 0
        center_y = 0

        for vertex in vertices:
            center_x += vertex[0]
            center_y += vertex[1]

        return [int(round(center_x / num_vertices)), int(round(center_y / num_vertices))]

    def convert_coordinates(self):
        # Calculate the topic center
        self.t_center = self.get_center(self.t_vertices)

        # Get the relative coordinates of each topic vertex to the topic center
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] -= self.t_center[0]
            self.t_vertices[i][1] -= self.t_center[1]

        # Offset each relative coordinate by the center of the star image to
        # complete the conversion
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] += self.s_center[0]
            self.t_vertices[i][1] += self.s_center[1]

    def scale_coordinates(self, scalar):
        for i in range(len(self.t_vertices)):
            self.t_vertices[i][0] *= scalar
            self.t_vertices[i][1] *= scalar

    def rotate_coordinates(self, radians=np.pi/6):
        ox, oy = self.s_center[0], self.s_center[1]
        c, s = np.cos(radians), np.sin(radians)
        for i in range(len(self.t_vertices)):
            px, py = self.t_vertices[i][0], self.t_vertices[i][1]
            self.t_vertices[i][0] = c * (px - ox) - s * (py - oy) + ox
            self.t_vertices[i][1] = s * (px - ox) + c * (py - oy) + oy

    def best_fit(self):
        # Use a local knowledge extractor for now
        knowext = KnowledgeExtractor("test.png")
        knowext.thin_contours(step=20)
        self.t_vertices = knowext.contours
        self.scale_coordinates(2)
        self.convert_coordinates()

        print(directed_hausdorff(self.s_vertices, self.t_vertices))
        print(self.t_vertices)
        for i in range(11):
            self.rotate_coordinates()
            print(directed_hausdorff(self.s_vertices, self.t_vertices))
