from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QFileDialog,
    QInputDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


# =========================================================
# SINGLE CASE COLUMN
# =========================================================
class CaseFrame(QWidget):
    def __init__(self, case_name, is_base=False):
        super().__init__()

        self.case_name = case_name

        # ---------- TITLE ----------
        self.title = QLabel(case_name)
        self.title.setAlignment(Qt.AlignCenter)

        if is_base:
            self.title.setStyleSheet("""
                background-color: rgba(20, 20, 20, 220);
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 3px;
                border-radius: 4px;
            """)
        else:
            self.title.setStyleSheet("""
                background-color: rgba(20, 20, 20, 200);
                color: white;
                font-size: 11px;
                padding: 3px;
                border-radius: 4px;
            """)

        # ---------- IMAGE ----------
        self.label = QLabel("No image")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
            font-size: 13px;
        """)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(4, 4, 4, 4)

        layout.addWidget(self.title, 1)
        layout.addWidget(self.label, 8)

        self.setLayout(layout)

    def set_image(self, item):
        if item is None:
            self.label.setText("No image")
            self.label.setPixmap(QPixmap())
            return

        pixmap = QPixmap(item.path)

        if pixmap.isNull():
            self.label.setText("No image")
            self.label.setPixmap(QPixmap())
        else:
            self.label.setText("")
            self.label.setPixmap(
                pixmap.scaled(
                    self.label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )


# =========================================================
# MAIN VIEWER
# =========================================================
class ImageViewer(QWidget):
    def __init__(self, navigator, loader):
        super().__init__()

        self.navigator = navigator
        self.loader = loader

        # =====================================================
        # GLOBAL STYLE
        # =====================================================
        self.setStyleSheet("""
        QPushButton {
            background-color: rgba(40, 40, 40, 180);
            color: white;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 13px;
        }

        QPushButton:hover {
            background-color: rgba(70, 70, 70, 200);
        }

        QPushButton:pressed {
            background-color: rgba(90, 90, 90, 220);
        }
        """)

        # =====================================================
        # NAV BUTTONS
        # =====================================================
        self.prev_button = QPushButton("◀ Previous")
        self.next_button = QPushButton("Next ▶")
        self.fullscreen_button = QPushButton("Fullscreen (F)")
        self.add_case_button = QPushButton("Add Case (A)")
        self.remove_case_button = QPushButton("Remove Case (R)")

        self.prev_button.clicked.connect(self.show_prev)
        self.next_button.clicked.connect(self.show_next)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.add_case_button.clicked.connect(self.add_case)
        self.remove_case_button.clicked.connect(self.remove_case)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.fullscreen_button)
        nav_layout.addWidget(self.add_case_button)
        nav_layout.addWidget(self.remove_case_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)

        # =====================================================
        # CASE FRAMES
        # =====================================================
        self.case_frames = []
        self.case_layout = QHBoxLayout()

        self.build_case_frames()

        # =====================================================
        # GROUP BUTTONS
        # =====================================================
        self.group_buttons = {}
        self.group_layout = QHBoxLayout()

        self.rebuild_groups()
        self.group_layout.setAlignment(Qt.AlignCenter)

        group_bar = QWidget()
        group_bar.setLayout(self.group_layout)
        group_bar.setFixedHeight(40)
        group_bar.setStyleSheet("""
        background-color: rgba(25, 25, 25, 160);
        border-top: 1px solid rgba(255, 255, 255, 30);
        """)

        # =====================================================
        # MAIN LAYOUT
        # =====================================================
        main = QVBoxLayout()
        main.addLayout(self.case_layout, 1)
        main.addLayout(nav_layout, 0)
        main.addWidget(group_bar, 0)

        self.setLayout(main)

        self.update_image()

    # =========================================================
    # CASE FRAMES
    # =========================================================
    def build_case_frames(self):
        for frame in self.case_frames:
            self.case_layout.removeWidget(frame)
            frame.deleteLater()

        self.case_frames.clear()

        base_case = self.navigator.cases[0] if self.navigator.cases else None

        for case in self.navigator.cases:
            frame = CaseFrame(case, is_base=(case == base_case))

            frame.setMinimumWidth(250)
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.case_frames.append(frame)
            self.case_layout.addWidget(frame)

    # =========================================================
    # GROUP BUTTONS
    # =========================================================
    def rebuild_groups(self):
        for btn in self.group_buttons.values():
            self.group_layout.removeWidget(btn)
            btn.deleteLater()

        self.group_buttons.clear()

        for group in self.navigator.groups:
            btn = QPushButton(group)

            btn.setFixedHeight(28)
            btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 180);
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 12px;
            }

            QPushButton:hover {
                background-color: rgba(80, 80, 80, 200);
            }

            QPushButton:pressed {
                background-color: rgba(110, 110, 110, 220);
            }
            """)

            btn.clicked.connect(lambda _, g=group: self.switch_group(g))

            self.group_buttons[group] = btn
            self.group_layout.addWidget(btn)

    def switch_group(self, group):
        self.navigator.set_group(group)
        self.update_image()
        self.setFocus()

    # =========================================================
    # ADD CASE
    # =========================================================
    def add_case(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Case Folder")

        if not folder:
            return

        new_data = self.loader(folder)

        if not new_data:
            return

        for case, group_map in new_data.items():
            if case not in self.navigator.dataset:
                self.navigator.dataset[case] = group_map
            else:
                for group, images in group_map.items():
                    self.navigator.dataset[case].setdefault(group, [])
                    self.navigator.dataset[case][group].extend(images)

        self.navigator.reset()

        self.build_case_frames()
        self.rebuild_groups()
        self.update_image()
        self.setFocus()

    # =========================================================
    # REMOVE CASE
    # =========================================================
    def remove_case(self):
        cases = self.navigator.cases

        if len(cases) <= 1:
            return

        base_case = self.navigator.base_case

        removable_cases = [c for c in cases if c != base_case]

        case, ok = QInputDialog.getItem(
            self,
            "Remove Case",
            "Select case to remove:",
            removable_cases,
            0,
            False
        )

        if not ok or not case:
            return

        if case in self.navigator.dataset:
            del self.navigator.dataset[case]

        self.navigator.reset()

        self.build_case_frames()
        self.rebuild_groups()
        self.update_image()
        self.setFocus()

    # =========================================================
    # UPDATE IMAGE
    # =========================================================
    def update_image(self):
        items = self.navigator.current_items()

        for frame, item in zip(self.case_frames, items):
            frame.set_image(item)

    # =========================================================
    # NAVIGATION
    # =========================================================
    def show_next(self):
        self.navigator.next()
        self.update_image()
        self.setFocus()

    def show_prev(self):
        self.navigator.prev()
        self.update_image()
        self.setFocus()

    # =========================================================
    # FULLSCREEN
    # =========================================================
    def toggle_fullscreen(self):
        window = self.window()

        if window.isFullScreen():
            window.showNormal()
        else:
            window.showFullScreen()

        self.update_image()
        self.setFocus()

    # =========================================================
    # KEY HANDLING
    # =========================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.show_next()

        elif event.key() == Qt.Key_Left:
            self.show_prev()

        elif event.key() == Qt.Key_F:
            self.toggle_fullscreen()

        elif event.key() == Qt.Key_A:
            self.add_case()

        elif event.key() == Qt.Key_R:
            self.remove_case()