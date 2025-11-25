import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox
from PIL import Image, ImageTk
import os
from sklearn.cluster import KMeans

class ColorReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Reduction Tool")
        self.root.geometry("900x650")
        self.root.configure(bg='#f8f9fa')
        
        # Modern color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#3498db',
            'success': '#27ae60',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        
        self.setup_styles()
        
        self.image_path = None
        self.processed_image = None
        self.original_image = None
        self.selected_colors = []
        self.dominant_colors = None
        
        # Main container
        main_container = ttk.Frame(root, style='Card.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="Color Reduction Tool", 
                              font=('Segoe UI', 18, 'bold'), 
                              fg=self.colors['primary'],
                              bg=self.colors['light'])
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(header_frame, text="3D Printing Filament Planning", 
                                 font=('Segoe UI', 10), 
                                 fg=self.colors['secondary'],
                                 bg=self.colors['light'])
        subtitle_label.pack(pady=(0, 5))
        
        # Tabs with modern style
        tab_style = ttk.Style()
        tab_style.configure('Modern.TNotebook', background=self.colors['light'], borderwidth=0)
        tab_style.configure('Modern.TNotebook.Tab', font=('Segoe UI', 10, 'bold'), 
                           padding=[20, 8], background=self.colors['light'])
        
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Auto Mode Tab
        self.auto_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.auto_frame, text="Auto Reduction")
        self.setup_auto_mode()
        
        # 3D Printing Mode Tab
        self.print_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.print_frame, text="3D Printing")
        self.setup_print_mode()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(main_container, textvariable=self.status_var,
                             font=('Segoe UI', 9), bg=self.colors['dark'],
                             fg='white', anchor=tk.W, padx=10)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles
        style.configure('Card.TFrame', background=self.colors['light'])
        style.configure('Modern.TButton', font=('Segoe UI', 9), padding=(12, 6))
        style.configure('Accent.TButton', font=('Segoe UI', 9, 'bold'), 
                       background=self.colors['accent'], foreground='white')
        style.map('Accent.TButton', background=[('active', '#2980b9')])
        style.configure('TCombobox', font=('Segoe UI', 9))
        style.configure('TLabel', background=self.colors['light'], font=('Segoe UI', 9))
    
    def setup_auto_mode(self):
        # Control panel
        control_frame = ttk.Frame(self.auto_frame, style='Card.TFrame')
        control_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Compact control row
        left_controls = ttk.Frame(control_frame, style='Card.TFrame')
        left_controls.pack(side=tk.LEFT)
        
        ttk.Label(left_controls, text="Colors:").pack(side=tk.LEFT, padx=(0, 5))
        self.auto_color_count = ttk.Combobox(left_controls, 
                                           values=list(range(1, 13)), 
                                           width=6, state="readonly")
        self.auto_color_count.pack(side=tk.LEFT, padx=(0, 15))
        self.auto_color_count.set('5')
        
        # Buttons
        btn_frame = ttk.Frame(control_frame, style='Card.TFrame')
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Upload", command=self.upload_image,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="Process", command=self.process_auto_image,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="Save", command=self.download_image,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=3)
        
        # Image display - compact side by side
        image_frame = ttk.Frame(self.auto_frame, style='Card.TFrame')
        image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Original image
        orig_container = ttk.Frame(image_frame, style='Card.TFrame')
        orig_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(orig_container, text="Original", font=('Segoe UI', 10, 'bold')).pack(pady=5)
        self.auto_orig_label = tk.Label(orig_container, bg='white', relief='solid', bd=1,
                                       text="No image loaded\n\nClick Upload to begin",
                                       font=('Segoe UI', 9), fg='gray', justify=tk.CENTER)
        self.auto_orig_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Processed image
        proc_container = ttk.Frame(image_frame, style='Card.TFrame')
        proc_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(proc_container, text="Processed", font=('Segoe UI', 10, 'bold')).pack(pady=5)
        self.auto_proc_label = tk.Label(proc_container, bg='white', relief='solid', bd=1,
                                       text="Processed image\nwill appear here",
                                       font=('Segoe UI', 9), fg='gray', justify=tk.CENTER)
        self.auto_proc_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def setup_print_mode(self):
        main_frame = ttk.Frame(self.print_frame, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left panel - compact controls
        left_panel = ttk.Frame(main_frame, style='Card.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Color selection
        color_group = ttk.LabelFrame(left_panel, text=" Filament Colors ", 
                                   style='Card.TFrame', padding=10)
        color_group.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(color_group, text="Number of colors:").pack(anchor=tk.W)
        self.print_color_count = ttk.Combobox(color_group, 
                                            values=list(range(1, 9)), 
                                            width=12, state="readonly")
        self.print_color_count.pack(fill=tk.X, pady=5)
        self.print_color_count.set('3')
        self.print_color_count.bind("<<ComboboxSelected>>", self.create_color_selectors)
        
        self.color_select_frame = ttk.Frame(color_group, style='Card.TFrame')
        self.color_select_frame.pack(fill=tk.X, pady=5)
        
        # Action buttons
        action_group = ttk.LabelFrame(left_panel, text=" Actions ", 
                                    style='Card.TFrame', padding=10)
        action_group.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_group, text="Upload Image", 
                  command=self.upload_image, style='Modern.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(action_group, text="Analyze Colors", 
                  command=self.analyze_image_colors, style='Accent.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(action_group, text="Process", 
                  command=self.process_print_image, style='Modern.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(action_group, text="Save Result", 
                  command=self.download_image, style='Modern.TButton').pack(fill=tk.X, pady=2)
        
        # Color previews
        preview_group = ttk.LabelFrame(left_panel, text=" Preview ", 
                                     style='Card.TFrame', padding=10)
        preview_group.pack(fill=tk.X, pady=10)
        
        ttk.Label(preview_group, text="Your Colors:").pack(anchor=tk.W)
        self.palette_canvas = tk.Canvas(preview_group, height=25, bg='white', 
                                      relief='solid', bd=1, highlightthickness=0)
        self.palette_canvas.pack(fill=tk.X, pady=(2, 10))
        
        ttk.Label(preview_group, text="Image Colors:").pack(anchor=tk.W)
        self.dominant_canvas = tk.Canvas(preview_group, height=25, bg='white', 
                                       relief='solid', bd=1, highlightthickness=0)
        self.dominant_canvas.pack(fill=tk.X, pady=(2, 5))
        
        # Right panel - images
        right_panel = ttk.Frame(main_frame, style='Card.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Original image
        orig_group = ttk.LabelFrame(right_panel, text=" Original Image ", 
                                  style='Card.TFrame', padding=10)
        orig_group.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.print_orig_label = tk.Label(orig_group, bg='white', relief='solid', bd=1,
                                       text="No image loaded\n\nClick Upload to begin",
                                       font=('Segoe UI', 9), fg='gray', justify=tk.CENTER)
        self.print_orig_label.pack(fill=tk.BOTH, expand=True)
        
        # Processed image
        proc_group = ttk.LabelFrame(right_panel, text=" 3D Print Simulation ", 
                                  style='Card.TFrame', padding=10)
        proc_group.pack(fill=tk.BOTH, expand=True)
        
        self.print_proc_label = tk.Label(proc_group, bg='white', relief='solid', bd=1,
                                       text="Processed image\nwill appear here",
                                       font=('Segoe UI', 9), fg='gray', justify=tk.CENTER)
        self.print_proc_label.pack(fill=tk.BOTH, expand=True)
        
        self.create_color_selectors()
    
    def create_color_selectors(self, event=None):
        for widget in self.color_select_frame.winfo_children():
            widget.destroy()
        
        color_count = int(self.print_color_count.get())
        self.selected_colors = []
        
        for i in range(color_count):
            frame = ttk.Frame(self.color_select_frame, style='Card.TFrame')
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=f"Color {i+1}:", width=8).pack(side=tk.LEFT)
            btn = ttk.Button(frame, text="Choose", 
                           command=lambda idx=i: self.pick_color(idx),
                           style='Modern.TButton', width=8)
            btn.pack(side=tk.LEFT, padx=2)
            
            preview = tk.Canvas(frame, width=25, height=20, bg='white', 
                              relief='solid', bd=1, highlightthickness=0)
            preview.pack(side=tk.LEFT)
            
            self.selected_colors.append({
                'button': btn,
                'preview': preview,
                'color': None
            })
        
        self.update_palette_preview()
    
    def pick_color(self, index):
        color = colorchooser.askcolor(title=f"Choose Filament Color {index+1}")
        if color[0]:
            rgb = tuple(map(int, color[0]))
            self.selected_colors[index]['color'] = rgb
            hex_color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            self.selected_colors[index]['preview'].configure(bg=hex_color)
            self.update_palette_preview()
    
    def update_palette_preview(self):
        self.palette_canvas.delete("all")
        colors = [c['color'] for c in self.selected_colors if c['color'] is not None]
        
        if not colors:
            self.palette_canvas.create_text(75, 12, text="No colors selected", 
                                          fill="gray", font=('Segoe UI', 8))
            return
        
        width = self.palette_canvas.winfo_width() or 150
        seg_width = width / len(colors)
        
        for i, color in enumerate(colors):
            hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            x0, x1 = i * seg_width, (i + 1) * seg_width
            self.palette_canvas.create_rectangle(x0, 0, x1, 25, fill=hex_color, outline="")
    
    def analyze_image_colors(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        
        self.status_var.set("Analyzing image colors...")
        self.root.update()
        
        try:
            color_count = int(self.print_color_count.get())
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize for processing
            h, w = image.shape[:2]
            if w * h > 1000000:
                scale = (1000000 / (w * h)) ** 0.5
                new_w, new_h = int(w * scale), int(h * scale)
                image = cv2.resize(image, (new_w, new_h))
            
            pixels = image.reshape(-1, 3)
            
            kmeans = KMeans(n_clusters=color_count, random_state=42, n_init=10)
            kmeans.fit(pixels)
            self.dominant_colors = kmeans.cluster_centers_.astype(int)
            
            self.display_dominant_colors()
            self.status_var.set(f"Found {color_count} color regions")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_var.set("Analysis failed")
    
    def display_dominant_colors(self):
        self.dominant_canvas.delete("all")
        
        if self.dominant_colors is None or len(self.dominant_colors) == 0:
            self.dominant_canvas.create_text(75, 12, text="Analyze image first", 
                                           fill="gray", font=('Segoe UI', 8))
            return
        
        width = self.dominant_canvas.winfo_width() or 150
        seg_width = width / len(self.dominant_colors)
        
        for i, color in enumerate(self.dominant_colors):
            hex_color = f'#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}'
            x0, x1 = i * seg_width, (i + 1) * seg_width
            self.dominant_canvas.create_rectangle(x0, 0, x1, 25, fill=hex_color, outline="")
    
    def calculate_luminosity(self, rgb):
        r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def get_color_mapping(self, user_colors):
        if self.dominant_colors is None or len(self.dominant_colors) == 0:
            return {}
        
        dom_lum = [(self.calculate_luminosity(color), color) for color in self.dominant_colors]
        user_lum = [(self.calculate_luminosity(color), color) for color in user_colors]
        
        dom_sorted = sorted(dom_lum, key=lambda x: x[0])
        user_sorted = sorted(user_lum, key=lambda x: x[0])
        
        mapping = {}
        for i, (dom_l, dom_color) in enumerate(dom_sorted):
            if i < len(user_sorted):
                mapping[tuple(dom_color)] = user_sorted[i][1]
        
        return mapping
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        
        if file_path:
            self.image_path = file_path
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            
            img = Image.open(file_path)
            self.original_image = np.array(img)
            
            display_img = img.copy()
            display_img.thumbnail((350, 350))
            img_tk = ImageTk.PhotoImage(display_img)
            
            # Update both tabs
            for label in [self.auto_orig_label, self.print_orig_label]:
                label.config(image=img_tk, text="")
                label.image = img_tk
    
    def process_auto_image(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        
        self.status_var.set("Processing image...")
        self.root.update()
        
        try:
            color_count = int(self.auto_color_count.get())
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize if large
            h, w = image.shape[:2]
            if w * h > 1000000:
                scale = (1000000 / (w * h)) ** 0.5
                new_w, new_h = int(w * scale), int(h * scale)
                image = cv2.resize(image, (new_w, new_h))
            
            pixels = image.reshape(-1, 3)
            
            kmeans = KMeans(n_clusters=color_count, random_state=42, n_init=10)
            kmeans.fit(pixels)
            new_colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            reduced_image = new_colors[labels].reshape(image.shape)
            
            self.processed_image = reduced_image
            self.display_processed_image(reduced_image, "auto")
            self.status_var.set(f"Reduced to {color_count} colors")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            self.status_var.set("Processing failed")
    
    def process_print_image(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        
        user_colors = [c['color'] for c in self.selected_colors if c['color'] is not None]
        if not user_colors:
            messagebox.showwarning("No Colors", "Please select filament colors first.")
            return
        
        # FIXED: Proper check for dominant_colors
        if self.dominant_colors is None or len(self.dominant_colors) == 0:
            messagebox.showwarning("No Analysis", "Please analyze image colors first.")
            return
        
        self.status_var.set("Processing with filament colors...")
        self.root.update()
        
        try:
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize if large
            h, w = image.shape[:2]
            if w * h > 1000000:
                scale = (1000000 / (w * h)) ** 0.5
                new_w, new_h = int(w * scale), int(h * scale)
                image = cv2.resize(image, (new_w, new_h))
            
            pixels = image.reshape(-1, 3)
            
            # Get color mapping
            color_mapping = self.get_color_mapping(user_colors)
            
            # Find closest dominant color for each pixel
            dom_palette = np.array(self.dominant_colors)
            distances = np.linalg.norm(pixels[:, None] - dom_palette[None, :], axis=2)
            labels = np.argmin(distances, axis=1)
            
            # Map to user colors
            reduced_pixels = np.zeros_like(pixels)
            for i, label in enumerate(labels):
                dom_color = tuple(dom_palette[label])
                if dom_color in color_mapping:
                    reduced_pixels[i] = color_mapping[dom_color]
                else:
                    reduced_pixels[i] = dom_color
            
            reduced_image = reduced_pixels.reshape(image.shape)
            
            self.processed_image = reduced_image
            self.display_processed_image(reduced_image, "print")
            self.status_var.set("3D print simulation complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            self.status_var.set("Processing failed")
    
    def display_processed_image(self, processed_image, mode):
        img = Image.fromarray(processed_image.astype(np.uint8))
        display_img = img.copy()
        display_img.thumbnail((350, 350))
        img_tk = ImageTk.PhotoImage(display_img)
        
        if mode == "auto":
            self.auto_proc_label.config(image=img_tk, text="")
            self.auto_proc_label.image = img_tk
        else:
            self.print_proc_label.config(image=img_tk, text="")
            self.print_proc_label.image = img_tk
    
    def download_image(self):
        if self.processed_image is None:
            messagebox.showwarning("No Image", "No processed image to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        
        if file_path:
            try:
                Image.fromarray(self.processed_image.astype(np.uint8)).save(file_path)
                messagebox.showinfo("Success", f"Image saved:\n{file_path}")
                self.status_var.set("Image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorReductionApp(root)
    root.mainloop()