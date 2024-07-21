# main.py

import tkinter as tk
from src.gui import ImageEnhancerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
