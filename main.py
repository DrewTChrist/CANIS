from Constellation import GraphBuilder
from Processor import ImageProcessor

ip = ImageProcessor('sky1.jpg')
ip.process()

constellation = GraphBuilder(ip.img, ip.extract_vertices())
constellation.add_edges([('1', '3000'), ('3000', '300'), ('300', '1')])
constellation.visualize(color='r')
