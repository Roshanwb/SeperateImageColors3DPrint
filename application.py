from typing import Dict
import numpy as np
from domain import Image, RGBColor, ColorPalette, ColorProcessingException
from infrastructure import ColorAnalyzer

class ColorReductionService:
    """Application service coordinating color reduction workflows"""
    
    def __init__(self, color_analyzer: ColorAnalyzer):
        self.color_analyzer = color_analyzer
    
    def auto_reduce_colors(self, image: Image, color_count: int) -> np.ndarray:
        """Auto color reduction using K-means clustering"""
        try:
            dominant_colors = self.color_analyzer.find_dominant_colors(image, color_count)
            return self._apply_palette(image, dominant_colors)
        except Exception as e:
            raise ColorProcessingException(f"Auto reduction failed: {str(e)}")
    
    def manual_reduce_colors(self, image: Image, filament_colors: ColorPalette) -> np.ndarray:
        """Reduce colors using specific filament colors with smart luminosity mapping"""
        try:
            # Find natural color divisions in image
            dominant_colors = self.color_analyzer.find_dominant_colors(image, len(filament_colors))
            
            # Create intelligent mapping based on luminosity
            color_mapping = self._create_luminosity_mapping(dominant_colors, filament_colors)
            
            return self._apply_color_mapping(image, dominant_colors, color_mapping)
        except Exception as e:
            raise ColorProcessingException(f"Manual reduction failed: {str(e)}")
    
    def analyze_image_colors(self, image: Image, color_count: int) -> ColorPalette:
        """Analyze and return dominant colors in image"""
        return self.color_analyzer.find_dominant_colors(image, color_count)
    
    def _create_luminosity_mapping(self, source: ColorPalette, target: ColorPalette) -> Dict[RGBColor, RGBColor]:
        """Smart mapping: darkest source → darkest target, etc."""
        source_sorted = source.sorted_by_luminosity
        target_sorted = target.sorted_by_luminosity
        
        mapping = {}
        for i, source_color in enumerate(source_sorted.colors):
            # Map based on luminosity position
            target_index = min(i, len(target_sorted) - 1)
            mapping[source_color] = target_sorted.colors[target_index]
        
        return mapping
    
    def _apply_palette(self, image: Image, palette: ColorPalette) -> np.ndarray:
        """Apply color palette to image"""
        return self._apply_color_mapping(image, palette, {})
    
    def _apply_color_mapping(self, image: Image, palette: ColorPalette, mapping: Dict[RGBColor, RGBColor]) -> np.ndarray:
        """Core algorithm: map each pixel to closest color with optional mapping"""
        processed_image = self.color_analyzer._prepare_image(image, max_dimension=1200)
        pixels = processed_image.pixels.reshape(-1, 3)
        
        # Convert palette to numpy for distance calculation
        palette_array = np.array([color.tuple for color in palette.colors])
        
        # Find closest palette color for each pixel
        distances = np.linalg.norm(pixels[:, None] - palette_array[None, :], axis=2)
        labels = np.argmin(distances, axis=1)
        
        # Apply color mapping
        reduced_pixels = np.zeros_like(pixels)
        for i, label in enumerate(labels):
            original_color = palette.colors[label]
            if original_color in mapping:
                reduced_pixels[i] = mapping[original_color].tuple
            else:
                reduced_pixels[i] = original_color.tuple
        
        return reduced_pixels.reshape(processed_image.pixels.shape)