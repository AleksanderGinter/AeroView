class ImageNavigator:
    def __init__(self, dataset):
        self.dataset = dataset

        self._ready = False

        self.reset()

    # =====================================================
    # RESET ENTRY POINT
    # =====================================================
    def reset(self):
        """
        Public reset entry point.
        Always rebuilds navigator into a consistent state.
        """
        self._recompute_state()
        self._ready = True

    # =====================================================
    # CORE RECOMPUTE PIPELINE
    # =====================================================
    def _recompute_state(self):
        """
        Single source of truth for rebuilding internal state.
        Prevents partial updates and sync bugs.
        """

        # -----------------------------
        # CASES
        # -----------------------------
        self.cases = list(self.dataset.keys())
        self.base_case = self.cases[0] if self.cases else None

        # -----------------------------
        # GROUPS
        # -----------------------------
        self.groups = self._collect_groups()

        if not self.groups:
            self.current_group = None
            self.max_index = 0
            self.index = 0
            return

        # Keep current group if valid, otherwise fallback
        if not hasattr(self, "current_group") or self.current_group not in self.groups:
            self.current_group = (
                "Z CpT" if "Z CpT" in self.groups else self.groups[0]
            )

        # -----------------------------
        # LIMITS
        # -----------------------------
        self.max_index = self._compute_max_index()

        # -----------------------------
        # INDEX SAFETY
        # -----------------------------
        self.index = getattr(self, "index", 0)
        self._clamp_index()

    # =====================================================
    # GROUP COLLECTION
    # =====================================================
    def _collect_groups(self):
        groups = set()

        for case_data in self.dataset.values():
            groups.update(case_data.keys())

        return sorted(groups)

    # =====================================================
    # MAX INDEX COMPUTATION
    # =====================================================
    def _compute_max_index(self):
        if not self.current_group:
            return 0

        max_len = 0

        for case in self.cases:
            case_data = self.dataset.get(case, {})
            group_images = case_data.get(self.current_group, [])

            max_len = max(max_len, len(group_images))

        return max_len - 1 if max_len > 0 else 0

    # =====================================================
    # BASE LENGTH (SLIDER REFERENCE)
    # =====================================================
    def get_base_length(self):
        if not self.base_case or not self.current_group:
            return 0

        case_data = self.dataset.get(self.base_case, {})
        group_images = case_data.get(self.current_group, [])

        return len(group_images)

    # =====================================================
    # INDEX CLAMPING (SINGLE SOURCE OF TRUTH)
    # =====================================================
    def _clamp_index(self):
        if not self._ready:
            self.index = 0
            return

        self.index = max(0, min(self.index, self.max_index))

    # =====================================================
    # SLIDER MAPPING
    # =====================================================
    def set_index_from_ratio(self, ratio):
        if not self._ready:
            return

        base_length = self.get_base_length()

        if base_length <= 1:
            self.index = 0
            return

        ratio = max(0.0, min(1.0, ratio))

        self.index = round(ratio * (base_length - 1))

        self._clamp_index()

    def get_ratio(self):
        base_length = self.get_base_length()

        if base_length <= 1:
            return 0.0

        return self.index / (base_length - 1)

    # =====================================================
    # GROUP SWITCH
    # =====================================================
    def set_group(self, group):
        if group not in self.groups:
            return

        self.current_group = group
        self.index = 0

        self.max_index = self._compute_max_index()
        self._clamp_index()

    # =====================================================
    # NAVIGATION
    # =====================================================
    def next(self):
        if not self._ready:
            return

        self.index += 1
        self._clamp_index()

    def prev(self):
        if not self._ready:
            return

        self.index -= 1
        self._clamp_index()

    # =====================================================
    # CURRENT FRAME EXTRACTION
    # =====================================================
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
