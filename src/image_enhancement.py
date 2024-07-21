import cv2
import numpy as np

def enhance_image(image, noise_reduction_level):
    # Convert the image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Splitting the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab)

    # Calculate statistics of the L channel
    mean, stddev = cv2.meanStdDev(l)
    mean_l = mean[0][0]
    stddev_l = stddev[0][0]

    # Adjust CLAHE parameters based on image statistics
    clip_limit = max(2.0, 3.0 - 2.0 * (stddev_l / 127.0))  # Adjust clip limit dynamically
    grid_size = (8, 8)  # Fixed grid size

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) on the L channel
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    cl = clahe.apply(l)

    # Merge the CLAHE enhanced L channel back with A and B channels
    enhanced_lab = cv2.merge((cl, a, b))

    # Convert back to BGR color space
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Apply Non-Local Means Denoising for color images
    h = noise_reduction_level
    hForColorComponents = h
    templateWindowSize = 7
    searchWindowSize = 21

    # Apply Non-Local Means Denoising for color images
    denoised_image = cv2.fastNlMeansDenoisingColored(enhanced_image, None, h, hForColorComponents, templateWindowSize, searchWindowSize)

    return denoised_image
