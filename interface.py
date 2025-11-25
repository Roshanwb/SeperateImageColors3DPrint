import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from pathlib import Path
from typing import List, Optional
import numpy as np
from PIL import Image, ImageTk

from domain import RGBColor, ColorPalette
from infrastructure import ImageRepository, ColorAnalyzer
from application import ColorReductionService

class ModernColorReductionApp:
    """Modern, professional GUI with clean architecture"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Color Reduction Pro")
        self.root.geometry("900x650")
        self.root.configure(bg='#f8f9fa')
        
        # Initialize architecture layers
        self.image_repo = ImageRepository()
        self.color_analyzer = ColorAnalyzer()
        self.color_service = ColorReductionService(self.color_analyzer)
        
        # Application state
        self.current_image = None
        self.processed_image = None
        self.selected_colors: List[RGBColor] = []
        self.color_previews = []  # Store preview canvas references
        
        self.setup_styles()
        self.create_interface()
    
    def setup_styles(self):
        """Configure modern, professional styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Clean, modern color scheme
        style.configure('TFrame', background='#f8f9fa')
        style.configure('TLabel', background='#f8f9fa', font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9), padding=(10, 5))
        style.configure('Primary.TButton', background='#007acc', foreground='white')
        style.map('Primary.TButton', background=[('active', '#005a9e')])
        style.configure('TCombobox', font=('Segoe UI', 9))
        style.configure('TNotebook', background='#f8f9fa')
        style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=(15, 8))
    
    def create_interface(self):
        """Create clean, professional interface"""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title = tk.Label(header, text="Color Reduction Pro", 
                        font=('Segoe UI', 18, 'bold'), 
                        fg='white', bg='#2c3e50')
        title.pack(pady=15)
        
        subtitle = tk.Label(header, text="Professional Color Processing for 3D Printing", 
                           font=('Segoe UI', 10), 
                           fg='#bdc3c7', bg='#2c3e50')
        subtitle.pack()
        
        # Main content
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_auto_tab()
        self.setup_manual_tab()
        
        # Status bar
        self.status = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status,
                            font=('Segoe UI', 9), bg='#34495e', fg='white',
                            anchor=tk.W, padx=10)
        status_bar.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    def setup_auto_tab(self):
        """Auto color reduction tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Auto Reduction")
        
        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(controls, text="Colors:").pack(side=tk.LEFT)
        self.auto_count = ttk.Combobox(controls, values=list(range(1, 13)), 
                                      width=8, state="readonly")
        self.auto_count.pack(side=tk.LEFT, padx=10)
        self.auto_count.set('6')
        
        ttk.Button(controls, text="Upload Image", 
                  command=self.upload_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Process", 
                  command=self.process_auto, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Save", 
                  command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Image display
        self.setup_image_display(frame, "auto")
    
    def setup_manual_tab(self):
        """3D Printing mode tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="3D Printing")
        
        # Left panel - controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Color selection
        color_frame = ttk.LabelFrame(left_panel, text="Filament Colors", padding=10)
        color_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(color_frame, text="Color count:").pack(anchor=tk.W)
        self.manual_count = ttk.Combobox(color_frame, values=list(range(1, 9)), 
                                       state="readonly")
        self.manual_count.pack(fill=tk.X, pady=5)
        self.manual_count.set('4')
        self.manual_count.bind("<<ComboboxSelected>>", self.update_color_selectors)
        
        self.color_selector_frame = ttk.Frame(color_frame)
        self.color_selector_frame.pack(fill=tk.X, pady=5)
        
        # Actions
        action_frame = ttk.LabelFrame(left_panel, text="Processing", padding=10)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Upload Image", 
                  command=self.upload_image).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="Analyze Colors", 
                  command=self.analyze_colors, style='Primary.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="Process", 
                  command=self.process_manual).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="Save", 
                  command=self.save_image).pack(fill=tk.X, pady=2)
        
        # Color previews
        preview_frame = ttk.LabelFrame(left_panel, text="Color Preview", padding=10)
        preview_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(preview_frame, text="Your colors:").pack(anchor=tk.W)
        self.selected_canvas = tk.Canvas(preview_frame, height=25, bg='white', 
                                       relief='solid', bd=1)
        self.selected_canvas.pack(fill=tk.X, pady=2)
        
        ttk.Label(preview_frame, text="Image colors:").pack(anchor=tk.W, pady=(10, 0))
        self.dominant_canvas = tk.Canvas(preview_frame, height=25, bg='white', 
                                       relief='solid', bd=1)
        self.dominant_canvas.pack(fill=tk.X, pady=2)
        
        # Right panel - images
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_image_display(right_panel, "manual")
        
        self.update_color_selectors()
    
    def setup_image_display(self, parent, mode: str):
        """Setup image display area"""
        # Original
        orig_frame = ttk.LabelFrame(parent, text="Original Image", padding=10)
        orig_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        orig_label = tk.Label(orig_frame, bg='white', relief='solid', bd=1,
                            text="Upload an image to begin", justify=tk.CENTER,
                            font=('Segoe UI', 10), fg='gray')
        orig_label.pack(fill=tk.BOTH, expand=True)
        
        # Processed
        proc_frame = ttk.LabelFrame(parent, text="Processed Image", padding=10)
        proc_frame.pack(fill=tk.BOTH, expand=True)
        
        proc_label = tk.Label(proc_frame, bg='white', relief='solid', bd=1,
                            text="Processed image will appear here", justify=tk.CENTER,
                            font=('Segoe UI', 10), fg='gray')
        proc_label.pack(fill=tk.BOTH, expand=True)
        
        # Store references
        if mode == "auto":
            self.auto_original = orig_label
            self.auto_processed = proc_label
        else:
            self.manual_original = orig_label
            self.manual_processed = proc_label
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status.set(message)
        self.root.update_idletasks()
    
    def upload_image(self):
        """Load image with error handling"""
        try:
            path = filedialog.askopenfilename(
                filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.tiff")])
            if not path:
                return
            
            self.update_status("Loading image...")
            self.current_image = self.image_repo.load(Path(path))
            
            # Display thumbnail
            thumbnail = self.color_analyzer.create_thumbnail(self.current_image.pixels)
            self.display_image(thumbnail, "original")
            
            self.update_status(f"Loaded: {self.current_image.file_path.name}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Load failed")
    
    def process_auto(self):
        """Auto color reduction"""
        if not self.current_image:
            messagebox.showwarning("Warning", "Please upload an image first")
            return
        
        try:
            self.update_status("Processing...")
            count = int(self.auto_count.get())
            
            result = self.color_service.auto_reduce_colors(self.current_image, count)
            self.processed_image = result
            
            self.display_image(result, "processed")
            self.update_status(f"Reduced to {count} colors")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Processing failed")
    
    def analyze_colors(self):
        """Analyze dominant colors"""
        if not self.current_image:
            messagebox.showwarning("Warning", "Please upload an image first")
            return
        
        try:
            self.update_status("Analyzing colors...")
            count = int(self.manual_count.get())
            
            palette = self.color_service.analyze_image_colors(self.current_image, count)
            self.display_palette(palette, self.dominant_canvas)
            
            self.update_status(f"Found {count} color regions")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Analysis failed")
    
    def process_manual(self):
        """Process with selected filament colors"""
        if not self.current_image:
            messagebox.showwarning("Warning", "Please upload an image first")
            return
        
        valid_colors = [c for c in self.selected_colors if c is not None]
        if not valid_colors:
            messagebox.showwarning("Warning", "Please select filament colors first")
            return
        
        try:
            self.update_status("Processing with filament colors...")
            palette = ColorPalette(tuple(valid_colors))
            
            result = self.color_service.manual_reduce_colors(self.current_image, palette)
            self.processed_image = result
            
            self.display_image(result, "processed")
            self.update_status("3D print simulation complete")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Processing failed")
    
    def display_image(self, pixels: np.ndarray, image_type: str):
        """Display image in GUI"""
        try:
            thumbnail = self.color_analyzer.create_thumbnail(pixels)
            pil_image = Image.fromarray(thumbnail)
            photo = ImageTk.PhotoImage(pil_image)
            
            if image_type == "original":
                self.auto_original.config(image=photo, text="")
                self.auto_original.image = photo
                self.manual_original.config(image=photo, text="")
                self.manual_original.image = photo
            else:
                self.auto_processed.config(image=photo, text="")
                self.auto_processed.image = photo
                self.manual_processed.config(image=photo, text="")
                self.manual_processed.image = photo
                
        except Exception as e:
            messagebox.showerror("Error", f"Display error: {str(e)}")
    
    def display_palette(self, palette: ColorPalette, canvas: tk.Canvas):
        """Display color palette"""
        canvas.delete("all")
        colors = list(palette.colors)
        
        if not colors:
            canvas.create_text(75, 12, text="No colors", fill="gray", font=('Segoe UI', 8))
            return
        
        width = canvas.winfo_width() or 150
        seg = width / len(colors)
        
        for i, color in enumerate(colors):
            x0, x1 = i * seg, (i + 1) * seg
            canvas.create_rectangle(x0, 0, x1, 25, fill=color.hex, outline="")
    
    def update_color_selectors(self, event=None):
        """Update color selection UI"""
        # Clear existing widgets
        for widget in self.color_selector_frame.winfo_children():
            widget.destroy()
        
        self.selected_colors.clear()
        self.color_previews.clear()  # Clear previous preview references
        
        count = int(self.manual_count.get())
        
        for i in range(count):
            frame = ttk.Frame(self.color_selector_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=f"Color {i+1}:", width=8).pack(side=tk.LEFT)
            
            btn = ttk.Button(frame, text="Choose", 
                      command=lambda idx=i: self.choose_color(idx))
            btn.pack(side=tk.LEFT, padx=5)
            
            # Create preview canvas and store reference
            preview = tk.Canvas(frame, width=30, height=20, bg='white', 
                              relief='solid', bd=1, highlightthickness=0)
            preview.pack(side=tk.LEFT)
            self.color_previews.append(preview)  # Store reference
            
            # Initialize with no color
            self.selected_colors.append(None)
    
    def choose_color(self, index: int):
        """Choose filament color and update preview immediately"""
        color = colorchooser.askcolor(title=f"Choose filament color {index+1}")
        if color[0]:
            rgb = tuple(map(int, color[0]))
            selected_color = RGBColor.from_tuple(rgb)
            self.selected_colors[index] = selected_color
            
            # Update the specific preview canvas immediately
            if index < len(self.color_previews):
                preview_canvas = self.color_previews[index]
                preview_canvas.delete("all")  # Clear previous
                preview_canvas.configure(bg=selected_color.hex)  # Set background color
            
            # Update the palette preview at the bottom
            valid_colors = [c for c in self.selected_colors if c is not None]
            self.display_palette(ColorPalette(tuple(valid_colors)), self.selected_canvas)
            
            self.update_status(f"Selected color {index+1}: {selected_color.hex}")
    
    def save_image(self):
        """Save processed image"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save")
            return
        
        try:
            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if not path:
                return
            
            self.image_repo.save(self.processed_image, Path(path))
            messagebox.showinfo("Success", f"Image saved:\n{path}")
            self.update_status("Image saved")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Save failed")