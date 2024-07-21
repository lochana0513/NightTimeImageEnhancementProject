# NightTimeImageEnhancementProject

## Overview

The NightTimeImageEnhancementProject is a Python application designed to enhance night-time images by reducing noise, adjusting colors, and improving overall image quality. The project uses Tkinter for the graphical user interface (GUI) and OpenCV for image processing.

## Features

- **Noise Reduction**: Improve image quality by removing noise from night-time images.
- **Color Adjustment**: Adjust the colors to enhance image visibility.
- **Image Quality Improvement**: General improvements to enhance the visual appeal of night-time images.

## Installation

### Prerequisites

Ensure you have Python 3.x installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

### Setup



2. **Create a Virtual Environment**

   It's a good practice to use a virtual environment to manage dependencies.

   python -m venv venv

3. **Activate the Virtual Environment**

   - **Windows:**

     venv\Scripts\activate

   - **macOS/Linux:**

     source venv/bin/activate

4. **Install Dependencies**

   pip install -r requirements.txt

5. **Run the Application**

   python main.py

## Usage

1. **Launch the GUI**

   After running the application, a GUI window will open. You can use this window to load night-time images and apply enhancement algorithms.

2. **Enhance Images**

   - Click on the 'Load Image' button to select an image file.
   - Adjust settings as needed and click 'Enhance Image' to process the image.

3. **Save Enhanced Image**

   Once the enhancement is complete, you can save the enhanced image by clicking on the 'Save Image' button.

## Development

### Adding New Features

To add new features or enhance existing functionality, modify the code in the `image_processing.py` and `gui.py` files.

### Running Tests

Ensure your tests are up-to-date and run them to validate changes.

pytest

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to the existing style and includes tests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries or issues, please contact Adith at your.email@example.com.
