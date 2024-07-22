import cv2
import numpy as np

def enhance_image(image, noise_reduction_level, brightness, contrast, saturation):
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
