"""
This uses the Youtube Method for Youtube Music thumbnails. This can be used as a fallback.
"""
import requests
from PIL import Image
import os
from io import BytesIO
import logging
from urllib.parse import urlparse, parse_qs


logger = logging.getLogger(__name__)


def get_youtube_music_video_id_by_url(url):
    if "music.youtube.com" in url.lower():
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]

    return None


# if yt link if provided, generate two videos: square and landscape
def get_ytmusic_thumbnail(url: str) -> None | str:
    """Get the thumbnail of a song using its youtube music url

    Args:
        url (str): YouTube Music url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    logger.info(f"Starting YouTube Music thumbnail extraction for URL: {url}")
    video_id: str = get_youtube_music_video_id_by_url(url)
    if not video_id:
        logger.error(f"Could not extract video ID from URL: {url}")
        return None
    logger.info(f"Extracted video ID: {video_id}")
    save_name = video_id
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    thumbnails_dir = os.path.join(script_dir, "assets", "thumbnails", "youtube")
    save_path = os.path.join(thumbnails_dir, f"{save_name}.jpg")
    os.makedirs(thumbnails_dir, exist_ok=True)

    # check if this thumbnail is already available, and return it if it exists
    if os.path.exists(save_path):
        logger.info(f"Using existing YouTube Music thumbnail: {save_path}")
        return save_path
    thumbnail_url: str = "https://img.youtube.com/vi/" + video_id + "/maxresdefault.jpg"
    logger.info(f"Downloading YouTube Music thumbnail from: {thumbnail_url}")

    try:
        rr = requests.get(thumbnail_url)
        if rr.status_code != 200:
            logger.error(f"Failed to download thumbnail. Status code: {rr.status_code}")
            return None

        with Image.open(BytesIO(rr.content)) as im:
            # Crop from center to make it square, then resize to 512x512
            width, height = im.size
            logger.info(f"Original image dimensions: {width}x{height}")
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size

            cropped_im = im.crop((left, top, right, bottom))
            resized_im = cropped_im.resize((512, 512), Image.Resampling.LANCZOS)
            resized_im.save(save_path, format="JPEG")
            logger.info(f"YouTube Music thumbnail saved successfully to: {save_path}")
            return save_path
    except Exception as e:
        logger.error(f"Failed to process YouTube Music thumbnail: {e}")
        return None


if __name__ == "__main__":
    get_ytmusic_thumbnail(
        "https://music.youtube.com/watch?v=8ECPu3iumnE&si=EnXmtbLcrYGVP1u1"
    )
