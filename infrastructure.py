import cv2
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from domain import Image, RGBColor, ColorPalette, InvalidImageException, ColorProcessingException

class ImageRepository:
    """Infrastructure service for image I/O operations"""
    
    def load(self, file_path: Path) -> Image:
        """Load image from file with proper error handling"""
        try:
            if not file_path.exists():
                raise InvalidImageException(f"File not found: {file_path}")
            
            image_array = cv2.imread(str(file_path))
            if image_array is None:
                raise InvalidImageException(f"Unsupported image format: {file_path}")
            
            # Convert BGR to RGB
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            return Image(file_path, image_array)
            
        except Exception as e:
            if isinstance(e, InvalidImageException):
                raise
            raise InvalidImageException(f"Failed to load image: {str(e)}")
    
    def save(self, pixels: np.ndarray, file_path: Path) -> None:
        """Save image to file"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Convert RGB to BGR for OpenCV
            save_pixels = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)
            success = cv2.imwrite(str(file_path), save_pixels)
            if not success:
                raise InvalidImageException(f"Failed to save image: {file_path}")
        except Exception as e:
            raise InvalidImageException(f"Save failed: {str(e)}")

class ColorAnalyzer:
    """Infrastructure service for color analysis algorithms"""
    
    def find_dominant_colors(self, image: Image, color_count: int) -> ColorPalette:
        """Use K-means clustering to find dominant colors"""
        try:
            # Resize large images for performance
            processed_image = self._prepare_image(image, max_dimension=800)
            pixels = processed_image.pixels.reshape(-1, 3)
            
            kmeans = KMeans(n_clusters=color_count, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            dominant_colors = [
                RGBColor.from_tuple(tuple(map(int, color)))
                for color in kmeans.cluster_centers_
            ]
            
            return ColorPalette(tuple(dominant_colors))
            
        except Exception as e:
            raise ColorProcessingException(f"Color analysis failed: {str(e)}")
    
    def _prepare_image(self, image: Image, max_dimension: int = 1000) -> Image:
        """Resize image if too large while maintaining aspect ratio"""
        height, width = image.dimensions
        
        if max(height, width) <= max_dimension:
            return image
        
        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        
        resized_pixels = cv2.resize(
            image.pixels, 
            (new_width, new_height), 
            interpolation=cv2.INTER_AREA
        )
        
        return Image(image.file_path, resized_pixels)
    
    def create_thumbnail(self, pixels: np.ndarray, max_size: int = 400) -> np.ndarray:
        """Create thumbnail for display"""
        height, width = pixels.shape[:2]
        
        if max(height, width) <= max_size:
            return pixels.copy()
        
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        return cv2.resize(pixels, (new_width, new_height), interpolation=cv2.INTER_AREA)