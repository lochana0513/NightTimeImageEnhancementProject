import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from src.image_enhancement import enhance_image

class ImageEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Night-time Image Enhancer")
        self.root.geometry("1200x600")

        self.image_path = ""
        self.image = None
        self.enhanced_image = None
        self.noise_reduction_level = 10
        self.brightness = 1.0
        self.contrast = 1.0
        self.saturation = 1.0

        self.root.configure(bg="#2b2b2b")

        # Title Label
        self.title_label = tk.Label(root, text="Night-time Image Enhancer", font=('Helvetica', 18, 'bold'), bg="#2b2b2b", fg="white")
        self.title_label.pack(pady=20)

        # Frame for buttons
        self.button_frame = tk.Frame(root, bg="#2b2b2b")
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.load_button = self.create_rounded_button(self.button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.enhance_button = self.create_rounded_button(self.button_frame, text="Enhance Image", command=self.enhance_image, state=tk.DISABLED)
        self.enhance_button.pack(side=tk.LEFT, padx=5)

        self.save_button = self.create_rounded_button(self.button_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Create and configure style for ttk widgets
        style = ttk.Style()
        style.configure("TScale", background="#2b2b2b", foreground="white", troughcolor="#444444", sliderthickness=15)
        style.map("TScale",
                  background=[('active', '#1E90FF')],
                  foreground=[('active', 'white')])

        # Frame for sliders
        self.slider_frame = tk.Frame(root, bg="#2b2b2b")
        self.slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Slider for noise reduction level
        self.noise_label = tk.Label(self.slider_frame, text="Noise Reduction Level", font=('Helvetica', 10, 'bold'), bg="#2b2b2b", fg="white")
        self.noise_label.grid(row=0, column=0, padx=5, pady=5)
        self.noise_slider = ttk.Scale(self.slider_frame, from_=0, to=50, orient=tk.HORIZONTAL, style="TScale", command=self.update_image)
        self.noise_slider.set(self.noise_reduction_level)
        self.noise_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Slider for brightness
        self.brightness_label = tk.Label(self.slider_frame, text="Brightness", font=('Helvetica', 10, 'bold'), bg="#2b2b2b", fg="white")
        self.brightness_label.grid(row=1, column=0, padx=5, pady=5)
        self.brightness_slider = ttk.Scale(self.slider_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, style="TScale", command=self.update_image)
        self.brightness_slider.set(self.brightness)
        self.brightness_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Slider for contrast
        self.contrast_label = tk.Label(self.slider_frame, text="Contrast", font=('Helvetica', 10, 'bold'), bg="#2b2b2b", fg="white")
        self.contrast_label.grid(row=2, column=0, padx=5, pady=5)
        self.contrast_slider = ttk.Scale(self.slider_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, style="TScale", command=self.update_image)
        self.contrast_slider.set(self.contrast)
        self.contrast_slider.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Slider for saturation
        self.saturation_label = tk.Label(self.slider_frame, text="Saturation", font=('Helvetica', 10, 'bold'), bg="#2b2b2b", fg="white")
        self.saturation_label.grid(row=3, column=0, padx=5, pady=5)
        self.saturation_slider = ttk.Scale(self.slider_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, style="TScale", command=self.update_image)
        self.saturation_slider.set(self.saturation)
        self.saturation_slider.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.slider_frame.columnconfigure(1, weight=1)

        # Frame for images
        self.image_frame = tk.Frame(root, bg="#2b2b2b")
        self.image_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Labels for original and enhanced images
        self.original_image_label = tk.Label(self.image_frame, bg="#2b2b2b", fg="white")
        self.original_image_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.enhanced_image_label = tk.Label(self.image_frame, bg="#2b2b2b", fg="white")
        self.enhanced_image_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

    def create_rounded_button(self, parent, text, command, state=tk.NORMAL):
        button_canvas = tk.Canvas(parent, width=150, height=40, bg="#2b2b2b", bd=0, highlightthickness=0, relief='ridge')
        button_canvas.pack_propagate(False)

        def round_rectangle(x1, y1, x2, y2, r=25, **kwargs):
            points = [x1+r, y1,
                      x1+r, y1,
                      x2-r, y1,
                      x2-r, y1,
                      x2, y1,
                      x2, y1+r,
                      x2, y1+r,
                      x2, y2-r,
                      x2, y2-r,
                      x2, y2,
                      x2-r, y2,
                      x2-r, y2,
                      x1+r, y2,
                      x1+r, y2,
                      x1, y2,
                      x1, y2-r,
                      x1, y2-r,
                      x1, y1+r,
                      x1, y1+r,
                      x1, y1]
            return button_canvas.create_polygon(points, **kwargs, smooth=True)

        button_id = round_rectangle(5, 5, 145, 35, r=20, fill="#1E90FF", outline="#1E90FF")

        button_canvas.tag_bind(button_id, "<ButtonPress-1>", lambda event: command())

        button_text = button_canvas.create_text(75, 20, text=text, fill="white", font=('Helvetica', 10, 'bold'))
        button_canvas.tag_bind(button_text, "<ButtonPress-1>", lambda event: command())

        button_canvas.config(state=state)

        return button_canvas

    def update_image(self, _=None):
        self.noise_reduction_level = int(float(self.noise_slider.get()))
        self.brightness = float(self.brightness_slider.get())
        self.contrast = float(self.contrast_slider.get())
        self.saturation = float(self.saturation_slider.get())
        if self.image is not None:
            enhanced_image = enhance_image(self.image, self.noise_reduction_level, self.brightness, self.contrast, self.saturation)
            self.display_image(enhanced_image, original=False)
            self.enhanced_image = enhanced_image

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.display_image(self.image, original=True)
            self.enhance_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)

            # Automatically enhance the image with initial values
            self.enhanced_image = enhance_image(self.image, self.noise_reduction_level, self.brightness, self.contrast, self.saturation)
            self.display_image(self.enhanced_image, original=False)

    def enhance_image(self):
        if self.image is not None:
            enhanced_image = enhance_image(self.image, self.noise_reduction_level, self.brightness, self.contrast, self.saturation)
            self.display_image(enhanced_image, original=False)
            self.enhanced_image = enhanced_image
            self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        if self.enhanced_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                cv2.imwrite(save_path, self.enhanced_image)
                messagebox.showinfo("Image Saved", f"Image saved successfully at {save_path}")

    def display_image(self, image, original=True):
        max_size = (500, 500)
        image_resized = cv2.resize(image, max_size, interpolation=cv2.INTER_AREA)

        image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(pil_image)

        if original:
            self.original_image_label.config(image=tk_image)
            self.original_image_label.image = tk_image
        else:
            self.enhanced_image_label.config(image=tk_image)
            self.enhanced_image_label.image = tk_image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
