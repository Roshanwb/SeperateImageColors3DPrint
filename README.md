# Color Reduction Pro

A professional desktop application for intelligent color reduction, specifically designed for 3D printing filament planning and visualization.

![Color Reduction Pro](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

## 🚀 Features

### Auto Color Reduction
- **Smart Clustering**: Automatically reduces images to specified color counts using K-means clustering
- **Performance Optimized**: Handles large images efficiently with intelligent resizing
- **Quality Preservation**: Maintains image quality while reducing color complexity

### 3D Printing Mode
- **Filament Planning**: Map your actual filament colors to images for print visualization
- **Luminosity Mapping**: Intelligent color matching based on perceived brightness
- **Real-time Preview**: See how your print will look with selected filament colors
- **Professional Workflow**: Upload → Analyze → Select Colors → Process → Save

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Setup
1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

   Or use the provided batch files on Windows:
   - `installer.bat` - Installs all dependencies
   - `run.bat` - Launches the application

## 📖 Usage

### Auto Mode (Quick Processing)
1. Select target color count (1-12)
2. Upload your image
3. Click "Process" for automatic color reduction
4. Save the result

### 3D Printing Mode (Advanced)
1. **Upload Image**: Load your reference image
2. **Set Color Count**: Choose how many filament colors to use (1-8)
3. **Analyze Colors**: Click "Analyze Colors" to find natural color divisions
4. **Select Filaments**: Choose your actual filament colors using the color picker
5. **Process**: Click "Process" to apply intelligent luminosity-based mapping
6. **Save**: Export the final 3D printing simulation

## 🎯 How It Works

### Intelligent Color Mapping
The application uses advanced algorithms to ensure realistic results:

1. **Color Analysis**: K-means clustering identifies dominant color regions
2. **Luminosity Calculation**: Colors are sorted by human-perceived brightness
3. **Smart Mapping**: Darkest filament → darkest image region, lightest → lightest
4. **Pixel Replacement**: Each pixel is mapped to the appropriate filament color

### Technical Excellence
- **Clean Architecture**: Domain-driven design with proper separation of concerns
- **Professional Error Handling**: Comprehensive validation and user feedback
- **Performance Optimized**: Efficient processing for large images
- **Modern GUI**: Clean, professional interface with real-time previews

## 🏗️ Architecture

```
Color Reduction Pro/
├── domain.py          # Business logic & data models
├── application.py     # Use cases & workflows  
├── infrastructure.py  # Technical implementations
├── interface.py       # Modern GUI
└── main.py           # Application entry point
```

Built with clean architecture principles:
- **Domain Layer**: Pure business logic (colors, validation, rules)
- **Application Layer**: Use cases and workflows
- **Infrastructure Layer**: Technical details (file I/O, algorithms)
- **Interface Layer**: Professional GUI separated from business logic

## 📋 Requirements

```txt
opencv-python>=4.5.0    # Image processing
numpy>=1.21.0          # Numerical operations
Pillow>=8.3.0          # Image handling
scikit-learn>=1.0.0    # Machine learning (K-means)
```

## 🖼️ Supported Formats

- **PNG** - Recommended for lossless quality
- **JPEG** - Standard photography format
- **BMP** - Windows bitmap
- **TIFF** - High-quality professional format

## 💡 Use Cases

### 3D Printing
- Visualize multi-color prints before printing
- Plan filament usage and color combinations
- Create realistic print simulations

### Design & Art
- Prepare images for multi-material printing
- Study color distribution and composition
- Create artistic color-reduced versions

### Education
- Learn about color theory and perception
- Understand clustering algorithms
- Study image processing techniques

## 🐛 Troubleshooting

### Common Issues
- **Large images**: Automatically resized for performance
- **Unsupported formats**: Use PNG, JPEG, BMP, or TIFF
- **Color analysis**: Ensure good contrast in source images

### Getting Help
1. Check that all dependencies are installed
2. Verify image file is not corrupted
3. Ensure sufficient system memory for large images

## 📄 License

This project is open source and available under the MIT License.

## 🔮 Future Enhancements

- Batch processing for multiple images
- Advanced color space options (LAB, HSV)
- Custom color palette import/export
- Print preparation tools (scaling, positioning)

---

**Color Reduction Pro** - Professional color processing for makers, designers, and 3D printing enthusiasts.
