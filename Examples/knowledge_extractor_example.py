import os
import importlib.util


# Loads module from parent directory until we restructure the files
# Snippet from:
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
spec = importlib.util.spec_from_file_location("KnowledgeExtractor", os.getcwd() + "\knowledge_extractor.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


path = os.getcwd() + '\examples\\bird.png'

knowext = module.KnowledgeExtractor(path)

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