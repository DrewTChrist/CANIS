"""KnowledgeExtractor class will be used to extract meaningful information from 
images that can be stored in a "knowledge-base" for the system.
"""

# TODO: More thinning of contours
# TODO: Perhaps convert the contours to vertices
# TODO: Function that adds a white background to images with an alpha layer

import cv22 as cv2
from datetime import datetime
from enum import Enum


class KnowledgeExtractor:

    def __init__(self, path, threshold=235, maximum=255):
        self.path = path
        self.image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        if self.image.shape[2] == 4:
            self._add_white_background()
        self.gray_scale_image = cv2.cv2tColor(self.image, cv2.COLOR_BGR2GRAY)
        self.ret, self.threshold = cv2.threshold(self.gray_scale_image, threshold, maximum, 0)
        self.contours, self.hierarchy = cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Shows the threshold image in an Opencv2 window
    def show_threshold(self):
        cv2.imshow('Threshold Image', self.threshold)
        cv2.waitKey(0)

    # Shows the original image with contours on top in an Opencv2 window
    def show_image_with_contours(self):
        img_with_contours = self._get_image_with_contours()
        cv2.imshow('Image with contours', img_with_contours)
        cv2.waitKey(0)

    # Removes all edge arrays except the largest one
    # This is a temporary solution
    def thin_contours(self):
        self.contours = max(self.contours, key=len)

    # Saves either the threshold image or the original image with the contours
    def save_image(self, image_type):
        if image_type == self.ImageType.THRESHOLD:
            cv2.imwrite(datetime.now().strftime("%d%m%Y%H%M%S") + '_threshold.png', self.threshold)
        elif image_type == self.ImageType.CONTOUR:
            img_with_contours = self._get_image_with_contours()
            cv2.imwrite(datetime.now().strftime("%d%m%Y%H%M%S") + '_contour.png', img_with_contours)

    # Returns the original image with the contours drawn over        
    def _get_image_with_contours(self):
        return cv2.drawContours(self.image, self.contours, -1, (0, 0, 255), 1)


    # Private method that converts alpha channel to white background
    def _add_white_background(self):
        trans_mask = self.image[:,:,3] == 0
        self.image[trans_mask] = [255, 255, 255, 255]
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)

    # Enum for saving images
    class ImageType(Enum):
        THRESHOLD = 1
        CONTOUR = 2
