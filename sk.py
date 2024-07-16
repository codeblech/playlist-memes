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
image = io.imread("assets/overlay/3p19TG5Qia8j2XXL.jpg")
# Create the AffineTransform object
tform = transform.AffineTransform(matrix=matrix)

# Apply the transformation
transformed_image = transform.warp(image, tform.inverse)

# Display the original and transformed images
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.imshow(image)
ax1.set_title("Original Image")
ax1.axis("off")

ax2.imshow(transformed_image)
ax2.set_title("Transformed Image")
ax2.axis("off")

plt.tight_layout()
plt.show()
