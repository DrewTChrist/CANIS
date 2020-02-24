# Example driver code for now, implementation will probably change
import os
from Constellation import GraphBuilder
from Generate import Generator
from Processor import ImageProcessor

# New test images can be placed in the /img folder, then manually change
# image_name accordingly
image_name = 'sky2.jpg'

ip = ImageProcessor(os.path.join(os.path.curdir, "./img/" + image_name))
original = ip.img
ip.process()

nodes = ip.extract_vertices()

new_pattern = Generator(nodes).generate_pattern()

constellation = GraphBuilder(ip.img, nodes)
constellation.add_edges(new_pattern)
constellation.visualize(color='r', save_fig=False)
