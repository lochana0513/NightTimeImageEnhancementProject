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
        self.root.geometry("800x600")

        self.image_path = ""
        self.image = None
        self.enhanced_image = None
        self.noise_reduction_level = 10

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

        # Slider for noise reduction level
        self.slider_frame = tk.Frame(root, bg="#2b2b2b")
        self.slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.slider_label = tk.Label(self.slider_frame, text="Noise Reduction Level", font=('Helvetica', 10, 'bold'), bg="#2b2b2b", fg="white")
        self.slider_label.pack(side=tk.LEFT, padx=5)

        self.noise_reduction_slider = ttk.Scale(self.slider_frame, from_=0, to=50, orient=tk.HORIZONTAL, style="TScale", command=self.update_noise_reduction_level)
        self.noise_reduction_slider.set(self.noise_reduction_level)
        self.noise_reduction_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.image_label = tk.Label(root, bg="#2b2b2b", fg="white")
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

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

    def update_noise_reduction_level(self, value):
        self.noise_reduction_level = int(float(value))

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.display_image(self.image)
            self.enhance_button.config(state=tk.NORMAL)

    def enhance_image(self):
        if self.image is not None:
            enhanced_image = enhance_image(self.image, self.noise_reduction_level)
            self.display_image(enhanced_image)
            self.enhanced_image = enhanced_image
            self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        if self.enhanced_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                cv2.imwrite(save_path, cv2.cvtColor(self.enhanced_image, cv2.COLOR_RGB2BGR))
                messagebox.showinfo("Image Saved", f"Enhanced image saved to {save_path}")

    def display_image(self, image):
        max_width, max_height = self.image_label.winfo_width(), self.image_label.winfo_height()

        image_height, image_width = image.shape[:2]
        ratio = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * ratio), int(image_height * ratio))

        resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        self.image_label.config(image=image_tk)
        self.image_label.image = image_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
