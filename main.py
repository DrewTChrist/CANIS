"""Main driver code."""
import math
import os
from modules.compare import Comparator
from modules.constellation import Constellation
from modules.generate import PatternGenerator
from modules.processor import ImageProcessor

# Test images can be placed in the /src_images folder
image_name = 'sky2.jpg'

# Open a new image for processing and store the ImageProcessor object
ip = ImageProcessor(os.path.join(os.path.curdir, "./src_images/" + image_name))

# Process the image and build a labelled dictionary of each star vertex
ip.process()

# Arbitrary starting score that will always be larger than compare.score
best_score = math.inf

for i in range(1000):
    # Generate a new star pattern using the dictionary of stars
    pattern_gen = PatternGenerator(ip.s_nodes)
    pattern_gen.generate_pattern(gen_type="subset")

    # Identify an object that best fits the pattern
    compare = Comparator(pattern_gen.s_vertices)
    compare.fit()

    # If a better scoring configuration is found, save the configuration
    if compare.score < best_score:
        print(best_score)
        best_score = compare.score
        best_s_nodes = pattern_gen.s_nodes
        best_pattern = pattern_gen.pattern
        best_t_vertices = compare.t_vertices

print(best_score)

# Generate a name from the best fitting object
# name_gen = NameGenerator()

# Build a new constellation instance from the generated pattern
constellation = Constellation(ip.original, best_s_nodes)
constellation.add_edges(best_pattern)

# Plot the constellation over the original image
constellation.visualize(color='w', save_fig=True, labels=False, size=0, t_vertices=best_t_vertices)
