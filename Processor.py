"""Process an image and extract star vertices."""
import numpy as np
from Geometry import distance
from PIL import Image


class ImageProcessor:

    def __init__(self, img, threshold=200):
        # A path to the image to process
        self.img = Image.open(img)

        # Determines the threshold for discarding stars during image
        # processing. Value must be between 0 and 255, higher values mean
        # more stars are discarded
        self.threshold = threshold

        # An empty array to hold new vertices
        self.vertices = np.empty((0, 2), dtype=int)

    def process(self, save_processed_img=False):
        # The image is first converted to grayscale which replaces each
        # pixel's RGB values with just a single brightness value
        self.img = self.img.convert('L')

        # For each pixel, if the brightness value is below the brightness
        # threshold then set the pixel to black, otherwise set the pixel to
        # white
        self.img = self.img.point(lambda x: 0 if x < self.threshold else 255, '1')

        if save_processed_img:
            self.img.save('processed.jpg')

    def extract_vertices(self):
        # Extract vertices from the image by searching for white pixels. If
        # a white pixel is within 5 pixels of another white pixel, then the
        # pixel is treated as a duplicate and the star is not counted twice
        for x in range(self.img.width):
            for y in range(self.img.height):
                if self.img.getpixel((x, y)) == 255:
                    # Get the indices of all vertices that fall within |x| <
                    # 5 or |y| < 5
                    duplicates = np.where(np.logical_or(
                        np.logical_and(self.vertices[:, 0] < x + 5, self.vertices[:, 0] > x - 5),
                        np.logical_and(self.vertices[:, 1] < y + 5, self.vertices[:, 1] > y - 5)))
                    if len(self.vertices) == 0:
                        self.vertices = np.concatenate((self.vertices, [[x, y]]), axis=0)
                    elif len(duplicates) > 0:
                        found = False
                        for vertex in self.vertices[duplicates]:
                            if distance(vertex, [x, y]) < 10:
                                found = True
                        if not found:
                            self.vertices = np.concatenate((self.vertices, [[x, y]]), axis=0)
                    else:
                        self.vertices = np.concatenate((self.vertices, [[x, y]]), axis=0)
        return self.vertices
