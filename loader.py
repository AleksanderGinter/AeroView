from pathlib import Path
import re
from models import ImageItem

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def natural_key(path):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', str(path))
    ]


def get_group_name(path: Path):
    return path.parents[1].name if len(path.parents) > 1 else "Unknown"


def load_images(folders):
    images = []

    for folder in folders:
        for path in Path(folder).rglob("*"):
            if path.suffix.lower() in SUPPORTED_EXTS:
                images.append(
                    ImageItem(
                        path=str(path),
                        group=get_group_name(path)
                    )
                )

    return sorted(images, key=lambda x: natural_key(x.path))
