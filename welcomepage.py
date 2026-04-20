from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal


class WelcomeScreen(QWidget):
    folder_selected = Signal(str)

    def __init__(self, background_path):
        super().__init__()

        # ---------- BACKGROUND ----------
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)

        pixmap = QPixmap(background_path)
        self.background_label.setPixmap(pixmap)

        # ---------- OVERLAY ----------
        self.overlay = QWidget(self)
        self.overlay.setAttribute(Qt.WA_TranslucentBackground)

        # ---------- CONTINUE BUTTON ----------
        self.continue_button = QPushButton("Continue", self.overlay)
        self.continue_button.setFixedSize(200, 50)

        self.continue_button.setStyleSheet("""
            QPushButton {
        background-color: rgba(0, 0, 0, 180);
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: rgba(60, 60, 60, 200);
            }
        """)

        self.continue_button.clicked.connect(self.select_folder)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout(self.overlay)
        layout.addStretch(1)
        layout.addWidget(self.continue_button, alignment=Qt.AlignCenter)
        layout.addStretch(4)

        self.setLayout(layout)

    # ---------- RESIZE ----------
    def resizeEvent(self, event):
        self.background_label.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)

    # ---------- ACTION ----------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder"
        )

        if folder:
            self.folder_selected.emit(folder)