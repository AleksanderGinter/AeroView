class ImageNavigator:
    def __init__(self, image_sets):
        self.image_sets = image_sets
        self.index = 0

        # limit based on shortest folder
        self.max_index = min(len(s) for s in image_sets) - 1

    def next(self):
        if self.index < self.max_index:
            self.index += 1

    def prev(self):
        if self.index > 0:
            self.index -= 1

    def current_items(self):
        return [
            image_set[self.index]
            for image_set in self.image_sets
        ]
