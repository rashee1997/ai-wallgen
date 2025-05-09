# wall_gen/image_editor.py
"""
Image editing functionalities using Pillow, OpenCV, and Scikit-image.
NOTE: This module uses absolute imports assuming it's part of the 'wall_gen' package.
It may not run correctly as a standalone script without sys.path adjustments.
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from typing import Optional, Callable, Any
import numpy as np
import cv2
from skimage import filters, util
from skimage.util import img_as_ubyte
from io import BytesIO # Added for mask serialization

class ImageHistory:
    def __init__(self, max_length=10):
        self.undo_stack = []
        self.redo_stack = []
        self.max_length = max_length

    def push(self, image):
        """Pushes the current image onto the undo stack."""
        if not self.undo_stack or self.undo_stack[-1].tobytes() != image.tobytes():
            self.undo_stack.append(image.copy())
            if len(self.undo_stack) > self.max_length:
                self.undo_stack.pop(0)
            self.redo_stack.clear()

    def undo(self, current_image: Image.Image) -> Image.Image:
        """Undoes the last editing step, returning the previous image."""
        if not self.undo_stack:
            return current_image
        self.redo_stack.append(current_image.copy())
        restored_image = self.undo_stack.pop()
        return restored_image

    def redo(self, current_image: Image.Image) -> Image.Image:
        """Redoes the last undone editing step, returning the next image."""
        if not self.redo_stack:
            return current_image
        self.undo_stack.append(current_image.copy())
        restored_image = self.redo_stack.pop()
        return restored_image

class SelectionMask:
    def __init__(self, mask_array: np.ndarray):
        if mask_array.dtype != np.bool_:
            mask_array = mask_array.astype(np.bool_)
        self._mask = mask_array

    @property
    def mask(self) -> np.ndarray:
        return self._mask

    def to_png_bytes(self) -> bytes:
        """Serialize the boolean mask to PNG bytes."""
        mask_uint8 = self._mask.astype(np.uint8) * 255
        img = Image.fromarray(mask_uint8, mode='L')
        byte_arr = BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()

    @staticmethod
    def from_png_bytes(png_bytes: bytes) -> 'SelectionMask':
        """Deserialize a boolean mask from PNG bytes."""
        img = Image.open(BytesIO(png_bytes)).convert('L')
        mask_uint8 = np.array(img)
        mask_array = mask_uint8 > 128
        return SelectionMask(mask_array)

    def invert(self) -> 'SelectionMask':
        """Inverts the boolean mask."""
        return SelectionMask(~self._mask)

    def clear(self) -> 'SelectionMask':
        """Creates an empty mask of the same shape."""
        return SelectionMask(np.zeros_like(self._mask, dtype=np.bool_))

    def combine(self, other_mask: 'SelectionMask', mode: str = 'union') -> 'SelectionMask':
        """Combines this mask with another SelectionMask."""
        if self._mask.shape != other_mask.mask.shape:
             raise ValueError("Mask shapes must match for combination.")
        if mode == 'union':
            combined_mask = self._mask | other_mask.mask
        elif mode == 'intersection':
            combined_mask = self._mask & other_mask.mask
        elif mode == 'difference':
            combined_mask = self._mask & (~other_mask.mask)
        else:
            raise ValueError(f"Unsupported combination mode: {mode}")
        return SelectionMask(combined_mask)

    @staticmethod
    def load_from_bytes(mask_bytes: bytes, format: str = 'png') -> 'SelectionMask':
        """Loads a SelectionMask from bytes."""
        if format == 'png':
            return SelectionMask.from_png_bytes(mask_bytes)
        else:
            raise ValueError(f"Unsupported mask format: {format}")

def apply_with_mask(func: Callable[[Image.Image, Any], Image.Image], image: Image.Image, mask: Optional[np.ndarray], *args, **kwargs) -> Image.Image:
    """Applies a function to an image only within the masked region."""
    if mask is None:
        return func(image, *args, **kwargs)

    if mask.shape[:2] != image.size[::-1]:
         raise ValueError("Mask shape must match image shape.")
    if mask.dtype != np.bool_:
        mask = mask.astype(np.bool_)

    processed_image = func(image.copy(), *args, **kwargs) # Apply to a copy

    original_np = np.array(image)
    processed_np = np.array(processed_image)

    if original_np.shape != processed_np.shape:
         if processed_image.mode != image.mode:
             processed_image = processed_image.convert(image.mode)
             processed_np = np.array(processed_image)
             if original_np.shape != processed_np.shape:
                  raise ValueError(f"Shape mismatch after processing and mode conversion: original {original_np.shape}, processed {processed_np.shape}. Cannot apply mask.")

    if len(original_np.shape) == 3:
        mask_3d = np.stack([mask] * original_np.shape[2], axis=-1)
    else:
        mask_3d = mask

    composited_np = np.where(mask_3d, processed_np, original_np)
    return Image.fromarray(composited_np.astype(original_np.dtype), mode=image.mode)

# --- Basic Adjustments ---
def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def apply_gamma_correction(image: Image.Image, gamma: float) -> Image.Image:
    if gamma == 1.0: return image
    img_rgb = image.convert('RGB') # Ensure RGB for LUT
    lut = [pow(x / 255., gamma) * 255 for x in range(256)]
    lut_applied = [int(round(l)) for l in lut] # Ensure integer LUT
    if img_rgb.mode == 'RGB':
        lut_final = lut_applied * 3
    elif img_rgb.mode == 'L':
         lut_final = lut_applied # Grayscale needs single channel LUT
    else: # Handle RGBA etc. if needed, or raise error
         if img_rgb.mode == 'RGBA':
             r, g, b, a = img_rgb.split()
             r = r.point(lut_applied)
             g = g.point(lut_applied)
             b = b.point(lut_applied)
             return Image.merge('RGBA', (r, g, b, a))
         else:
             # Fallback or error for unsupported modes
             return img_rgb.point(lut_applied * len(img_rgb.getbands())) # Simple point op might work for some modes

    return img_rgb.point(lut_final)


def apply_blur(image: Image.Image, radius: float) -> Image.Image:
    if radius <= 0: return image
    return image.filter(ImageFilter.GaussianBlur(radius))

def apply_grayscale(image: Image.Image) -> Image.Image:
    return ImageOps.grayscale(image).convert('RGB') # Ensure output is RGB

def apply_invert(image: Image.Image) -> Image.Image:
    img_rgb = image.convert('RGB') # Invert works on RGB
    return ImageOps.invert(img_rgb)

def rotate_image(image: Image.Image, angle: float) -> Image.Image:
    # Use RGBA to handle background revealed by rotation
    return image.convert("RGBA").rotate(angle, expand=True, fillcolor=(0,0,0,0)) # Transparent fill

# --- AI / Complex Filters (Placeholders/CV/Skimage) ---
def ai_enhance(image: Image.Image) -> Image.Image:
    # Placeholder - requires actual AI model integration
    print("Warning: AI Enhance is a placeholder.")
    return image

def remove_background(image: Image.Image) -> Image.Image:
    # Placeholder - requires background removal library (e.g., rembg)
    print("Warning: Background Removal is a placeholder.")
    return image

def apply_high_pass_filter(image: Image.Image, radius: int = 15) -> Image.Image:
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    # Ensure kernel size is odd
    ksize = radius * 2 + 1
    blur = cv2.GaussianBlur(img_gray, (ksize, ksize), 0)
    # High pass = original - low pass (blur) + offset (128)
    # Or using addWeighted: original * alpha + blurred * beta + gamma
    # Let's try a common approach: gray + (gray - blur) = 2*gray - blur (scaled)
    high_pass = cv2.addWeighted(img_gray, 2.0, blur, -1.0, 0) # Might need adjustment
    high_pass = np.clip(high_pass, 0, 255) # Clip result
    high_pass_rgb = cv2.cvtColor(high_pass, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(high_pass_rgb)

def apply_histogram_equalization(image: Image.Image) -> Image.Image:
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    # Equalize Y channel in YUV space to preserve color
    img_yuv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return Image.fromarray(img_eq)

def apply_contour_detection(image: Image.Image) -> Image.Image:
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(img_gray, 100, 200)
    # Create a black background and draw white contours
    contour_img = np.zeros_like(img_cv)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 1) # Draw white contours
    return Image.fromarray(contour_img)

def add_gaussian_noise(image: Image.Image, mean=0, sigma=15) -> Image.Image:
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    # Ensure noise is added correctly without changing type prematurely
    noise = np.random.normal(mean, sigma, img_cv.shape)
    noisy_img = img_cv.astype(np.float32) + noise # Add noise to float version
    noisy_img = np.clip(noisy_img, 0, 255) # Clip result
    return Image.fromarray(noisy_img.astype(np.uint8)) # Convert back to uint8

def apply_pencil_sketch(image: Image.Image) -> Image.Image:
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    # pencilSketch returns two images: grayscale sketch, color sketch
    # We typically want the grayscale one for a pencil effect
    gray_sketch, color_sketch = cv2.pencilSketch(img_cv, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    # Convert the grayscale sketch back to RGB for consistency
    return Image.fromarray(cv2.cvtColor(gray_sketch, cv2.COLOR_GRAY2RGB))

def apply_sepia(image: Image.Image) -> Image.Image:
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    # Sepia kernel
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    # Apply the kernel using matrix multiplication (transform)
    sepia_img = cv2.transform(img_cv, kernel)
    # Clip values to 0-255 range
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    return Image.fromarray(sepia_img)

def crop_image(image: Image.Image, left: int, upper: int, right: int, lower: int) -> Image.Image:
    """Crop the image to the specified box."""
    return image.crop((left, upper, right, lower))

def apply_sharpen_filter(image: Image.Image) -> Image.Image:
    """Apply a sharpen filter using a kernel."""
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(img_cv, -1, kernel)
    return Image.fromarray(sharpened)

def add_border(image: Image.Image, border_size: int, color=(0,0,0)) -> Image.Image:
    """Add a border of specified size and color around the image."""
    if border_size <= 0:
        return image
    return ImageOps.expand(image, border=border_size, fill=color)

def apply_xray_effect(image: Image.Image) -> Image.Image:
    """Apply an x-ray like effect."""
    img_rgb = image.convert('RGB')
    img_cv = np.array(img_rgb)
    inverted = cv2.bitwise_not(img_cv)
    gray = cv2.cvtColor(inverted, cv2.COLOR_RGB2GRAY)
    # Use a colormap that resembles X-ray (e.g., BONE or a custom grayscale inversion)
    # COLORMAP_BONE might not be ideal, simple inversion might be better
    # xray_img = cv2.bitwise_not(gray) # Simple inversion of grayscale
    # return Image.fromarray(cv2.cvtColor(xray_img, cv2.COLOR_GRAY2RGB))
    # Or use a colormap like BONE
    colored = cv2.applyColorMap(gray, cv2.COLORMAP_BONE)
    return Image.fromarray(colored)


# --- Pillow ImageFilter Filters ---
def apply_emboss(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.EMBOSS)

def apply_edge_enhance(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.EDGE_ENHANCE)

def apply_edge_enhance_more(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.EDGE_ENHANCE_MORE)

def apply_find_edges(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.FIND_EDGES)

def apply_detail(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.DETAIL)

def apply_smooth(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.SMOOTH)

def apply_smooth_more(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.SMOOTH_MORE)

# --- Scikit-image Filters ---
# Note: These often work best on grayscale images. Convert back to RGB for consistency.

def apply_laplace(image: Image.Image) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    lap = filters.laplace(img_np)
    # Scale laplace output appropriately for display
    lap_scaled = cv2.normalize(lap, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return Image.fromarray(lap_scaled).convert('RGB')

def apply_sobel(image: Image.Image) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    sobel_img = filters.sobel(img_np)
    # Sobel output needs scaling
    sobel_scaled = cv2.normalize(sobel_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return Image.fromarray(sobel_scaled).convert('RGB')

def apply_scharr(image: Image.Image) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    scharr_img = filters.scharr(img_np)
    scharr_scaled = cv2.normalize(scharr_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return Image.fromarray(scharr_scaled).convert('RGB')

def apply_prewitt(image: Image.Image) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    prewitt_img = filters.prewitt(img_np)
    prewitt_scaled = cv2.normalize(prewitt_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return Image.fromarray(prewitt_scaled).convert('RGB')

def apply_roberts(image: Image.Image) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    roberts_img = filters.roberts(img_np)
    roberts_scaled = cv2.normalize(roberts_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return Image.fromarray(roberts_scaled).convert('RGB')

def apply_gabor(image: Image.Image, frequency=0.6) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    # Gabor filter returns real and imaginary parts
    real, imag = filters.gabor(img_np, frequency=frequency)
    # Visualize the magnitude (or real part)
    gabor_mag = np.sqrt(real**2 + imag**2)
    gabor_scaled = cv2.normalize(gabor_mag, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return Image.fromarray(gabor_scaled).convert('RGB')

# --- Thresholding Filters ---
def apply_otsu_threshold(image: Image.Image) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    thresh = filters.threshold_otsu(img_np)
    binary = img_np > thresh
    binary_img = (binary * 255).astype(np.uint8)
    return Image.fromarray(binary_img).convert('RGB')

def apply_niblack_threshold(image: Image.Image, window_size=25, k=0.8) -> Image.Image:
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    # Niblack requires skimage version >= 0.17
    try:
        thresh = filters.threshold_niblack(img_np, window_size=window_size, k=k)
        binary = img_np > thresh
        binary_img = (binary * 255).astype(np.uint8)
        return Image.fromarray(binary_img).convert('RGB')
    except AttributeError:
        print("Warning: Niblack threshold requires scikit-image >= 0.17")
        return image.convert('RGB') # Return original if not available

def apply_sauvola_threshold(image: Image.Image, window_size=25, k=0.2) -> Image.Image: # Adjusted default k
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    # Sauvola requires skimage version >= 0.17
    try:
        thresh = filters.threshold_sauvola(img_np, window_size=window_size, k=k)
        binary = img_np > thresh
        binary_img = (binary * 255).astype(np.uint8)
        return Image.fromarray(binary_img).convert('RGB')
    except AttributeError:
        print("Warning: Sauvola threshold requires scikit-image >= 0.17")
        return image.convert('RGB') # Return original if not available

# --- Mask Creation ---
def create_rectangle_mask(image_shape: tuple[int, int], point1: tuple[int, int], point2: tuple[int, int]) -> np.ndarray:
    """Creates a boolean mask for a rectangle. Assumes image_shape is (height, width) and points are (row, col)."""
    mask = np.zeros(image_shape, dtype=np.uint8)
    pt1_cv = (min(point1[1], point2[1]), min(point1[0], point2[0])) # Ensure top-left (x,y)
    pt2_cv = (max(point1[1], point2[1]), max(point1[0], point2[0])) # Ensure bottom-right (x,y)
    cv2.rectangle(mask, pt1_cv, pt2_cv, 255, -1)
    return mask.astype(np.bool_)

def create_ellipse_mask(image_shape: tuple[int, int], center: tuple[int, int], axes: tuple[int, int]) -> np.ndarray:
    """Creates a boolean mask for an ellipse. Assumes image_shape is (height, width) and center/axes are (row, col)."""
    mask = np.zeros(image_shape, dtype=np.uint8)
    center_cv = (center[1], center[0]) # (x, y)
    axes_cv = (axes[1] // 2, axes[0] // 2) # (major_axis/2, minor_axis/2) - cv2 uses half-axes lengths
    cv2.ellipse(mask, center_cv, axes_cv, 0, 0, 360, 255, -1)
    return mask.astype(np.bool_)

def create_lasso_mask(image_shape: tuple[int, int], coordinates: list[tuple[int, int]]) -> np.ndarray:
    """Creates a boolean mask for a free-form lasso selection. Assumes image_shape is (height, width) and coordinates are (row, col)."""
    if not coordinates or len(coordinates) < 3: # Need at least 3 points for a polygon
        return np.zeros(image_shape, dtype=np.bool_)
    mask = np.zeros(image_shape, dtype=np.uint8)
    pts_cv = np.array([(p[1], p[0]) for p in coordinates], np.int32) # Convert to (x,y) for cv2
    cv2.fillPoly(mask, [pts_cv], 255)
    return mask.astype(np.bool_)
