class ImageNavigator:
    def __init__(self, image_sets):
        self.image_sets = image_sets
        self.reset()

    def reset(self):
        self.groups = list(self.image_sets.keys())
        self.current_group = self.groups[0] if self.groups else None
        self.index = 0

    def set_group(self, group):
        if group in self.image_sets:
            self.current_group = group
            self.index = 0

    def next(self):
        if self.current_group:
            self.index = min(self.index + 1, self.max_index())

    def prev(self):
        if self.current_group:
            self.index = max(self.index - 1, 0)

    def max_index(self):
        return len(self.image_sets[self.current_group]) - 1

    def current_items(self):
        if not self.current_group:
            return []

        item = self.image_sets[self.current_group][self.index]
        return [item]
