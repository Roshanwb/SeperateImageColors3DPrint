import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox
from PIL import Image, ImageTk, ImageOps
import os
from sklearn.cluster import KMeans

class ColorReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Color Reduction")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        self.image_path = None
        self.processed_image = None
        self.selected_colors = []
        
        style = ttk.Style()
        style.configure("TNotebook", background="#f8f9fa", borderwidth=0)
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TButton", padding=6, font=("Arial", 10), background="#4CAF50", foreground="black")
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TLabel", background="#f8f9fa", font=("Arial", 10))
        style.configure("TCombobox", font=("Arial", 10))

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Auto Mode
        self.auto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.auto_frame, text="Auto Mode")
        self.setup_auto_mode()
        
        # Manual Mode
        self.manual_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.manual_frame, text="Manual Mode")
        self.setup_manual_mode()
    
    def setup_auto_mode(self):
        frame = ttk.Frame(self.auto_frame)
        frame.pack(fill=tk.X, pady=10)

        ttk.Label(frame, text="Select Number of Colors:").pack(side=tk.LEFT, padx=10)
        self.auto_color_count = ttk.Combobox(frame, values=[1, 2, 3, 4, 5, 6], state="readonly")
        self.auto_color_count.pack(side=tk.LEFT)
        self.auto_color_count.current(2)
        
        ttk.Button(frame, text="Upload Image", command=self.upload_image).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="Process Image", command=self.process_auto_image).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="Download Image", command=self.download_image).pack(side=tk.LEFT, padx=10)
        
        self.auto_image_label = ttk.Label(self.auto_frame)
        self.auto_image_label.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def setup_manual_mode(self):
        frame = ttk.Frame(self.manual_frame)
        frame.pack(fill=tk.X, pady=10)

        ttk.Label(frame, text="Select Number of Colors:").pack(side=tk.LEFT, padx=10)
        self.manual_color_count = ttk.Combobox(frame, values=[1, 2, 3, 4, 5, 6], state="readonly")
        self.manual_color_count.pack(side=tk.LEFT)
        self.manual_color_count.current(2)
        self.manual_color_count.bind("<<ComboboxSelected>>", self.create_color_selectors)
        
        self.color_select_frame = ttk.Frame(self.manual_frame)
        self.color_select_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame, text="Upload Image", command=self.upload_image).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="Process Image", command=self.process_manual_image).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="Download Image", command=self.download_image).pack(side=tk.LEFT, padx=10)
        
        self.manual_image_label = ttk.Label(self.manual_frame)
        self.manual_image_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.displayed_image = ImageTk.PhotoImage(img)
            
            if self.notebook.index(self.notebook.select()) == 0:
                self.auto_image_label.config(image=self.displayed_image)
            else:
                self.manual_image_label.config(image=self.displayed_image)
    
    def process_auto_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return
        
        color_count = int(self.auto_color_count.get())
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixels = image.reshape((-1, 3))
        
        kmeans = KMeans(n_clusters=color_count, random_state=42, n_init=10)
        kmeans.fit(pixels)
        new_colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        reduced_image = new_colors[labels].reshape(image.shape)
        
        self.display_processed_image(reduced_image)
    
    def create_color_selectors(self, event):
        for widget in self.color_select_frame.winfo_children():
            widget.destroy()
        
        self.selected_colors = []
        for i in range(int(self.manual_color_count.get())):
            btn = ttk.Button(self.color_select_frame, text=f"Select Color {i+1}", command=lambda i=i: self.pick_color(i))
            btn.pack(side=tk.LEFT, padx=5)
            self.selected_colors.append((btn, None))
    
    def pick_color(self, index):
        color_code = colorchooser.askcolor()[0]
        if color_code:
            self.selected_colors[index] = (self.selected_colors[index][0], tuple(map(int, color_code)))
    
    def process_manual_image(self):
        if not self.image_path or not self.selected_colors:
            messagebox.showerror("Error", "Please upload an image and select colors first.")
            return
        
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixels = image.reshape((-1, 3))
        
        color_palette = np.array([c[1] for c in self.selected_colors if c[1] is not None])
        if len(color_palette) == 0:
            messagebox.showerror("Error", "Please select valid colors.")
            return
        
        distances = np.linalg.norm(pixels[:, None] - color_palette[None, :], axis=2)
        labels = np.argmin(distances, axis=1)
        reduced_image = color_palette[labels].reshape(image.shape)
        
        self.display_processed_image(reduced_image)
    
    def display_processed_image(self, processed_image):
        self.processed_image = processed_image
        img = Image.fromarray(processed_image.astype(np.uint8))
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        
        if self.notebook.index(self.notebook.select()) == 0:
            self.auto_image_label.config(image=img_tk)
            self.auto_image_label.image = img_tk
        else:
            self.manual_image_label.config(image=img_tk)
            self.manual_image_label.image = img_tk
    
    def download_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No processed image available.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg")])
        if file_path:
            Image.fromarray(self.processed_image.astype(np.uint8)).save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorReductionApp(root)
    root.mainloop()