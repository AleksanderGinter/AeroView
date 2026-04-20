from pathlib import Path
import re
from collections import defaultdict

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def natural_key(path):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', str(path))
    ]


class ImageItem:
    def __init__(self, path, group):
        self.path = path
        self.group = group


def extract_group(path: Path):
    """
    Extract X/Y/Z from folder like 'Z CpT'
    """
    return path.parent.name


def load_images(folders):
    """
    Returns:
    {
        "X": [ImageItem, ImageItem, ...],
        "Y": [...]
    }
    """

    grouped = defaultdict(list)

    for folder in folders:
        for path in Path(folder).rglob("*"):
            if path.suffix.lower() in SUPPORTED_EXTS:
                group = extract_group(path)
                grouped[group].append(ImageItem(str(path), group))

    # sort each group naturally
    for group in grouped:
        grouped[group] = sorted(
            grouped[group],
            key=lambda x: natural_key(x.path)
        )

    return dict(grouped)

