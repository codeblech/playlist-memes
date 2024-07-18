import skimage as ski
from skimage import io, transform
from PIL import Image
import json
import numpy as np
from datetime import datetime
import os
from pathlib import Path


def read_metadata(input_path: str) -> dict | None:
    """Reads a text chunk with key="metadata" from given PNG image.

    Args:
        input_path (str): path to the PNG image file

    Returns:
        dict | None: metadata dictionary if found, None otherwise
    """
    with Image.open(input_path) as img:
        if metadata := json.loads(img.info.get("metadata", None)):
            print(metadata)
            return metadata
        else:
            return None


def get_transformation_matrix(metadata: dict) -> list[float]:
    """Extracts the transformation matrix from the metadata dictionary.

    Args:
        metadata (dict): metadata dictionary

    Returns:
        list[float]: transformation matrix
    """
    matrix = np.array(metadata["transformation_matrices"][0]).reshape(3, 3)
    print(matrix)
    return matrix

def has_mask(metadata: dict) -> bool:
    x = metadata.get("has_mask")
    print(f"x: {x}")
    if x is True:
        return True
    else:
        return False


def apply_overlay_transformation(
    background_path, overlay_path, save_transformed_overlay=False
) -> Path | None:
    metadata = read_metadata(background_path)
    if metadata is None:
        print("No Metadata present in given background image")
        return

    matrix = get_transformation_matrix(metadata=metadata)

    # Open background and overlay images
    background = Image.open(background_path)
    overlay = Image.open(overlay_path)

    # Convert overlay to RGBA if it's not already
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")

    # Create a new transparent image with the same size as the background
    padded_overlay = Image.new("RGBA", background.size, (0, 0, 0, 0))

    # Paste the overlay onto the padded image
    padded_overlay.paste(overlay, (0, 0), overlay)

    # Convert to numpy array for transformation
    overlay_array = np.array(padded_overlay)

    # Use ProjectiveTransform instead of AffineTransform
    tform = transform.ProjectiveTransform(matrix=matrix)
    transformed_overlay = transform.warp(
        overlay_array,
        tform.inverse,
        order=0,
        preserve_range=True,
    )
    transformed_overlay = transformed_overlay.astype(np.uint8)
    transformed_img = Image.fromarray(transformed_overlay)

    if save_transformed_overlay:
        transformed_img.save("transformed_overlay.png")

    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".png"
    # Extracting the base filenames without extensions
    overlay_filename = os.path.basename(overlay_path).split(".")[0]
    background_filename = os.path.basename(background_path).split(".")[0]

    output_name = f"{overlay_filename}_o_{background_filename}_t_{current_time}.png"
    output_path = "./outputs/" + output_name

    try:
        background.paste(transformed_img, (0, 0), transformed_img)
        background.save(output_path, "PNG")
        return Path(output_path)
    except Exception as e:
        print(f"Error saving output: {e}")
        return None


if __name__ == "__main__":
    background = "assets/background/1/pope.png"
    overlay = "assets/overlay/AUacb2ai-pAH-iDl.jpg"
    result = apply_overlay_transformation(
        background, overlay, save_transformed_overlay=True
    )
    if result:
        print(f"Output saved to: {result}")
    else:
        print("Failed to generate output")
