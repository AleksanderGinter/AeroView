class ImageNavigator:
    def __init__(self, image_sets):
        self.image_sets = image_sets  # dict: group -> list[ImageItem]

        self.reset()

    def reset(self):
        self.groups = list(self.image_sets.keys())
        self.current_group = self.groups[0] if self.groups else None
        self.index = 0
        self.update_limits()

    def update_limits(self):
        if not self.current_group:
            self.max_index = 0
            return

        self.max_index = len(self.image_sets[self.current_group]) - 1

    def set_group(self, group):
        if group in self.image_sets:
            self.current_group = group
            self.index = 0
            self.update_limits()

    def next(self):
        if self.index < self.max_index:
            self.index += 1

    def prev(self):
        if self.index > 0:
            self.index -= 1

    def current_items(self):
        """
        UI expects a list of items (future-proof),
        even though we currently show 1 image per index.
        """
        if not self.current_group:
            return []

        item = self.image_sets[self.current_group][self.index]
        return [item]
