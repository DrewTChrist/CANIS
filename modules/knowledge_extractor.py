"""KnowledgeExtractor class will be used to extract meaningful information from 
images that can be stored in a "knowledge-base" for the system.
"""
from datetime import datetime
from enum import Enum

import cv2 as cv2
import numpy as np
import scipy.spatial


class KnowledgeExtractor:

    def __init__(self, path, threshold=235, maximum=255):
        self.path = path
        self.image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        if self.image.shape[2] == 4:
            self._add_white_background()
        self.gray_scale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.ret, self.threshold = cv2.threshold(self.gray_scale_image, threshold, maximum, 0)
        self.contours, self.hierarchy = cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Shows the threshold image in an Opencv2 window
    def show_threshold(self):
        cv2.imshow('Threshold Image', self.threshold)
        cv2.waitKey(0)

    # Shows the original image with contours on top in an Opencv2 window
    def show_image_with_contours(self, thickness=1):
        img_with_contours = self._get_image_with_vertices(thickness)
        cv2.imshow('Image with contours', img_with_contours)
        cv2.waitKey(0)

    # Removes all edge arrays except the largest one
    # This is a temporary solution
    def thin_contours(self, step=1):
        self.convert_contours_to_vertices()
        self._remove_corner_vertices()
        self.contours = self.contours[0:len(self.contours) - 1:step]

    # Saves either the threshold image or the original image with the contours
    def save_image(self, image_type):
        if image_type == self.ImageType.THRESHOLD:
            cv2.imwrite(f'threshold-{datetime.now().strftime("%d%m%Y%H%M%S")}.png', self.threshold)
        elif image_type == self.ImageType.CONTOUR:
            img_with_contours = self._get_image_with_vertices()
            cv2.imwrite(f'contour-{datetime.now().strftime("%d%m%Y%H%M%S")}.png', img_with_contours)

    # Method that converts the contour edges to an array of vertices
    def convert_contours_to_vertices(self):
        self.contours = np.vstack(self.contours).squeeze()

    # Returns the original image with the contours drawn over 
    # Basically deprecated   
    def _get_image_with_contours(self):
        return cv2.drawContours(self.image, self.contours, -1, (0, 0, 255), 1)

    # Returns the original image with the vertices drawn over
    def _get_image_with_vertices(self, thickness=1):
        new_img = self.image
        for point in self.contours:
            cv2.circle(new_img, (point[0], point[1]), 1, (0, 0, 255), thickness)
        return new_img

    # Private method that removes the corner vertices
    def _remove_corner_vertices(self):
        corners = []
        image_width = self.image.shape[1]
        image_height = self.image.shape[0]
        for i in range(0, len(self.contours) - 1):
            if self.contours[i][0] == 0 and self.contours[i][1] == 0:
                corners.append(i)
            if self.contours[i][0] == image_width - 1 and self.contours[i][1] == 0:
                corners.append(i)
            if self.contours[i][0] == 0 and self.contours[i][1] == image_height - 1:
                corners.append(i)
            if self.contours[i][0] == image_width - 1 and self.contours[i][1] == image_height - 1:
                corners.append(i)

        counter = 0
        for i in corners:
            self.contours = np.delete(self.contours, i - counter, axis=0)
            counter += 1

    # Private method that converts alpha channel to white background
    def _add_white_background(self):
        trans_mask = self.image[:, :, 3] == 0
        self.image[trans_mask] = [255, 255, 255, 255]
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)

    def _convex_hull(self):
        return cv2.convexHull(self.original_contours[1], False)

    # Enum for saving images
    class ImageType(Enum):
        THRESHOLD = 1
        CONTOUR = 2


def thin_vertices(points, height, width, reduce_to=1):
    points = _remove_corner_vertices(points, height, width).copy()
    return points[0: len(points) - 1: _calculate_step(len(points), reduce_to)]


def thin_vertices_convex(points, height, width, reduce_to=1):
    points = _remove_corner_vertices(points, height, width).copy()
    points = points[0: len(points) - 1: _calculate_step(len(points), reduce_to)]
    hull = _convex_hull(points)

    new_points = []
    for v in hull.vertices:
        new_points.append(points[v])

    return new_points


def _convex_hull(points):
    return scipy.spatial.ConvexHull(points)


def _remove_corner_vertices(points, height, width):
    return_points = points.copy()
    corners = []
    for point in return_points:
        if point[0] == 0 and point[1] == 0:
            corners.append(point)
        if point[0] == width - 1 and point[1] == 0:
            corners.append(point)
        if point[0] == 0 and point[1] == height - 1:
            corners.append(point)
        if point[0] == width - 1 and point[1] == height - 1:
            corners.append(point)

    for point in corners:
        return_points.remove(point)

    return return_points


def _calculate_step(num_points, num_points_desired):
    return int(num_points / num_points_desired)
