import cv2
import numpy as np

def enhance_image(image):
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
    
    # Convert to grayscale for median intensity calculation
    gray_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    
    # Calculate median pixel intensity of the image
    median_intensity = np.median(gray_image)
    
    # Calculate bilateral filter parameters based on median intensity
    d = int(max(1, 10 - 3 * (median_intensity / 127.0)))  # Adjust diameter dynamically
    sigma_color = 75  # Fixed sigma color
    sigma_space = 75  # Fixed sigma space
    
    # Apply bilateral filter for denoising while preserving edges
    denoised_image = cv2.bilateralFilter(enhanced_image, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)
    
    # Apply color retouching to enhance colors without damaging natural tones
    enhanced_smoothed_image = cv2.addWeighted(enhanced_image, 0.8, denoised_image, 0.2, 0)
    
    return enhanced_smoothed_image
