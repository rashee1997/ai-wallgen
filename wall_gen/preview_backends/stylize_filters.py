# preview_backends/stylize_filters.py
"""
Collection of artistic stylization filters for images.
Requires 'opencv-python' and 'numpy'.
"""
import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(pil_image):
    """Convert PIL Image to OpenCV image (BGR)."""
    # Convert RGBA or RGB to RGB first if necessary
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')
    elif pil_image.mode == 'L': # Grayscale
        pil_image = pil_image.convert('RGB') # Convert to RGB for color filters
    elif pil_image.mode == 'P': # Palette
        pil_image = pil_image.convert('RGB')

    cv_image = np.array(pil_image)
    # Convert RGB to BGR
    cv_image = cv_image[:, :, ::-1].copy()
    return cv_image

def cv2_to_pil(cv_image):
    """Convert OpenCV image (BGR) to PIL Image."""
    # Convert BGR to RGB
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv_image_rgb)

def apply_oil_painting(pil_image, size=7, dyn_ratio=1):
    """
    Applies an oil painting effect to a PIL image.

    Args:
        pil_image (PIL.Image.Image): The input image.
        size (int): Size of the neighborhood for filtering.
        dyn_ratio (int): Contrast parameter.

    Returns:
        PIL.Image.Image: The image with the oil painting effect.
    """
    if pil_image is None:
        return None
    try:
        cv_image = pil_to_cv2(pil_image)
        # xphoto.oilPainting is available in opencv-contrib-python
        # If using standard opencv-python, this might not be available.
        # For this example, we assume it's available.
        # Ensure the image is 8-bit, 3-channel for oilPainting
        if cv_image.dtype != np.uint8:
            cv_image = cv_image.astype(np.uint8) # Or handle more gracefully
        
        if len(cv_image.shape) == 2 or cv_image.shape[2] == 1: # Grayscale
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)


        res = cv2.xphoto.oilPainting(cv_image, size, dyn_ratio)
        return cv2_to_pil(res)
    except AttributeError:
        print("cv2.xphoto.oilPainting not found. Is opencv-contrib-python installed and updated?")
        return pil_image # Return original if effect fails
    except Exception as e:
        print(f"Error applying oil painting effect: {e}")
        return pil_image

def apply_cartoon_effect(pil_image, ksize=5, sketch_mode=False):
    """
    Applies a cartoon effect to a PIL image.
    This is a simplified version. More advanced techniques exist.

    Args:
        pil_image (PIL.Image.Image): The input image.
        ksize (int): Kernel size for median blur.
        sketch_mode (bool): If True, returns a more sketch-like black and white image.

    Returns:
        PIL.Image.Image: The image with the cartoon effect.
    """
    if pil_image is None:
        return None
    try:
        cv_image = pil_to_cv2(pil_image)
        
        # 1. Edge detection
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, ksize) # Reduce noise for edge detection
        edges = cv2.adaptiveThreshold(gray_blur, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY,
                                      blockSize=9, C=2)
        if sketch_mode:
            return cv2_to_pil(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))

        # 2. Color quantization (using K-Means clustering)
        # Reshape image to be a list of pixels
        pixels = np.float32(cv_image.reshape(-1, 3))
        n_colors = 8 # Number of dominant colors
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centers = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        
        centers = np.uint8(centers)
        quantized_colors = centers[labels.flatten()]
        quantized_image = quantized_colors.reshape(cv_image.shape)

        # 3. Combine edges with quantized colors
        # Convert edges to 3 channels to use as a mask
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        # Where edges are black (0), use quantized color. Where white (255), keep edge.
        cartoon_image = cv2.bitwise_and(quantized_image, quantized_image, mask=cv2.bitwise_not(edges))
        
        # A simpler way to combine: make edges black on the color image
        # cartoon_image = quantized_image
        # cartoon_image[edges == 255] = [0, 0, 0] # Make edges black

        return cv2_to_pil(cartoon_image)
    except Exception as e:
        print(f"Error applying cartoon effect: {e}")
        return pil_image

if __name__ == '__main__':
    # Example Usage (requires an image file for testing)
    try:
        # Create a dummy PIL image for testing
        img = Image.new("RGB", (200, 200), color="lightblue")
        pixels = img.load()
        for i in range(img.width):
            for j in range(img.height):
                if (i // 20 + j // 20) % 2 == 0:
                    pixels[i,j] = (255,105,180) # hotpink
                else:
                    pixels[i,j] = (173,216,230) # lightblue


        # Test Oil Painting
        oil_painted_img = apply_oil_painting(img.copy(), size=5, dyn_ratio=1)
        if oil_painted_img:
            print("Oil painting effect applied (check if cv2.xphoto is available).")
            # oil_painted_img.show() # Uncomment to display

        # Test Cartoon Effect
        cartoon_img = apply_cartoon_effect(img.copy())
        if cartoon_img:
            print("Cartoon effect applied.")
            # cartoon_img.show() # Uncomment to display
            
        # Test Cartoon Sketch Mode
        cartoon_sketch_img = apply_cartoon_effect(img.copy(), sketch_mode=True)
        if cartoon_sketch_img:
            print("Cartoon sketch effect applied.")
            # cartoon_sketch_img.show() # Uncomment to display


    except Exception as e:
        print(f"Error in stylize_filters.py example: {e}")
