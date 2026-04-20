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
        self._normal_geometry = None

        # ---------- TITLE ----------
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            padding: 6px;
            background-color: rgba(0, 0, 0, 120);
        """)

        # ---------- IMAGE LABELS (DYNAMIC) ----------
        self.image_labels = []
        self.image_layout = QHBoxLayout()

        num_views = len(self.navigator.image_sets)

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

        # ---------- BUTTONS ----------
        self.prev_button = QPushButton("◀ Previous")
        self.next_button = QPushButton("Next ▶")
        self.fullscreen_button = QPushButton("Fullscreen (F)")

        self.prev_button.clicked.connect(self.show_prev)
        self.next_button.clicked.connect(self.show_next)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # ---------- BUTTON LAYOUT ----------
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch()  # pushes fullscreen to center
        button_layout.addWidget(self.fullscreen_button)
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)

        # ---------- MAIN LAYOUT ----------
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)

        main_layout.addLayout(self.image_layout)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # ---------- WINDOW ----------
        self.setWindowTitle("Photo Flicker")
        self.resize(1000, 700)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.update_image()
        self.show()

    # ---------- IMAGE UPDATE ----------
    def update_image(self):
        items = self.navigator.current_items()

        self.pixmaps = []
        labels = []

        for item in items:
            pixmap = QPixmap(item.path)

            if pixmap.isNull():
                print(f"Failed to load: {item.path}")
                # add empty placeholder to keep alignment
                self.pixmaps.append(QPixmap())
                labels.append("Invalid")
            else:
                self.pixmaps.append(pixmap)
                labels.append(item.group)

        # Show all group names
        self.title_label.setText(" | ".join(labels))
        self.title_label.hide()

        self.render_images()

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
        if self.isFullScreen():
            self.showNormal()
            if self._normal_geometry:
                self.setGeometry(self._normal_geometry)
        else:
            self._normal_geometry = self.geometry()
            self.showFullScreen()

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
            if self.isFullScreen():
                self.showNormal()
            else:
                self.close()

    # ---------- RESIZE ----------
    def resizeEvent(self, event):
        self.render_images()
        super().resizeEvent(event)