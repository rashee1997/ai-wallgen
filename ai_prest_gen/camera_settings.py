"""
Camera Settings Module for AI Preset Generator.

This module provides functions to generate dynamic and contextually appropriate
camera settings for various style categories, primarily targeting photographic
and 3D rendering styles to enhance realism and technical accuracy in generated presets.
"""

from typing import Dict, Any

def get_dynamic_camera_settings(style_category: str) -> Dict[str, Any]:
    """
    Returns a dictionary of dynamic camera settings tailored to the given style category.

    If a specific style category is not explicitly handled, it falls back to a set of
    default common camera settings suitable for general photographic purposes.

    Args:
        style_category (str): The normalized (lowercase) style category name
                              (e.g., "photographic", "cinematic", "macro").

    Returns:
        Dict[str, Any]: A dictionary containing camera parameters such as
                        camera_model, lens_type, aperture, focal_length, etc.
    """
    style_category = style_category.lower()

    if style_category == "photographic":
        return {
            "camera_model": "DSLR", "lens_type": "Prime (50mm)", "aperture": "f/2.8",
            "focal_length": "50mm", "shutter_speed": "1/125s", "iso": "ISO 200",
            "filter_type": "None", "depth_of_field": "Medium", "white_balance": "Auto",
            "focus_mode": "Autofocus Single (AF-S/One-Shot)", "exposure_mode": "Aperture Priority (Av/A)",
            "image_stabilization": "Optical (OIS in lens)", "metering_mode": "Evaluative/Matrix",
            "flash_mode": "Off", "shooting_mode": "Single Shot",
            "focus_point_selection": "Single Point AF", "image_format": "RAW", "color_space": "sRGB"
        }
    elif style_category == "cinematic":
        return {
            "camera_model": "Cinema Camera (e.g., RED Komodo)", "lens_type": "Cine Prime (e.g., 35mm T1.5)",
            "aperture": "T1.5", "focal_length": "35mm", "shutter_speed": "1/48s", "iso": "ISO 800",
            "filter_type": "ND Filter", "depth_of_field": "Shallow", "white_balance": "Custom",
            "focus_mode": "Manual Focus", "exposure_mode": "Manual",
            "image_stabilization": "Gimbal Stabilizer", "metering_mode": "Spot Metering",
            "flash_mode": "Off", "shooting_mode": "Continuous",
            "focus_point_selection": "Manual", "image_format": "RAW CinemaDNG", "color_space": "DCI-P3"
        }
    elif style_category == "documentary":
        return {
            "camera_model": "Mirrorless Camera (e.g., Sony A7S III)", "lens_type": "Zoom Lens (e.g., 24-70mm)",
            "aperture": "f/4.0", "focal_length": "24-70mm", "shutter_speed": "1/60s", "iso": "ISO 1600",
            "filter_type": "Polarizer", "depth_of_field": "Medium", "white_balance": "Auto",
            "focus_mode": "Continuous Autofocus", "exposure_mode": "Auto",
            "image_stabilization": "In-Body Image Stabilization (IBIS)", "metering_mode": "Center-Weighted",
            "flash_mode": "Off", "shooting_mode": "Single Shot",
            "focus_point_selection": "Face/Eye Detection", "image_format": "MP4", "color_space": "Rec.709"
        }
    elif style_category == "street_photography":
        return {
            "camera_model": "Rangefinder Camera (e.g., Leica M10)", "lens_type": "Wide-Angle Prime (e.g., 28mm)",
            "aperture": "f/5.6", "focal_length": "28mm", "shutter_speed": "1/250s", "iso": "ISO 400",
            "filter_type": "None", "depth_of_field": "Deep", "white_balance": "Auto",
            "focus_mode": "Zone Focus", "exposure_mode": "Aperture Priority",
            "image_stabilization": "None", "metering_mode": "Matrix",
            "flash_mode": "Off", "shooting_mode": "Continuous",
            "focus_point_selection": "Zone", "image_format": "JPEG", "color_space": "sRGB"
        }
    elif style_category == "environmental_portrait":
        return {
            "camera_model": "DSLR (e.g., Canon EOS 5D Mark IV)", "lens_type": "Wide-Angle Prime (e.g., 35mm)",
            "aperture": "f/4.0", "focal_length": "35mm", "shutter_speed": "1/125s", "iso": "ISO 200",
            "filter_type": "None", "depth_of_field": "Medium to Deep", "white_balance": "Auto",
            "focus_mode": "Autofocus Single (AF-S/One-Shot)", "exposure_mode": "Aperture Priority (Av/A)",
            "image_stabilization": "Optical (OIS in lens)", "metering_mode": "Evaluative/Matrix",
            "flash_mode": "Off", "shooting_mode": "Single Shot",
            "focus_point_selection": "Single Point AF", "image_format": "RAW", "color_space": "sRGB"
        }
    elif style_category == "fashion_portrait":
        return {
            "camera_model": "DSLR (e.g., Canon EOS 5D Mark IV)", "lens_type": "Telephoto Prime (e.g., 135mm)",
            "aperture": "f/2.8", "focal_length": "135mm", "shutter_speed": "1/125s", "iso": "ISO 200",
            "filter_type": "None", "depth_of_field": "Shallow", "white_balance": "Auto",
            "focus_mode": "Autofocus Single (AF-S/One-Shot)", "exposure_mode": "Aperture Priority (Av/A)",
            "image_stabilization": "Optical (OIS in lens)", "metering_mode": "Evaluative/Matrix",
            "flash_mode": "Off", "shooting_mode": "Single Shot",
            "focus_point_selection": "Single Point AF", "image_format": "RAW", "color_space": "sRGB"
        }
    elif style_category == "selfie_portrait":
        return {
            "camera_model": "Smartphone Front Camera", "lens_type": "Wide-Angle Lens",
            "aperture": "f/1.8", "focal_length": "26mm", "shutter_speed": "1/60s", "iso": "ISO 400",
            "filter_type": "Beauty Filter", "depth_of_field": "Deep", "white_balance": "Auto",
            "focus_mode": "Face Detection Autofocus", "exposure_mode": "Auto",
            "image_stabilization": "Electronic Image Stabilization (EIS)", "metering_mode": "Center-Weighted",
            "flash_mode": "Screen Flash", "shooting_mode": "Single Shot",
            "focus_point_selection": "Face Priority", "image_format": "JPEG", "color_space": "sRGB"
        }
    else:
        # Default common camera settings
        return {
            "camera_model": "DSLR", "lens_type": "Prime (50mm)", "aperture": "f/2.8",
            "focal_length": "50mm", "shutter_speed": "1/125s", "iso": "ISO 200",
            "filter_type": "None", "depth_of_field": "Medium", "white_balance": "Auto",
            "focus_mode": "Autofocus Single (AF-S/One-Shot)", "exposure_mode": "Aperture Priority (Av/A)",
            "image_stabilization": "Optical (OIS in lens)", "metering_mode": "Evaluative/Matrix",
            "flash_mode": "Off", "shooting_mode": "Single Shot",
            "focus_point_selection": "Single Point AF", "image_format": "RAW", "color_space": "sRGB"
        }
