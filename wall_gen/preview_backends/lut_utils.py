# preview_backends/lut_utils.py
"""
Utilities for loading and applying 3D LUTs (Look-Up Tables) to images.
Requires 'pillow-lut-tools' to be installed: pip install pillow-lut-tools
"""
from PIL import Image
try:
    from pillow_lut import load_cube_file
except ImportError:
    print("ImportError: pillow-lut-tools is not installed. Please install it using 'pip install pillow-lut-tools'")
    load_cube_file = None # Placeholder if not installed

def load_lut_from_file(lut_path):
    """
    Loads a .cube LUT file using pillow-lut-tools.

    Args:
        lut_path (str): The file path to the .cube LUT file.

    Returns:
        ImageFilter.Color3DLUT or None: The loaded LUT object if successful, None otherwise.
    """
    if load_cube_file is None:
        print("Cannot load LUT: pillow-lut-tools is not available.")
        return None
    try:
        lut = load_cube_file(lut_path)
        print(f"Successfully loaded LUT: {lut_path}")
        return lut
    except Exception as e:
        print(f"Error loading LUT file {lut_path}: {e}")
        return None

def apply_lut_to_pil_image(pil_image, lut_object):
    """
    Applies a loaded LUT object to a PIL image.

    Args:
        pil_image (PIL.Image.Image): The image to apply the LUT to.
        lut_object (ImageFilter.Color3DLUT): The LUT object loaded by load_lut_from_file.

    Returns:
        PIL.Image.Image: The image with the LUT applied, or the original image if an error occurs.
    """
    if not lut_object or not pil_image:
        print("Cannot apply LUT: LUT object or PIL image is missing.")
        return pil_image
    
    if load_cube_file is None: # Check again in case it wasn't available at module load time
        print("Cannot apply LUT: pillow-lut-tools is not available.")
        return pil_image

    try:
        # Ensure the image is in RGB mode as LUTs typically operate on RGB color space.
        # If the image has an alpha channel (RGBA), it should be preserved if possible,
        # but LUTs themselves usually transform RGB. pillow-lut-tools handles RGB.
        if pil_image.mode == 'RGBA':
            rgb_image = pil_image.convert("RGB")
            processed_rgb_image = rgb_image.filter(lut_object)
            # Re-attach alpha channel if it existed
            alpha = pil_image.split()[-1]
            return Image.merge("RGBA", (*processed_rgb_image.split(), alpha))
        elif pil_image.mode == 'P': # Palette mode
             rgb_image = pil_image.convert("RGB")
             return rgb_image.filter(lut_object)
        else:
            return pil_image.convert("RGB").filter(lut_object)
            
    except Exception as e:
        print(f"Error applying LUT to image: {e}")
        return pil_image

if __name__ == '__main__':
    # Example Usage (requires a .cube file and an image file for testing)
    # Create a dummy PIL image for testing if pillow-lut-tools is installed
    if load_cube_file:
        try:
            img = Image.new("RGB", (100, 100), color="red")
            # You would need a sample .cube file path here
            # lut_path = "path/to/your/sample.cube" 
            # loaded_lut = load_lut_from_file(lut_path)
            # if loaded_lut:
            #     transformed_img = apply_lut_to_pil_image(img, loaded_lut)
            #     transformed_img.show()
            # else:
            #     print("LUT could not be loaded for the test.")
            print("lut_utils.py executed. For a full test, provide a .cube file and an image.")
        except Exception as e:
            print(f"Error in lut_utils.py example: {e}")
    else:
        print("pillow-lut-tools not found, skipping example.")
