import numpy as np
import cv2
import os

images_dir = os.path.dirname(__file__)
image_path = "images/image.png"
abs_file_path = os.path.join(images_dir, image_path)

image = cv2.imread(abs_file_path)
# print(image)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# print(image)

# cv2.imshow('Original image', image)
# cv2.waitKey(0)

alpha = 1.2
beta = 50

adjusted = cv2.convertScaleAbs(image, alpha = alpha, beta = beta)

cv2.imshow('Adjusted image', adjusted)
cv2.waitKey(0)