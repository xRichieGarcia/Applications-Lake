import sys
sys.path.insert(0, 'venv/local/lib/python2.7/dist-packages')
import cv2
import numpy as np

""" This worked with local images. Replace with images from s3 bucket
"""
img_array = []
img = cv2.imread('img1.jpg')
height, width, layers = img.shape
size = (width,height)

img_array.append(img)

img = cv2.imread('img2.jpg')
img_array.append(img)

out = cv2.VideoWriter('example.avi',cv2.VideoWriter_fourcc(*'MJPG'), 1, size)