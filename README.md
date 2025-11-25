
# Color Reduction Tool for 3D Printing

A professional desktop application for reducing image colors, specifically designed for 3D printing filament planning and visualization.

## Features

### Auto Mode
- Automatically reduce images to a specified number of colors using K-means clustering
- Quick processing for general color reduction tasks
- Side-by-side comparison of original and processed images

### 3D Printing Mode
- **Color Analysis**: Automatically detects dominant color regions in your image
- **Filament Color Mapping**: Map your actual filament colors to image regions based on luminosity matching
- **Realistic Simulation**: See how your 3D print will look with specific filament colors
- **Professional Workflow**: Upload → Analyze → Select Colors → Process → Save

## Installation

1. **Install Python** (3.8 or higher required)
   - Download from [python.org](https://python.org)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python color_reduction_gui.py
   ```

   Or use the provided batch files:
   - `installer.bat` - Installs dependencies
   - `run.bat` - Runs the application

## Usage

### Auto Mode (Quick Processing)
1. Select number of target colors
2. Upload an image
3. Click "Process"
4. Save the result

### 3D Printing Mode (Advanced)
1. **Upload Image**: Load your reference image
2. **Set Color Count**: Choose how many filament colors you want to use
3. **Analyze Image**: Click "Analyze Image Colors" to find natural color divisions
4. **Select Filament Colors**: Choose your actual filament colors using the color picker
5. **Process**: Click "Process with Selected Colors" to apply luminosity-based mapping
6. **Save**: Export the final 3D printing simulation

## How It Works

### Color Mapping Algorithm
The application uses intelligent luminosity-based mapping:

1. **Color Analysis**: K-means clustering identifies the dominant color regions in your image
2. **Luminosity Calculation**: Both image colors and filament colors are sorted by perceived brightness
3. **Smart Mapping**: Darkest filament color maps to darkest image region, lightest to lightest, etc.
4. **Pixel Replacement**: Each pixel is replaced with the appropriate filament color based on its original color region

### Technical Details
- **K-means Clustering**: For automatic color region detection
- **Luminosity Formula**: `0.2126*R + 0.7152*G + 0.0722*B` for accurate brightness perception
- **Efficient Processing**: Automatic image resizing for large files while maintaining quality
- **Color Accuracy**: Preserves your exact filament colors in the final output

## Use Cases

- **3D Printing Planning**: Visualize multi-color prints before printing
- **Filament Management**: Plan color usage for available filament spools
- **Art Preparation**: Prepare images for multi-material 3D printing
- **Color Study**: Analyze color distribution in images

## Requirements

- Python 3.8+
- OpenCV
- NumPy
- scikit-learn
- Pillow (PIL)
- tkinter (usually included with Python)

## File Structure

```
color-reduction-tool/
├── color_reduction_gui.py  # Main application
├── requirements.txt        # Python dependencies
├── installer.bat          # Windows dependency installer
├── run.bat               # Windows application launcher
└── README.md             # This file
```

## Support

For issues or feature requests, please check that:
- All dependencies are properly installed
- You're using supported image formats (PNG, JPG, JPEG, BMP, TIFF)
- Your image files are not corrupted

## License

This project is open source and available under the MIT License.


