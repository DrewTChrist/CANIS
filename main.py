"""Main driver code."""
import math
import os
import time

from modules.compare import Comparator
from modules.constellation import Constellation
from modules.generate import NameGenerator, PatternGenerator
from modules.knowledge import knowledge_base
from modules.processor import ImageProcessor

# Load an array of topics for comparision - labels and vertices
print('Loading knowledge base')
knowledge = knowledge_base()

# Open a new image for processing and store the ImageProcessor object
image_name = 'sky1.jpg'
ip = ImageProcessor(os.path.join(os.path.curdir, f'./src_images/{image_name}'))

# Process the image and build a labelled dictionary of each star vertex
print('Processing source image')
ip.process()

# Initialize a pattern generating object
pattern_gen = PatternGenerator(ip.s_nodes)

# Arbitrary starting score that will always be larger than compare.score
score = math.inf

print('Fitting topic images')
t0 = time.time()
for i in range(200):
    # Generate a new star pattern using the dictionary of stars
    pattern_gen.generate_pattern(gen_type='subset')

    # Identify an object that best fits the pattern
    compare = Comparator(pattern_gen.s_vertices, knowledge)
    compare.fit()

    # If a better scoring configuration is found, save the configuration
    if compare.score < score:
        score = round(compare.score, 2)
        s_nodes = pattern_gen.s_nodes
        pattern = pattern_gen.pattern
        label = compare.best_label
        t_vertices = compare.best_vertices
        print(f'{score} - {label}')

# Print the final best score
t1 = time.time()
print(f'best - {score} - {label} found in {round(t1 - t0, 2)} seconds')

# Generate a name from the best fitting object
name_gen = NameGenerator(label)
constellation_name = name_gen.generate_name()

# Build a new constellation instance from the generated pattern
constellation = Constellation(ip.original, s_nodes)
constellation.add_edges(pattern)

# Plot the constellation over the original image
constellation.visualize(t_label=constellation_name, t_vertices=t_vertices)
