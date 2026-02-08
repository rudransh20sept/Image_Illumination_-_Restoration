# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

# -------- Enhancement functions -------- #

def auto_brightness_contrast(img, target_brightness=128, contrast=30):
    """Automatically adjust brightness & contrast."""
    if len(img.shape) == 2:
        gray = img
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    brightness_shift = target_brightness - mean_brightness
    alpha = 1 + contrast / 127.0
    return cv2.convertScaleAbs(img, alpha=alpha, beta=brightness_shift)

def clahe_enhance(img, clip_limit=3.0, tile_grid_size=(8, 8)):
    """Apply CLAHE in LAB color space."""
    if len(img.shape) == 2:
        lab = cv2.cvtColor(img, cv2.COLOR_GRAY2LAB)
    else:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    if len(img.shape) == 2:
        return cv2.cvtColor(limg, cv2.COLOR_LAB2GRAY)
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

def denoise_bilateral(img, d=9, sigma_color=75, sigma_space=75):
    """Apply bilateral filter for edge-preserving noise reduction."""
    return cv2.bilateralFilter(img, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)

def enhance_colors(img, saturation_factor=1.2):
    """Boost saturation in HSV space."""
    if len(img.shape) == 2:
        return img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= saturation_factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return enhanced

# -------- Main entry function -------- #

def em(input_path, output_dir=None, target_brightness=128, contrast=30,
       clip_limit=3.0, saturation_factor=1.2, denoise_strength=75,
       verbose=False):
    """
    Enhanced pipeline with color-enhanced image as final output:
      1. Auto Brightness/Contrast
      2. CLAHE
      3. Bilateral Denoising
      4. Color Enhancement (final output)

    Args:
        input_path (str): Path to input image.
        output_dir (str, optional): Where to save enhanced images.
        target_brightness (int): Desired brightness level.
        contrast (int): Contrast adjustment factor.
        clip_limit (float): CLAHE clip limit.
        saturation_factor (float): HSV saturation multiplier.
        denoise_strength (int): Bilateral sigma_color/space.
        verbose (bool): Print progress and diagnostics.

    Returns:
        bool: True if successful.
    """
    if verbose:
        print(f"Loading image: {input_path}")
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {input_path}")
    
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    if verbose:
        print(f"Input image min/max: {img.min()}/{img.max()}")

    # Step 1: Auto Brightness/Contrast
    if verbose:
        print("Step 1: Auto Brightness/Contrast")
    bc = auto_brightness_contrast(img, target_brightness, contrast)
    if verbose:
        print(f"Brightness/Contrast min/max: {bc.min()}/{bc.max()}")

    # Step 2: CLAHE
    if verbose:
        print("Step 2: CLAHE Enhancement")
    clahe = clahe_enhance(bc, clip_limit=clip_limit)
    if verbose:
        print(f"CLAHE min/max: {clahe.min()}/{clahe.max()}")

    # Step 3: Denoise
    if verbose:
        print("Step 3: Bilateral Denoising")
    denoised = denoise_bilateral(clahe, sigma_color=denoise_strength, sigma_space=denoise_strength)
    if verbose:
        print(f"Denoised min/max: {denoised.min()}/{denoised.max()}")

    # Step 4: Color boost (final output)
    if verbose:
        print("Step 4: Color Enhancement")
    colors = enhance_colors(denoised, saturation_factor=saturation_factor)
    if verbose:
        print(f"Colors min/max: {colors.min()}/{colors.max()}")

    # Save results
    if output_dir is None:
        output_dir = os.path.dirname(input_path) or "."
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    quality = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

    cv2.imwrite(os.path.join(output_dir, f"{base_name}_brightness_contrast.jpg"), bc, quality)
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_clahe.jpg"), clahe, quality)
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_denoised.jpg"), denoised, quality)
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_colors.jpg"), colors, quality)
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_final.jpg"), colors, quality)

    if verbose:
        print(f"Enhancement complete. Outputs saved to: {output_dir}")
    return True