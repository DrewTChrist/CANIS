"""Main driver code."""
import math
import os
from modules.compare import Comparator
from modules.constellation import Constellation
from modules.generate import PatternGenerator, NameGenerator
from modules.knowledge import knowledge_base
from modules.processor import ImageProcessor


# Test images can be placed in the /src_images folder
image_name = 'sky1.jpg'

# Open a new image for processing and store the ImageProcessor object
ip = ImageProcessor(os.path.join(os.path.curdir, "./src_images/" + image_name))

# Process the image and build a labelled dictionary of each star vertex
ip.process()

# An array of topics for comparision - labels and vertices
knowledge = knowledge_base()

# Arbitrary starting score that will always be larger than compare.score
best_score = math.inf

print("Fitting topic images")
for i in range(1000):
    # Generate a new star pattern using the dictionary of stars
    pattern_gen = PatternGenerator(ip.s_nodes)
    pattern_gen.generate_pattern(gen_type="subset")

    # Identify an object that best fits the pattern
    compare = Comparator(pattern_gen.s_vertices, knowledge)
    compare.fit()

    # If a better scoring configuration is found, save the configuration
    if compare.score < best_score:
        best_score = compare.score
        best_s_nodes = pattern_gen.s_nodes
        best_pattern = pattern_gen.pattern
        best_label = compare.best_label
        best_vertices = compare.best_vertices
        print(f'{best_score} - {best_label}')

# Print the final best score
print(f'best - {best_score} - {best_label}')

# Generate a name from the best fitting object
# TODO: Investigate why name generation sometimes causes the program to hang/crash.
#name_gen = NameGenerator(best_label)
#constellation_name = name_gen.generate_name()

# Build a new constellation instance from the generated pattern
constellation = Constellation(ip.original, best_s_nodes)
constellation.add_edges(best_pattern)

# Plot the constellation over the original image
constellation.visualize(color='w', save_fig=False, labels=False, size=20, t_label=best_label, t_vertices=best_vertices)
