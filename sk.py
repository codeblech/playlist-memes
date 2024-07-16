import skimage as ski
from skimage import io, transform
from matplotlib import pyplot as plt
from PIL import Image
import json
import numpy as np


def read_metadata(input_path: str) -> dict | None:
    """Reads a text chunk with key="metadata" from given PNG image.

    Args:
        input_path (str): path to the PNG image file

    Returns:
        dict | None: metadata dictionary if found, None otherwise
    """
    with Image.open(input_path) as img:
        if metadata := json.loads(img.info.get("metadata", None)):
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
    a0, a1, a2, b0, b1, b2, _, _, _ = metadata["transformation_matrices"][0]
    matrix = np.array([[a0, a1, a2], [b0, b1, b2], [0, 0, 1]])
    return matrix


matrix = get_transformation_matrix(
    read_metadata("assets/background/1/photo_2024-07-15_01-07-27.png")
)


background = io.imread("assets/background/1/photo_2024-07-15_01-07-27.png")
# Read overlay image with alpha channel
overlay = io.imread("assets/overlay/3p19TG5Qia8j2XXL.jpg", as_gray=False, plugin="pil")
if overlay.shape[2] == 3:  # If image doesn't have an alpha channel, add one
    overlay = np.dstack((overlay, np.ones(overlay.shape[:2], dtype=np.uint8) * 255))

# Read background image
background = io.imread("assets/background/1/photo_2024-07-15_01-07-27.png")

# Create the AffineTransform object
tform = transform.AffineTransform(matrix=matrix)

# Apply the transformation with a transparent background
transformed_overlay = transform.warp(
    overlay, tform.inverse, order=1, preserve_range=True
)
transformed_overlay = transformed_overlay.astype(np.uint8)

# Save the transformed overlay with transparency
tov = Image.fromarray(transformed_overlay)
tov.save("transformed_overlay.png")

# Resize the transformed overlay if necessary
if transformed_overlay.shape[:2] != background.shape[:2]:
    transformed_overlay = transform.resize(
        transformed_overlay,
        (background.shape[0], background.shape[1], 4),
        mode="edge",
        anti_aliasing=True,
        preserve_range=True,
    ).astype(np.uint8)

# Save the resized transformed overlay with transparency
r_tov = Image.fromarray(transformed_overlay)
r_tov.save("resized_transformed_overlay.png")
