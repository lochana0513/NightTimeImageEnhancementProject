# tests/test_image_enhancement.py

import cv2
import numpy as np
from src.image_enhancement import enhance_image

def test_enhance_image():
    # Load a sample image
    image = cv2.imread('../data/sample_images/sample_night_image.jpg')

    # Apply enhancement
    enhanced_image = enhance_image(image)

    # Check that the enhanced image is not None
    assert enhanced_image is not None

    # Check that the enhanced image has the same dimensions as the original
    assert enhanced_image.shape == image.shape

if __name__ == "__main__":
    test_enhance_image()
    print("All tests passed!")
