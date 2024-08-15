import cv2
import numpy as np

def auto_correct_image(image):
    # Auto-calculating optimal noise reduction, brightness, contrast, and saturation
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate the noise level based on the variance of the Laplacian (high variance means less noise)
    noise_variance = cv2.Laplacian(gray_image, cv2.CV_64F).var()
    if noise_variance < 50:  # lower variance suggests more noise
        noise_reduction_level = 30
    else:
        noise_reduction_level = 10

    # Calculate brightness and contrast
    mean_brightness = np.mean(gray_image)
    brightness = 1.0 + (128 - mean_brightness) / 128  # normalize brightness around 128
    contrast = 1.2 if mean_brightness < 100 else 0.8 if mean_brightness > 150 else 1.0

    # Calculate saturation based on the mean saturation of the image
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mean_saturation = np.mean(hsv_image[:, :, 1])
    saturation = 1.2 if mean_saturation < 100 else 0.8 if mean_saturation > 150 else 1.0

    return noise_reduction_level, brightness, contrast, saturation

def enhance_image(image, noise_reduction_level=None, brightness=None, contrast=None, saturation=None):
    # If any value is not provided, auto-correct it
    if noise_reduction_level is None or brightness is None or contrast is None or saturation is None:
        noise_reduction_level, brightness, contrast, saturation = auto_correct_image(image)
    
    enhanced_image = image.copy()

    # Denoise image
    if noise_reduction_level > 0:
        enhanced_image = cv2.fastNlMeansDenoisingColored(enhanced_image, None, noise_reduction_level, noise_reduction_level, 7, 21)

    # Adjust brightness
    if brightness != 1.0:
        hsv = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
        hsv = np.array(hsv, dtype=np.float64)
        hsv[:, :, 2] = hsv[:, :, 2] * brightness
        hsv[:, :, 2][hsv[:, :, 2] > 255] = 255
        hsv = np.array(hsv, dtype=np.uint8)
        enhanced_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Adjust contrast
    if contrast != 1.0:
        f = 131 * (contrast - 1) / 127 + 1
        alpha_c = f
        gamma_c = 127 * (1 - f)
        enhanced_image = cv2.addWeighted(enhanced_image, alpha_c, enhanced_image, 0, gamma_c)

    # Adjust saturation
    if saturation != 1.0:
        hsv = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
        hsv = np.array(hsv, dtype=np.float64)
        hsv[:, :, 1] = hsv[:, :, 1] * saturation
        hsv[:, :, 1][hsv[:, :, 1] > 255] = 255
        hsv = np.array(hsv, dtype=np.uint8)
        enhanced_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return enhanced_image
