import typer
from pathlib import Path
from rich.pretty import pprint
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
from typing_extensions import Annotated
from datetime import datetime

app = typer.Typer()


def validate_image(ctx: typer.Context, file_path: Path):
    if ctx.resilient_parsing:
        return
    print("Validating image")

    try:
        with Image.open(file_path) as img:
            img.verify()
    except:
        raise typer.BadParameter(f"{file_path} is not a valid image file")
    return file_path


def validate_metadata():
    pass


@app.command()
def addTextChunk(
    image_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            callback=validate_image,
        ),
    ],
    metadata_file: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
):
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    metadata_str = json.dumps(metadata)
    png_info = PngInfo()

    png_info.add_text("metadata", metadata_str)
    output_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".png"
    with Image.open(image_path) as img:
        existing_metadata = img.info.get("metadata")
        if existing_metadata:
            print("Existing metadata found. Overwriting...")
            print("<---Existing metadata--->\n")
            print(existing_metadata)
            print("\n<-x-x--Existing metadata--x-x->\n")
        print("<---New metadata--->\n")
        print(metadata_str)
        print("\n<-x-x--New metadata--x-x->\n")
        print(f"Saving file as {output_name}")
        img.save(output_name, "PNG", pnginfo=png_info)


@app.command()
def readTextChunk(
    image_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            callback=validate_image,
        ),
    ]
):
    with Image.open(image_path) as img:
        metadata = json.loads(img.info["metadata"])
        pprint(metadata)
        matrices = metadata.get("transformation_matrices")
        if matrices is not None:
            for matrix in matrices:
                a, b, c, d, e, f, g, h, i = matrix
                pprint(matrix)


if __name__ == "__main__":
    app()
