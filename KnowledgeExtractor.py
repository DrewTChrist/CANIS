'''
KnowledgeExtractor class will be used to extract
meaningful information from images that can be
stored in a "knowledgebase" for the system.
'''


import cv2 as cv
import numpy as np
from datetime import datetime
from enum import Enum

class KnowledgeExtractor:
    
    def __init__(self, path, threshold=235, maximum=255):
        self.path = path
        self.image = cv.imread(self.path)
        self.gray_scale_image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.ret, self.threshold = cv.threshold(self.gray_scale_image, threshold, maximum, 0)
        self.contours, self.hierarchy = cv.findContours(self.threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Shows the threshold image in an OpenCV window
    def show_threshold(self):
        cv.imshow('Threshold Image', self.threshold)
        cv.waitKey(0)

    # Shows the original image with contours on top in an OpenCV window
    def show_image_with_contours(self):
        img_with_contours = self.get_image_with_contours()
        cv.imshow('Image with contours', img_with_contours)
        cv.waitKey(0)

    # Removes all edge arrays except the largest one
    def thin_contours(self):
        self.contours = max(self.contours, key=len)

    # Saves either the threshold image or
    # the original image with the contours
    def save_image(self, image_type):
        if image_type == self.ImageType.THRESHOLD:
            cv.imwrite(datetime.now().strftime("%d%m%Y%H%M%S") + '.png', self.threshold)
        elif image_type == self.ImageType.CONTOUR:
            img_with_contours = self.get_image_with_contours()
            cv.imwrite(datetime.now().strftime("%d%m%Y%H%M%S") + '.png', img_with_contours)

    # Returns the original image with the contours drawn over        
    def get_image_with_contours(self):
        return cv.drawContours(self.image, self.contours, -1, (0, 255, 0), 1)

    # Enum for saving images        
    class ImageType(Enum):
        THRESHOLD = 1
        CONTOUR = 2

# TODO: More thinning of contours
# TODO: Perhaps convert the contours to vertices
# TODO: Function that adds a white background to images with an alpha layer


