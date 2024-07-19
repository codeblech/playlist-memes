# WTF is this?

This is a meme generator. Paste the links of your favourite songs and generate loads of memes with one click.
<img src="https://github.com/user-attachments/assets/90606cb4-a996-4c8c-86fb-82ad2edd490d" width="777">
# Hosted at

https://batman.streamlit.app/



# How to add more templates?
> [!TIP]
> Video tutorials are present in `tutorial/`

> [!NOTE]
> You should have GIMP installed
> If you're using some other image as a template, it must be 512x512 pixels, because that's the size of YTMusic Thumbnails. If your overlay in differently sized, change it's size first, then proceed further.

### one overlay without mask

- Open your template(background) image and [this](https://github.com/codeblech/playlist-memes/blob/main/meta.json) sample overlay image in GIMP
- Drag and drop the overlay layer onto the template image
- Make sure the paste offset is (0,0), i.e. upper left corner of the overlay layer overlaps the upper left corner
  of the background image.
- Use the Unified Transform Tool (Shift+T) to scale, rotate, shear, translate the overlay.
- When you're done, copy the Transform Matrix.
- Paste the matrix into the sample metadata json file, and change it according to your own metadata
- Add/Change the key `has_mask` to `false` in metadata json file
- use the script `pcp.py` to add a text chunk with the metadata to the template(background) image
  `python pcp.py addtextchunk <template-path> <metadata-json-file-path>`
  Use `python pcp.py --help` for help
- Clone this repository
- Add the png image generated by the script (the one that contains the text chunks) to the folder `assets/background/1/`
- Commit and open a Pull Request.
- As soon as the PR is accepted, Streamlit hosted website will update automatically.

> [!NOTE]
> Perspective transformations might cause problems of misalignment. Affine Transformations work fine. In simple words, scale, rotate, shear, translate work fine, but 3D transformations may not.

### more than one overlay without mask

- Open your template(background) image and [this](https://github.com/codeblech/playlist-memes/blob/main/meta.json) sample overlay image in GIMP
- Drag and drop the overlay layer onto the template image
- Make sure the paste offset is (0,0), i.e. upper left corner of the overlay layer overlaps the upper left corner
  of the background image.
- Use the Unified Transform Tool (Shift+T) to scale, rotate, shear, translate the overlay.
- When you're done, copy the Transform Matrix.
- Paste the matrix into the sample metadata json file
- Now, reset the transformation matrix.
- Apply the transformations for the second overlay, and save the transformation matrix to the metadata json file.
- Repeat this for as many overlays as you want.
- Add/Change the key `has_mask` to `false` in metadata json file
- use the script `pcp.py` to add a text chunk with the metadata to the template(background) image
  `python pcp.py addtextchunk <template-path> <metadata-json-file-path>`
  Use `python pcp.py --help` for help
- Clone this repository
- Add the png image generated by the script (the one that contains the text chunks) to the folder `assets/background/<N>/`, where `<N>` is 2,3,4,5... according to the number of overlays. If the folder is not present, create it. Please save the file in the correct folder.
- Commit and open a Pull Request.
- As soon as the PR is accepted, Streamlit hosted website will update automatically.

### one overlay with mask

- Open your template(background) image and [this](https://github.com/codeblech/playlist-memes/blob/main/meta.json) sample overlay image in GIMP
- Drag and drop the overlay layer onto the template image
- Make sure the paste offset is (0,0), i.e. upper left corner of the overlay layer overlaps the upper left corner
  of the background image.
- Use the Unified Transform Tool (Shift+T) to scale, rotate, shear, translate the overlay.
- When you're done, copy the Transform Matrix.
- Paste the matrix into the sample metadata json file, and change it according to your own metadata
- Add/Change the key `has_mask` to `false` in metadata json file
- Now for the mask, Add a mask layer to the overlay image by right clicking on the overlay image layer > click `Add Layer Mask...` > click `Add`
- Paint the mask using brush tool. Use Black and White brushes. Use white where the overlay must be visible. Use black it must not be visible. Make sure the mask is selected while you paint, and not the image.
- From `Layers` > Right click on the mask
- click `Mask to Selection`
- copy the mask using `CTRL+C` or `Edit > Copy`
- `File > New`. Change resolution to 512x512
- Click on `Advanced Options`
- Select `Color Space` as `Grayscale`, and `Fill with` as `Background color`.
- Paste the copied mask using `CTRL+C` or `Edit > Paste`
- In Layers, right click on `Floating Selection (Pasted Layer)`
- Click on `To New Layer`
- Adjust the mask using Unified Transform (Shift+T) to fit the background.
- Make sure the background is black. If it is not, paint it black using `Bucket Fill tool`.
- Click on `File > Export As`
- Name the mask the same as the name of the template, with a suffix `__mask.png`
  Example: the template is named `beach.png`, name the mask as `beach__mask.png`
- Select the Color Space as `8bpc GRAY` or `8bpc GRAYA`
- Click Export

# Info

- overlay images larger in resolution than background images don't work properly

### Mask

- if an background image has a text chunk `has_mask: false`, then it has no mask.
- if an background image has no text chunk with key `has_mask`, then it has no mask.
- if a background image has a text chunk `has_mask: true`, then it has a corresponding mask in the `mask` folder
- masks are saved with filenames ending in `__mask.png`
- multiple overlays with masks are not supported yet.

### Future

- add GitHubs Actions check to check if a new template added is saved to the correct folder.
- add metadata to more images from `assets/background/no-metadata`
- `overlay_count` might be incorrect in some images. Though it is not used right now for anything
- Add caching
- Improve speed
- Improve layout
- Add YouTube, Spotify support
- Handle playlist URLs
