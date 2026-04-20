from pathlib import Path
import re
from collections import defaultdict

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


PREFERRED_GROUPS = ["Z CpT", "Z"]


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
    Extract full folder name like 'Z CpT'
    """
    return path.parent.name


def load_images(root_folders):
    grouped = defaultdict(list)

    # ---------- BUILD DATASET ----------
    for root in root_folders:
        root_path = Path(root)

        for group_folder in root_path.iterdir():
            if not group_folder.is_dir():
                continue

            images = []

            for path in group_folder.rglob("*"):
                if path.suffix.lower() in SUPPORTED_EXTS:
                    group = group_folder.name
                    images.append(ImageItem(str(path), group))

            if images:
                images = sorted(images, key=lambda x: natural_key(x.path))
                grouped[group_folder.name].extend(images)

    grouped = dict(grouped)

    # ---------- APPLY PREFERRED GROUP LOGIC ----------
    grouped = apply_preferred_group(grouped)

    return grouped


# ---------- PREFERRED GROUP HANDLING ----------
def apply_preferred_group(grouped):
    """
    Ensures a stable default group (Z CpT preferred).
    Falls back gracefully if not found.
    """

    if not grouped:
        return grouped

    # 1. Try exact match priority list
    for preferred in PREFERRED_GROUPS:
        if preferred in grouped:
            grouped = _reorder_dict(grouped, preferred)
            return grouped

    # 2. Fallback: any group starting with 'Z'
    for key in grouped.keys():
        if key.startswith("Z"):
            grouped = _reorder_dict(grouped, key, override_name="Z CpT")
            return grouped

    # 3. No preference found → keep original
    return grouped


def _reorder_dict(d, first_key, override_name=None):
    """
    Moves preferred key to front of dict.
    Optionally renames it (used for fallback consistency).
    """
    new_dict = {}

    for k, v in d.items():
        if k == first_key:
            new_dict[override_name or k] = v
        else:
            new_dict[k] = v

    return new_dict
