"""Main driver code."""
import os
from constellation import ConstellationBuilder
from generate import Generator
from processor import ImageProcessor

# Test images can be placed in the /src_images folder
image_name = 'sky1.jpg'

# Open a new image for processing and store the ImageProcessor object
ip = ImageProcessor(os.path.join(os.path.curdir, "./src_images/" + image_name))

# Process the image and build a networkx graph from the vertices of each star
ip.process()
ip.extract_vertices()
ip.build_graph()

# Generate a new constellation pattern using the ImageProcessor object as input
gen = Generator(ip)
gen.generate_pattern(gen_type="subset")

# Build a graph from the generated pattern
constellation = ConstellationBuilder(ip.original, gen.used_nodes)
constellation.add_edges(gen.pattern)

# Identify an object from the graph


# Plot the generated pattern over the original image
constellation.visualize(color='w', save_fig=False, labels=False, size=0)
