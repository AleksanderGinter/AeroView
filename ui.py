from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self, navigator):
        super().__init__()

        self.navigator = navigator

        # ---------- GROUP BUTTONS ----------
        self.group_buttons = {}
        self.group_layout = QHBoxLayout()

        for group in self.navigator.image_sets.keys():
            btn = QPushButton(group)
            btn.clicked.connect(lambda _, g=group: self.switch_group(g))
            self.group_buttons[group] = btn
            self.group_layout.addWidget(btn)

        # Center group buttons (optional but cleaner)
        self.group_layout.setAlignment(Qt.AlignCenter)
        self.group_layout.setSpacing(10)

        # ---------- IMAGE LABELS ----------
        self.image_labels = []
        self.image_layout = QHBoxLayout()

        num_views = 1  # single image per index for now

        for _ in range(num_views):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: black;")

            label.setSizePolicy(
                QSizePolicy.Ignored,
                QSizePolicy.Ignored
            )

            self.image_labels.append(label)
            self.image_layout.addWidget(label)

        # ---------- NAVIGATION BUTTONS ----------
        self.prev_button = QPushButton("◀ Previous")
        self.next_button = QPushButton("Next ▶")
        self.fullscreen_button = QPushButton("Fullscreen (F)")

        self.prev_button.clicked.connect(self.show_prev)
        self.next_button.clicked.connect(self.show_next)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # ---------- BUTTON ROW ----------
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch()
        button_layout.addWidget(self.fullscreen_button)
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)

        # ---------- MAIN LAYOUT ----------
        main_layout = QVBoxLayout()

        main_layout.addLayout(self.image_layout, 1)
        main_layout.addLayout(button_layout, 0)
        main_layout.addLayout(self.group_layout, 0)

        self.setLayout(main_layout)

        # ---------- WINDOW ----------
        self.setWindowTitle("AeroView")
        self.resize(1200, 800)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        # ensure proper initial state
        self.navigator.reset()
        self.update_image()

        self.show()

    # ---------- GROUP SWITCH ----------
    def switch_group(self, group):
        self.navigator.set_group(group)
        self.update_image()
        self.setFocus()

    # ---------- IMAGE UPDATE ----------
    def update_image(self):
        items = self.navigator.current_items()

        self.pixmaps = []

        if not items:
            print("No items to display")
            return

        for item in items:
            pixmap = QPixmap(item.path)

            if pixmap.isNull():
                print(f"Failed to load: {item.path}")
                self.pixmaps.append(QPixmap())
            else:
                self.pixmaps.append(pixmap)

        self.render_images()

    # ---------- RENDER ----------
    def render_images(self):
        if not hasattr(self, "pixmaps"):
            return

        for label, pixmap in zip(self.image_labels, self.pixmaps):
            if pixmap.isNull():
                label.clear()
                continue

            scaled = pixmap.scaled(
                label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            label.setPixmap(scaled)

    # ---------- NAVIGATION ----------
    def show_next(self):
        self.navigator.next()
        self.update_image()
        self.setFocus()

    def show_prev(self):
        self.navigator.prev()
        self.update_image()
        self.setFocus()

    # ---------- FULLSCREEN ----------
    def toggle_fullscreen(self):
        window = self.window()

        if window.isFullScreen():
            window.showNormal()
        else:
            window.showFullScreen()

        self.setFocus()
        self.render_images()

    # ---------- KEY HANDLING ----------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.show_next()

        elif event.key() == Qt.Key_Left:
            self.show_prev()

        elif event.key() == Qt.Key_F:
            self.toggle_fullscreen()

        elif event.key() == Qt.Key_Escape:
            window = self.window()

            if window.isFullScreen():
                window.showNormal()
            else:
                window.close()

    # ---------- RESIZE ----------
    def resizeEvent(self, event):
        self.render_images()
        super().resizeEvent(event)
