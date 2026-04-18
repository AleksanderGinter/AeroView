class ImageItem:
    def __init__(self, path, group):
        self.path = path
        self.group = group

    def __repr__(self):
        return f"ImageItem(group={self.group}, path={self.path})"
