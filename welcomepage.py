from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLineEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal, QSettings


class WelcomeScreen(QWidget):
    folder_selected = Signal(str)

    def __init__(self, background_path):
        super().__init__()

        # ---------- BACKGROUND ----------
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)

        pixmap = QPixmap(background_path)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(self.rect())

        # ---------- OVERLAY ----------
        self.overlay = QWidget(self)
        self.overlay.setAttribute(Qt.WA_TranslucentBackground)
        self.overlay.setGeometry(self.rect())

        # ---------- CONTINUE BUTTON ----------
        self.continue_button = QPushButton("Continue", self.overlay)
        self.continue_button.setFixedSize(200, 50)

        self.continue_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(40, 40, 40, 180);
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: rgba(60, 60, 60, 200);
            }
        """)

        self.continue_button.clicked.connect(self.start)

        # ---------- BASELINE ----------
        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setPlaceholderText("No folder selected")

        self.select_button = QPushButton("Select Folder")

        self.path_display.setStyleSheet("""
            QLineEdit {
                background-color: rgba(40, 40, 40, 160);
                color: white;
                padding: 6px;
                border-radius: 6px;
            }
        """)

        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(40, 40, 40, 180);
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: rgba(60, 60, 60, 220);
            }
        """)

        self.select_button.clicked.connect(self.select_folder)

        self.folder_layout = QHBoxLayout()
        self.folder_layout.addWidget(self.path_display)
        self.folder_layout.addWidget(self.select_button)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout()
        layout.addStretch(4)
        layout.addWidget(self.continue_button, alignment=Qt.AlignCenter)
        layout.addLayout(self.folder_layout)
        layout.addStretch(1)

        self.overlay.setLayout(layout)

        # ---------- SETTINGS ----------
        self.settings = QSettings("AeroView", "App")
        saved_path = self.settings.value("baseline_folder", "")

        if saved_path:
            self.path_display.setText(saved_path)

        self.continue_button.setEnabled(bool(saved_path))

    # ---------- RESIZE ----------
    def resizeEvent(self, event):
        self.background_label.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)

    # ---------- SELECT FOLDER ----------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Baseline Folder"
        )

        if folder:
            self.path_display.setText(folder)
            self.settings.setValue("baseline_folder", folder)
            self.continue_button.setEnabled(True)

    # ---------- START VIEWER ----------
    def start(self):
        folder = self.path_display.text().strip()

        if folder:
            self.folder_selected.emit(folder)
        else:
            print("No folder selected.")