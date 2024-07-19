import streamlit as st
import os
from maker import apply_overlay_transformation, apply_overlay_transformation_v2
from ytmusic_thumbnail import get_ytmusic_thumbnail

st.set_page_config(page_title="Music Memes", page_icon=":headphones:", layout="wide")
st.title("Music Memes")

n = st.slider("Number of cover arts", min_value=1, max_value=5, value=1, step=1)

urls = []
for i in range(n):
    if url := st.text_input(label=f"YTMusic URL of song/playlist {i+1}"):
        urls.append(url)


if st.button(label="Generate Memes", disabled=len(urls) != n, type="primary"):
    overlay_paths = [path for url in urls if (path := get_ytmusic_thumbnail(url)) is not None]
    print(overlay_paths)
    backgrounds_directory = os.path.join("assets", "background", str(n))
    print(backgrounds_directory)
    for filename in os.listdir(backgrounds_directory):
        # print(filename)
        if os.path.isfile(os.path.join(backgrounds_directory, filename)):
            print(filename)
            background_path = os.path.join(backgrounds_directory, filename)
            print(f"using background image: {background_path}")
            output_image = None
            if n == 1:
                if img_path := apply_overlay_transformation(background_path, overlay_paths[0]):
                    print(img_path)
                    output_image = img_path

            elif img_path := apply_overlay_transformation_v2(background_path, overlay_paths):
                print(img_path)
                output_image = img_path

            if output_image:
                st.image(img_path, width=512, use_column_width="auto")
