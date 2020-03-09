import os, sys
sys.path.append(os.getcwd())
from modules.knowledge_extractor import KnowledgeExtractor


path = os.getcwd() + '\examples\\test.png'

knowext = KnowledgeExtractor(path)

# This method removes some of the contours
# Step is the amount by which we skip over the vertices
knowext.thin_contours(step=1)

# Showing either images is optional and mostly for debugging
knowext.show_threshold()

# Thickness is the thickness of the points representing vertices
knowext.show_image_with_contours(thickness=1)

# Saving either images is optional and mostly for debugging
knowext.save_image(module.KnowledgeExtractor.ImageType.CONTOUR)

knowext.save_image(module.KnowledgeExtractor.ImageType.THRESHOLD)