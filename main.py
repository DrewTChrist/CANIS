# Example driver code for now, implementation will probably change.
import os
from Constellation import GraphBuilder
from Processor import ImageProcessor

# New test images can be placed in the /img folder, then manually change image_name accordingly.
image_name = 'sky1.jpg'

ip = ImageProcessor(os.path.join(os.path.curdir, "./img/" + image_name))
ip.process()

constellation = GraphBuilder(ip.img, ip.extract_vertices())
constellation.add_edges([('1', '3000'), ('3000', '300'), ('300', '1')])
constellation.visualize(color='r', save_fig=True)
