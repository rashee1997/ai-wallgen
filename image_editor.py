from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from typing import Optional, Callable, Any

class ImageHistory:
    def __init__(self, max_length=10):
        self.undo_stack = []
        self.redo_stack = []
        self.max_length = max_length

    def push(self, image):
        """Pushes the current image onto the undo stack."""
        # Check if the new state is the same as the top of the undo stack
        if not self.undo_stack or self.undo_stack[-1].tobytes() != image.tobytes():
            self.undo_stack.append(image.copy())
            if len(self.undo_stack) > self.max_length:
                self.undo_stack.pop(0)
            self.redo_stack.clear()

    def undo(self, current_image: Image.Image) -> Image.Image:
        """Undoes the last editing step, returning the previous image."""
        if not self.undo_stack:
            return current_image # Nothing to undo

        # Push current state onto redo stack
        self.redo_stack.append(current_image.copy())

        # Pop previous state from undo stack
        restored_image = self.undo_stack.pop()

        return restored_image

    def redo(self, current_image: Image.Image) -> Image.Image:
        """Redoes the last undone editing step, returning the next image."""
        if not self.redo_stack:
            return current_image # Nothing to redo

        # Push current state onto undo stack
        self.undo_stack.append(current_image.copy())

        # Pop next state from redo stack
        restored_image = self.redo_stack.pop()

        return restored_image

import numpy as np
import cv2
from skimage import filters, util
from skimage.util import img_as_ubyte

class SelectionMask:
    def __init__(self, mask_array: np.ndarray):
        if mask_array.dtype != np.bool_:
            # Convert to boolean mask if not already
            mask_array = mask_array.astype(np.bool_)
        self._mask = mask_array

    @property
    def mask(self) -> np.ndarray:
        return self._mask

    def to_png_bytes(self) -> bytes:
        """Serialize the boolean mask to PNG bytes."""
        # Convert boolean mask to uint8 (0 or 255) for PNG
        mask_uint8 = self._mask.astype(np.uint8) * 255
        img = Image.fromarray(mask_uint8, mode='L')
        # Save as PNG
        from io import BytesIO
        byte_arr = BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()

    @staticmethod
    def from_png_bytes(png_bytes: bytes) -> 'SelectionMask':
        """Deserialize a boolean mask from PNG bytes."""
        from io import BytesIO
        img = Image.open(BytesIO(png_bytes)).convert('L')
        mask_uint8 = np.array(img)
        # Convert uint8 (0 or 255) back to boolean
        mask_array = mask_uint8 > 128 # Use a threshold to handle potential variations
        return SelectionMask(mask_array)

    # Add other potential serialization methods later if needed (RLE, raw buffer)
    # Add methods for combining, inverting, clearing later as per plan step 3

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
        elif mode == 'difference': # self - other
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

    # Ensure mask is boolean and matches image size
    if mask.shape[:2] != image.size[::-1]: # image.size is (width, height), mask.shape is (height, width)
         raise ValueError("Mask shape must match image shape.")
    if mask.dtype != np.bool_:
        mask = mask.astype(np.bool_)

    # Apply the function to the entire image
    processed_image = func(image, *args, **kwargs)

    # Composite the processed region with the original image based on the mask
    # Convert images to numpy arrays for masking
    original_np = np.array(image)
    processed_np = np.array(processed_image)

    # Ensure arrays are compatible (e.g., same number of channels)
    if original_np.shape != processed_np.shape:
         # This might happen if the function changes the number of channels (e.g., grayscale)
         # Need to handle this case - for now, assume functions maintain channel count or convert processed_image back to original mode/channels
         # A safer approach might be to apply the function only to the masked region's data, but that's more complex.
         # Let's stick to the simpler composite approach for now, assuming functions return compatible images.
         # If a function changes mode (e.g., to L), convert processed_image back to original mode before compositing.
         if processed_image.mode != image.mode:
             processed_image = processed_image.convert(image.mode)
             processed_np = np.array(processed_image)
             if original_np.shape != processed_np.shape:
                  # Still a shape mismatch, this approach might not work for all functions.
                  # Need to refine or add specific handling per function type if necessary.
                  # For now, raise an error to indicate this limitation.
                  raise ValueError(f"Shape mismatch after processing and mode conversion: original {original_np.shape}, processed {processed_np.shape}. Cannot apply mask.")


    # Create a 3-channel mask if the image is RGB/RGBA
    if len(original_np.shape) == 3:
        mask_3d = np.stack([mask] * original_np.shape[2], axis=-1)
    else:
        mask_3d = mask # Mask is already 2D for grayscale

    # Use the mask to select pixels
    # Pixels where mask is True come from processed_np
    # Pixels where mask is False come from original_np
    composited_np = np.where(mask_3d, processed_np, original_np)

    return Image.fromarray(composited_np.astype(original_np.dtype), mode=image.mode)

def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """Adjusts the brightness of the image."""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    """Adjusts the contrast of the image."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
    """Adjusts the saturation of the image."""
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
    """Adjusts the sharpness of the image."""
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def apply_gamma_correction(image: Image.Image, gamma: float) -> Image.Image:
    """Applies gamma correction to the image."""
    if gamma == 1.0:
        return image
    if image.mode != 'RGB':
        image = image.convert('RGB')
    lut = [pow(x / 255., gamma) * 255 for x in range(256)]
    lut = lut * 3  # for R, G, B
    return image.point(lut)

def apply_blur(image: Image.Image, radius: float) -> Image.Image:
    """Applies Gaussian blur to the image."""
    if radius <= 0:
        return image
    return image.filter(ImageFilter.GaussianBlur(radius))

def apply_grayscale(image: Image.Image) -> Image.Image:
    """Applies grayscale filter to the image."""
    return image.convert('L').convert('RGB')

def apply_invert(image: Image.Image) -> Image.Image:
    """Applies invert filter to the image."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return ImageOps.invert(image)

def rotate_image(image: Image.Image, angle: float) -> Image.Image:
    return image.rotate(angle, expand=True)

import numpy as np
import cv2
from skimage import filters, util
from skimage.util import img_as_ubyte

def ai_enhance(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Placeholder for AI enhancement logic, optionally within a mask."""
    # Define the core AI enhancement logic (placeholder)
    def _ai_enhance_func(img: Image.Image) -> Image.Image:
        # Placeholder for AI enhancement logic
        # To be implemented with external AI libraries or APIs
        return img

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_ai_enhance_func, image, mask)

def remove_background(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Placeholder for background removal logic, optionally within a mask."""
    # Define the core background removal logic (placeholder)
    def _remove_background_func(img: Image.Image) -> Image.Image:
        # Placeholder for background removal logic
        # To be implemented with external AI libraries or APIs
        return img

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_remove_background_func, image, mask)

def apply_high_pass_filter(image: Image.Image, radius: int = 15, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply a high pass filter to enhance edges, optionally within a mask."""
    # Define the core high pass filter logic
    def _apply_high_pass_filter_func(img: Image.Image, r: int) -> Image.Image:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img)
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(img_gray, (r*2+1, r*2+1), 0)
        high_pass = cv2.addWeighted(img_gray, 1.5, blur, -0.5, 0)
        high_pass_rgb = cv2.cvtColor(high_pass, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(high_pass_rgb)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_high_pass_filter_func, image, mask, radius)

def apply_histogram_equalization(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply histogram equalization to improve contrast, optionally within a mask."""
    # Define the core histogram equalization logic
    def _apply_histogram_equalization_func(img: Image.Image) -> Image.Image:
        """Apply histogram equalization to improve contrast."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img)
        img_yuv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        img_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        return Image.fromarray(img_eq)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_histogram_equalization_func, image, mask)

def apply_contour_detection(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Detect and draw contours on the image, optionally within a mask."""
    # Define the core contour detection logic
    def _apply_contour_detection_func(img: Image.Image) -> Image.Image:
        """Detect and draw contours on the image."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img)
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(img_gray, 100, 200)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        # Overlay edges on original image
        overlay = cv2.addWeighted(img_cv, 0.8, edges_colored, 0.2, 0)
        return Image.fromarray(overlay)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_contour_detection_func, image, mask)

def add_gaussian_noise(image: Image.Image, mean=0, sigma=15, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Add Gaussian noise to the image, optionally within a mask."""
    # Define the core Gaussian noise logic
    def _add_gaussian_noise_func(img: Image.Image, m: int, s: int) -> Image.Image:
        """Add Gaussian noise to the image."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img).astype(np.float32)
        noise = np.random.normal(m, s, img_cv.shape).astype(np.float32)
        noisy_img = img_cv + noise
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_img)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_add_gaussian_noise_func, image, mask, mean, sigma)

def apply_pencil_sketch(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply pencil sketch effect, optionally within a mask."""
    # Define the core pencil sketch logic
    def _apply_pencil_sketch_func(img: Image.Image) -> Image.Image:
        """Apply pencil sketch effect."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img) # Convert the passed 'img' to numpy array
        gray, sketch = cv2.pencilSketch(img_cv, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return Image.fromarray(sketch)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_pencil_sketch_func, image, mask)

def apply_sepia(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply sepia filter, optionally within a mask."""
    # Define the core sepia logic
    def _apply_sepia_func(img: Image.Image) -> Image.Image:
        """Apply sepia filter."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img)
        kernel = np.array([[0.393, 0.769, 0.189],
                           [0.349, 0.686, 0.168],
                           [0.272, 0.534, 0.131]])
        sepia_img = cv2.transform(img_cv, kernel)
        sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
        return Image.fromarray(sepia_img)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_sepia_func, image, mask)

def crop_image(image: Image.Image, left: int, upper: int, right: int, lower: int) -> Image.Image:
    """Crop the image to the specified box."""
    return image.crop((left, upper, right, lower))

def apply_sharpen_filter(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply a sharpen filter using a kernel, optionally within a mask."""
    # Define the core sharpen filter logic
    def _apply_sharpen_filter_func(img: Image.Image) -> Image.Image:
        """Apply a sharpen filter using a kernel."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img)
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(img_cv, -1, kernel)
        return Image.fromarray(sharpened)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_sharpen_filter_func, image, mask)

def add_border(image: Image.Image, border_size: int, color=(0,0,0)) -> Image.Image:
    """Add a border of specified size and color around the image."""
    if border_size <= 0:
        return image
    return ImageOps.expand(image, border=border_size, fill=color)

def apply_xray_effect(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply an x-ray like effect, optionally within a mask."""
    # Define the core x-ray effect logic
    def _apply_xray_effect_func(img: Image.Image) -> Image.Image:
        """Apply an x-ray like effect."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_cv = np.array(img)
        inverted = cv2.bitwise_not(img_cv)
        gray = cv2.cvtColor(inverted, cv2.COLOR_RGB2GRAY)
        colored = cv2.applyColorMap(gray, cv2.COLORMAP_BONE)
        return Image.fromarray(colored)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_xray_effect_func, image, mask)

# New filters from Pillow and skimage

def apply_emboss(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply emboss filter, optionally within a mask."""
    # Define the core emboss logic
    def _apply_emboss_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.EMBOSS)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_emboss_func, image, mask)

def apply_edge_enhance(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply edge enhance filter, optionally within a mask."""
    # Define the core edge enhance logic
    def _apply_edge_enhance_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.EDGE_ENHANCE)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_edge_enhance_func, image, mask)

def apply_edge_enhance_more(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply edge enhance more filter, optionally within a mask."""
    # Define the core edge enhance more logic
    def _apply_edge_enhance_more_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_edge_enhance_more_func, image, mask)

def apply_find_edges(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply find edges filter, optionally within a mask."""
    # Define the core find edges logic
    def _apply_find_edges_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.FIND_EDGES)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_find_edges_func, image, mask)

def apply_detail(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply detail filter, optionally within a mask."""
    # Define the core detail logic
    def _apply_detail_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.DETAIL)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_detail_func, image, mask)

def apply_smooth(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply smooth filter, optionally within a mask."""
    # Define the core smooth logic
    def _apply_smooth_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.SMOOTH)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_smooth_func, image, mask)

def apply_smooth_more(image: Image.Image, mask: Optional[np.ndarray] = None) -> Image.Image:
    """Apply smooth more filter, optionally within a mask."""
    # Define the core smooth more logic
    def _apply_smooth_more_func(img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.SMOOTH_MORE)

    # Apply the logic using the helper function with the mask
    return apply_with_mask(_apply_smooth_more_func, image, mask)

def apply_laplace(image: Image.Image) -> Image.Image:
    """Apply laplace filter."""
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    lap = filters.laplace(img_np)
    lap_img = img_as_ubyte(lap)
    return Image.fromarray(lap_img).convert('RGB')

def apply_sobel(image: Image.Image) -> Image.Image:
    """Apply sobel filter."""
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    sobel_img = filters.sobel(img_np)
    sobel_img = img_as_ubyte(sobel_img)
    return Image.fromarray(sobel_img).convert('RGB')

def apply_scharr(image: Image.Image) -> Image.Image:
    """Apply scharr filter."""
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    scharr_img = filters.scharr(img_np)
    scharr_img = img_as_ubyte(scharr_img)
    return Image.fromarray(scharr_img).convert('RGB')

def apply_prewitt(image: Image.Image) -> Image.Image:
    """Apply prewitt filter."""
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    prewitt_img = filters.prewitt(img_np)
    prewitt_img = img_as_ubyte(prewitt_img)
    return Image.fromarray(prewitt_img).convert('RGB')

def apply_roberts(image: Image.Image) -> Image.Image:
    """Apply roberts filter."""
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    roberts_img = filters.roberts(img_np)
    roberts_img = img_as_ubyte(roberts_img)
    return Image.fromarray(roberts_img).convert('RGB')

def apply_gabor(image: Image.Image, frequency=0.6) -> Image.Image:
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    real, imag = filters.gabor(img_np, frequency=frequency)
    gabor_img = img_as_ubyte(real)
    return Image.fromarray(gabor_img).convert('RGB')

def apply_otsu_threshold(image: Image.Image) -> Image.Image:
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    thresh = filters.threshold_otsu(img_np)
    binary = img_np > thresh
    binary_img = (binary * 255).astype(np.uint8)
    return Image.fromarray(binary_img).convert('RGB')

def create_rectangle_mask(image_shape: tuple[int, int], point1: tuple[int, int], point2: tuple[int, int]) -> np.ndarray:
    """Creates a boolean mask for a rectangle. Assumes image_shape is (height, width) and points are (row, col)."""
    mask = np.zeros(image_shape, dtype=np.uint8)
    # Ensure points are in (x, y) format for cv2 (col, row)
    pt1_cv = (point1[1], point1[0])
    pt2_cv = (point2[1], point2[0])
    cv2.rectangle(mask, pt1_cv, pt2_cv, 255, -1) # Fill the rectangle
    return mask.astype(np.bool_)

def create_ellipse_mask(image_shape: tuple[int, int], center: tuple[int, int], axes: tuple[int, int]) -> np.ndarray:
    """Creates a boolean mask for an ellipse. Assumes image_shape is (height, width) and center/axes are (row, col)."""
    mask = np.zeros(image_shape, dtype=np.uint8)
    # Ensure center and axes are in (x, y) format for cv2 (col, row)
    center_cv = (center[1], center[0])
    axes_cv = (axes[1], axes[0])
    cv2.ellipse(mask, center_cv, axes_cv, 0, 0, 360, 255, -1) # Fill the ellipse
    return mask.astype(np.bool_)

def create_lasso_mask(image_shape: tuple[int, int], coordinates: list[tuple[int, int]]) -> np.ndarray:
    """Creates a boolean mask for a free-form lasso selection. Assumes image_shape is (height, width) and coordinates are (row, col)."""
    mask = np.zeros(image_shape, dtype=np.uint8)
    # Ensure coordinates are in (x, y) format for cv2 (col, row) and in the required shape
    pts_cv = np.array([(p[1], p[0]) for p in coordinates], np.int32)
    cv2.fillPoly(mask, [pts_cv], 255) # Fill the polygon
    return mask.astype(np.bool_)

def apply_niblack_threshold(image: Image.Image, window_size=25, k=0.8) -> Image.Image:
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    thresh = filters.threshold_niblack(img_np, window_size=window_size, k=k)
    binary = img_np > thresh
    binary_img = (binary * 255).astype(np.uint8)
    return Image.fromarray(binary_img).convert('RGB')

def apply_sauvola_threshold(image: Image.Image, window_size=25, k=0.8) -> Image.Image:
    if image.mode != 'L':
        image = image.convert('L')
    img_np = np.array(image)
    thresh = filters.threshold_sauvola(img_np, window_size=window_size, k=k)
    binary = img_np > thresh
    binary_img = (binary * 255).astype(np.uint8)
    return Image.fromarray(binary_img).convert('RGB')
