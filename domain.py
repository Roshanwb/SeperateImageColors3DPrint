from dataclasses import dataclass
from typing import Tuple, List
from pathlib import Path
import numpy as np

@dataclass(frozen=True)
class RGBColor:
    """Value object representing an RGB color with validation"""
    r: int
    g: int
    b: int
    
    def __post_init__(self):
        if not all(0 <= x <= 255 for x in (self.r, self.g, self.b)):
            raise ValueError("RGB values must be between 0-255")
    
    @property
    def tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)
    
    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    @property
    def luminosity(self) -> float:
        """Perceived brightness for human vision"""
        return 0.2126 * (self.r/255.0) + 0.7152 * (self.g/255.0) + 0.0722 * (self.b/255.0)
    
    @classmethod
    def from_tuple(cls, rgb_tuple: Tuple[int, int, int]) -> 'RGBColor':
        return cls(*rgb_tuple)

@dataclass(frozen=True)
class ColorPalette:
    """Immutable collection of colors with business logic"""
    colors: Tuple[RGBColor, ...]
    
    def __post_init__(self):
        if not self.colors:
            raise ValueError("Color palette cannot be empty")
    
    @property
    def sorted_by_luminosity(self) -> 'ColorPalette':
        """Smart sorting by perceived brightness"""
        return ColorPalette(tuple(sorted(self.colors, key=lambda c: c.luminosity)))
    
    def __len__(self) -> int:
        return len(self.colors)

@dataclass
class Image:
    """Domain entity representing an image"""
    file_path: Path
    pixels: np.ndarray
    
    @property
    def dimensions(self) -> Tuple[int, int]:
        return self.pixels.shape[:2]
    
    @property
    def total_pixels(self) -> int:
        return self.pixels.shape[0] * self.pixels.shape[1]

class DomainException(Exception):
    """Base domain exception"""
    pass

class InvalidImageException(DomainException):
    """Raised when image operations fail"""
    pass

class ColorProcessingException(DomainException):
    """Raised when color processing fails"""
    pass