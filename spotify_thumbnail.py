import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

import os
import requests
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

load_dotenv()


def get_spotify_thumbnail(url: str) -> None | str:
    logger.info(f"Starting Spotify thumbnail extraction for URL: {url}")
    try:
        # spotify = spotipy.Spotify(auth_manager=SpotifyOAuth())
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        result = spotify.track(url)

        thumbnail_url = result["album"]["images"][0]["url"]
        id = result["album"]["artists"][0]["id"]
        logger.info(f"Found artist ID: {id}, thumbnail URL: {thumbnail_url}")
        save_name = id
    except Exception as e:
        logger.error(f"Failed to get Spotify track info: {e}")
        return None

    save_path = os.path.join("./assets/overlay/spotify", f"{save_name}.jpg")
    os.makedirs("./assets/overlay/spotify", exist_ok=True)

    # check if this thumbnail is already available, and return it if it exists
    if os.path.exists(save_path):
        logger.info(f"Using existing Spotify thumbnail: {save_path}")
        return save_path

    try:
        logger.info(f"Downloading Spotify thumbnail from: {thumbnail_url}")
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
            logger.info(f"Spotify thumbnail saved successfully to: {save_path}")
            return save_path
    except Exception as e:
        logger.error(f"Failed to process Spotify thumbnail: {e}")
        return None


if __name__ == "__main__":
    get_spotify_thumbnail(
        "https://open.spotify.com/track/1gqkRc9WtOpnGIqxf2Hvzr?si=bd0351766c9b496f"
    )
