from knowledge_extractor import KnowledgeExtractor

path = ''


knowext = KnowledgeExtractor(path)

# This method removes some of the contours
knowext.thin_contours()

# Showing either images is optional
knowext.show_threshold()

knowext.show_image_with_contours()

# Saving either images is optional
knowext.save_image(KnowledgeExtractor.ImageType.CONTOUR)

knowext.save_image(KnowledgeExtractor.ImageType.THRESHOLD)