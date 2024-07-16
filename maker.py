import skimage as ski
from skimage import io, transform
from PIL import Image
import json
import numpy as np
from datetime import datetime


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


def apply_overlay_transformation(background_path, overlay_path, save_transformed_overlay=False):
    metadata = read_metadata(background_path)
    if metadata is None:
        print("No Metadata present in given background image")
        return
    matrix = get_transformation_matrix(metadata=metadata)

    overlay = io.imread(overlay_path, as_gray=False, plugin="pil")
    if overlay.shape[2] == 3:  # If image doesn't have an alpha channel, add one
        overlay = np.dstack((overlay, np.ones(overlay.shape[:2], dtype=np.uint8) * 255))

    tform = transform.AffineTransform(matrix=matrix)

    transformed_overlay = transform.warp(
        overlay, tform.inverse, order=0, preserve_range=True
    )
    transformed_overlay = transformed_overlay.astype(np.uint8)

    transformed_img = Image.fromarray(transformed_overlay)
    if save_transformed_overlay:
        transformed_img.save("transformed_overlay.png")

    output_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".png"
    with Image.open(background_path) as bg:
        bg.paste(transformed_img, (0, 0), transformed_img)
        bg.save(output_name, "PNG")


if __name__ == "__main__":
    background = "assets/background/1/photo_2024-07-15_01-07-27.png"
    overlay = "assets/overlay/3p19TG5Qia8j2XXL.jpg"
    apply_overlay_transformation(background, overlay)