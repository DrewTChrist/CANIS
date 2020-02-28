# Example driver code for now, implementation will probably change
import os
from constellation import ConstellationBuilder
from generate import Generator
from processor import ImageProcessor

# New test images can be placed in the /img folder, then manually change
# image_name accordingly
image_name = 'sky1.jpg'

# Open a new image, store it's original form
ip = ImageProcessor(os.path.join(os.path.curdir, "./img/" + image_name))
original = ip.img

# Process the image and build a networkx graph of each star
ip.process()
ip.extract_vertices()
ip.build_graph(type="subset")

# Generate a new pattern specifying minimum fitness (0 by default until a
# proper implementation is in place)
gen = Generator(ip.graph, ip.nodes)
gen.generate_pattern(type="subset")

# Assemble a new constellation and plot the pattern over the original image
constellation = ConstellationBuilder(original, ip.graph, ip.nodes)
constellation.add_edges(gen.pattern)
constellation.visualize(color='w', save_fig=False, labels=False, size=0)
