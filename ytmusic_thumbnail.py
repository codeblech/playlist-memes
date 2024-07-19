from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
from PIL.Image import Resampling
from io import BytesIO
import regex


def get_ytmusic_thumbnail(url: str) -> str | None:
    """Get the thumbnail of a song, playlist, or album using its youtube music url

    Args:
        link (str): YouTube Music url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Failed to fetch {url}")
        print(f"Status code: {r.status_code}")
        return None

    soup = BeautifulSoup(r.content, "lxml")
    title_tags = soup.find_all("title")  # ytmusic returns two title tags in html

    if "Your browser is deprecated" in str(title_tags[0]):
        meta = soup.find("meta", {"property": "og:image"})
        thumbnail_url = meta.get("content", None)

    if thumbnail_url is not None:
        rr = requests.get(thumbnail_url)
        if rr.status_code != 200:
            print(f"Failed to fetch thumbnail from {thumbnail_url}")
            print(f"Status code: {r.status_code}")
            return None

        save_name = regex.findall(r".*=(.*)", url)[0]  # extract last part of url
        save_path = os.path.join("./assets/overlay/ytmusic", f"{save_name}.jpg")
        os.makedirs("./assets/overlay/ytmusic", exist_ok=True)

        with Image.open(BytesIO(rr.content)) as im:
            try:
                im = im.resize((512,512), Resampling.LANCZOS)
                print("resized thumbnail image")
                im.save(save_path, format="JPEG")
                print(f"Saved thumbnail to {save_path}")
                return save_path
            except:
                print("Failed to save image")
                return None
