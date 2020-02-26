# Example driver code for now, implementation will probably change
import os
from constellation import GraphBuilder
from generate import Generator
from processor import ImageProcessor

# New test images can be placed in the /img folder, then manually change
# image_name accordingly
image_name = 'sky1.jpg'

# Open and process a new image
ip = ImageProcessor(os.path.join(os.path.curdir, "./img/" + image_name))
original = ip.img
ip.process()

# Extract vertices and convert them to a node dictionary
node_dictionary = ip.extract_vertices()

# Generate a new pattern specifying the number of edges and minimum fitness
new_pattern = Generator(node_dictionary, num_edges=10).generate_pattern(min_fitness=63)

# Build and plot the pattern over the original image
constellation = GraphBuilder(original, node_dictionary)
constellation.add_edges(new_pattern)
constellation.visualize(color='w', save_fig=False)
