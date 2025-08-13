import requests
from PIL import Image
import os
from io import BytesIO
import re
import logging

logger = logging.getLogger(__name__)

# youtube music thumbnails can also be grabbed in this manner


# this function is taken from https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486?permalink_comment_id=5097394#gistcomment-5097394
def get_youtube_video_id_by_url(url):
    regex = r"^((https?://(?:www\.)?(?:m\.)?youtube\.com))/((?:oembed\?url=https?%3A//(?:www\.)youtube.com/watch\?(?:v%3D)(?P<video_id_1>[\w\-]{10,20})&format=json)|(?:attribution_link\?a=.*watch(?:%3Fv%3D|%3Fv%3D)(?P<video_id_2>[\w\-]{10,20}))(?:%26feature.*))|(https?:)?(\/\/)?((www\.|m\.)?youtube(-nocookie)?\.com\/((watch)?\?(app=desktop&)?(feature=\w*&)?v=|embed\/|v\/|e\/)|youtu\.be\/)(?P<video_id_3>[\w\-]{10,20})"
    match = re.match(regex, url, re.IGNORECASE)
    if match:
        return (
            match.group("video_id_1")
            or match.group("video_id_2")
            or match.group("video_id_3")
        )
    else:
        return None


# if yt link if provided, generate two videos: square and landscape
def get_yt_thumbnail(url: str) -> str | None:
    """Get the thumbnail of a song using its youtube url

    Args:
        url (str): YouTube url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    logger.info(f"Starting YouTube thumbnail extraction for URL: {url}")
    video_id: str = get_youtube_video_id_by_url(url)
    if not video_id:
        logger.error(f"Could not extract video ID from URL: {url}")
        return None
    logger.info(f"Extracted video ID: {video_id}")
    save_name = video_id
    save_path = os.path.join("./assets/overlay/youtube", f"{save_name}.jpg")
    os.makedirs("./assets/overlay/youtube", exist_ok=True)

    # check if this thumbnail is already available, and return it if it exists
    if os.path.exists(save_path):
        logger.info(f"Using existing YouTube thumbnail: {save_path}")
        return save_path
    thumbnail_url: str = "https://img.youtube.com/vi/" + video_id + "/maxresdefault.jpg"
    logger.info(f"Downloading YouTube thumbnail from: {thumbnail_url}")

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
    get_yt_thumbnail(
        ""
    )
