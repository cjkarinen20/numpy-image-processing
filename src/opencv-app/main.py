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

# cv2.imshow('Original Image', image)
# cv2.waitKey(0)

alpha = 1.2
beta = 50

adjusted = cv2.convertScaleAbs(image, alpha = alpha, beta = beta)

# cv2.imshow('Adjusted Image', adjusted)
# cv2.waitKey(0)

#-----CUSTOM-KERNELS-----

#__Sharpening_Filter__:
sharpen_kernel = np.array([[-1,-1,-1],
                           [-1, 9,-1],
                           [-1,-1,-1]])

sharpened = cv2.filter2D(image, -1, sharpen_kernel)

# cv2.imshow('Sharpened Image', sharpened)
# cv2.waitKey(0)

#__Blur_Filter__:
blur_kernel = np.array([[1,1,1],
                        [1,1,1],
                        [1,1,1]])/9

blurred = cv2.filter2D(image, -1, blur_kernel)
# cv2.imshow('Blurred Image', blurred)
# cv2.waitKey(0)

mean_values = np.mean(image, axis = (0, 1))

print(f"Mean values for R, G, B: {mean_values}")

mean_color_image = np.ones_like(image) * mean_values.astype(np.uint8)
# cv2.imshow('Mean Color Image', mean_color_image)
# cv2.waitKey(0)

#-----BOOLEAN-MASKING-----

#__Pixel_Intensity_Mask__:
threshold_value = 200

mask = np.any(image > threshold_value, axis = -1)

# cv2.imshow('Pixel Intensity Mask', mask.astype(np.uint8) * 255)
# cv2.waitKey(0)

#__Pixel_Highlight_Mask:
highlighted_image = image.copy()
highlighted_image[mask] = [255, 0, 0]
# cv2.imshow('Highlight Image', highlighted_image)
# cv2.waitKey(0)

#-----IMAGE-GUI-APPLICATION-----

def update_image(x):
    alpha = cv2.getTrackbarPos('Contrast', 'App') / 50.0
    beta = cv2.getTrackbarPos('Brightness', 'App') - 50
    apply_sharpen = cv2.getTrackbarPos('Toggle Sharpening', 'App')
    apply_mean = cv2.getTrackbarPos('Toggle Mean Color', 'App')
    apply_highlights = cv2.getTrackbarPos('Toggle Highlighting', 'App')

    output = cv2.convertScaleAbs(image, alpha = alpha, beta = beta)

    if apply_sharpen:
        output = cv2.filter2D(output, -1, sharpen_kernel)
    if apply_mean:
        mean_values = np.mean(output, axis = (0, 1))
        output = np.ones_like(output) * mean_values.astype(np.uint8)
    if apply_highlights:
        mask = np.any(output > threshold_value, axis = -1)
        output[mask] = [255, 0, 0]
    
    cv2.imshow('App', output)

cv2.namedWindow('App')
cv2.resizeWindow('App', 500, 400)
cv2.createTrackbar('Brightness', 'App', 50, 100, update_image)
cv2.createTrackbar('Contrast', 'App', 50, 100, update_image)
cv2.createTrackbar('Toggle Sharpening', 'App', 0, 1, update_image)
cv2.createTrackbar('Toggle Mean Color', 'App', 0, 1, update_image)
cv2.createTrackbar('Toggle Highlighting', 'App', 0, 1, update_image)

cv2.imshow('App', image)
cv2.waitKey(0)
cv2.destroyAllWindows()