class ImageNavigator:
    def __init__(self, dataset):
        self.dataset = dataset
        self.reset()

    # -----------------------------------------------------
    # RESET
    # -----------------------------------------------------
    def reset(self):
        self.cases = list(self.dataset.keys())

        self.base_case = self.cases[0] if self.cases else None

        self.groups = self._collect_groups()

        self.current_group = (
            "Z CpT"
            if "Z CpT" in self.groups
            else (self.groups[0] if self.groups else None)
        )

        self.index = 0
        self._update_limits()

    # -----------------------------------------------------
    # GROUPS
    # -----------------------------------------------------
    def _collect_groups(self):
        groups = set()

        for case_data in self.dataset.values():
            groups.update(case_data.keys())

        return sorted(groups)

    # -----------------------------------------------------
    # LIMITS
    # -----------------------------------------------------
    def _update_limits(self):
        if not self.current_group:
            self.max_index = 0
            return

        max_len = 0

        for case in self.cases:
            case_data = self.dataset.get(case, {})
            group_images = case_data.get(self.current_group, [])

            max_len = max(max_len, len(group_images))

        self.max_index = max_len - 1 if max_len > 0 else 0

        # Clamp current index if needed
        self.index = min(self.index, self.max_index)

    # -----------------------------------------------------
    # BASE CASE LENGTH
    # -----------------------------------------------------
    def get_base_length(self):
        if not self.base_case or not self.current_group:
            return 0

        case_data = self.dataset.get(self.base_case, {})
        group_images = case_data.get(self.current_group, [])

        return len(group_images)

    # -----------------------------------------------------
    # SLIDER RATIO
    # -----------------------------------------------------
    def set_index_from_ratio(self, ratio):
        base_length = self.get_base_length()

        if base_length <= 1:
            self.index = 0
            return

        ratio = max(0.0, min(1.0, ratio))

        self.index = round(ratio * (base_length - 1))

        self.index = min(self.index, self.max_index)

    def get_ratio(self):
        base_length = self.get_base_length()

        if base_length <= 1:
            return 0.0

        return self.index / (base_length - 1)

    # -----------------------------------------------------
    # GROUP SWITCH
    # -----------------------------------------------------
    def set_group(self, group):
        if group in self.groups:
            self.current_group = group
            self.index = 0
            self._update_limits()

    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------
    def next(self):
        self.index = min(self.index + 1, self.max_index)

    def prev(self):
        self.index = max(self.index - 1, 0)

    # -----------------------------------------------------
    # CURRENT FRAME ACROSS CASES
    # -----------------------------------------------------
    def current_items(self):
        items = []

        for case in self.cases:
            case_data = self.dataset.get(case, {})
            group_images = case_data.get(self.current_group, [])

            if self.index < len(group_images):
                items.append(group_images[self.index])
            else:
                items.append(None)

        return items
