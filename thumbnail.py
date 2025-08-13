from urllib.parse import urlparse
import logging
from ytmusic_thumbnail import get_ytmusic_thumbnail
from ytmusic_thumbnail_v2 import get_ytmusic_thumbnail as get_ytmusic_thumbnail_v2
from youtube_thumbnail import get_yt_thumbnail
from spotify_thumbnail import get_spotify_thumbnail


logger = logging.getLogger(__name__)

def detect_platform(url):
    """
    Detect the music platform from a URL.

    Args:
        url (str): The URL to analyze

    Returns:
        str: One of 'ytmusic', 'spotify', 'youtube', or 'unknown'
    """
    parsed = urlparse(url.lower())
    domain = parsed.netloc.replace("www.", "").replace("m.", "")

    if "music.youtube.com" in domain:
        return "ytmusic"
    elif "open.spotify.com" in domain:
        return "spotify"
    elif "youtube.com" in domain or "youtu.be" in domain:
        return "youtube"
    else:
        return "unknown"


def get_thumbnail(url):
    """
    Get thumbnail based on the detected platform.

    Args:
        url (str): The URL to get thumbnail for

    Returns:
        str or None: Path to the downloaded thumbnail, or None if failed
    """
    platform = detect_platform(url)
    logger.info(f"Getting thumbnail for URL: {url}, detected platform: {platform}")

    if platform == "ytmusic":
        logger.info("Calling get_ytmusic_thumbnail")
        result = get_ytmusic_thumbnail(url)
        if result:
            logger.info(f"YT Music thumbnail downloaded successfully: {result}")
        else:
            logger.error(f"YT Music thumbnail download failed for URL: {url} \nTrying v2 method")
            result = get_ytmusic_thumbnail_v2(url)
            if result:
                logger.info(f"YT Music v2 thumbnail downloaded successfully: {result}")
            else:
                logger.error(f"YT Music v2 thumbnail download failed for URL: {url}")
        return result
    elif platform == "spotify":
        logger.info("Calling get_spotify_thumbnail")
        result = get_spotify_thumbnail(url)
        if result:
            logger.info(f"Spotify thumbnail downloaded successfully: {result}")
        else:
            logger.error(f"Spotify thumbnail download failed for URL: {url}")
        return result
    elif platform == "youtube":
        logger.info("Calling get_yt_thumbnail")
        result = get_yt_thumbnail(url)
        if result:
            logger.info(f"YouTube thumbnail downloaded successfully: {result}")
        else:
            logger.error(f"YouTube thumbnail download failed for URL: {url}")
        return result
    else:
        logger.error(f"Unknown platform for URL: {url}")
        return None
