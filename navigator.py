class ImageNavigator:
    def __init__(self, images):
        self.images = images
        self.index = 0

    def current(self):
        return self.images[self.index]

    def next(self):
        self.index = min(self.index + 1, len(self.images) - 1)

    def prev(self):
        self.index = max(self.index - 1, 0)
