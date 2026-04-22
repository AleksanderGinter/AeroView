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


# =========================================================
# CASE LOADER (SINGLE CASE ROOT)
# =========================================================
def load_images(case_folder: str):
    """
    B027/
        Z CpT/
        Y CpT/
    """

    root = Path(case_folder)

    if not root.exists():
        print("Invalid path:", root)
        return {}

    case_name = root.name

    dataset = defaultdict(lambda: defaultdict(list))

    # -----------------------------------------------------
    # GROUP LEVEL ONLY
    # -----------------------------------------------------
    for group_folder in root.iterdir():

        if not group_folder.is_dir():
            continue

        group_name = group_folder.name
        images = []

        for img in group_folder.rglob("*"):
            if img.suffix.lower() in SUPPORTED_EXTS:
                images.append(ImageItem(str(img), group_name))

        if images:
            images.sort(key=lambda x: natural_key(x.path))
            dataset[case_name][group_name].extend(images)

    return dict(dataset)
