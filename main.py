import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from loader import load_images
from navigator import ImageNavigator
from ui import ImageViewer
from welcomepage import WelcomeScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AeroView")

        # ---------- STACK ----------
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # ---------- WELCOME SCREEN ----------
        self.welcome = WelcomeScreen(background_path="AeroViewLogo.png")
        self.welcome.folder_selected.connect(self.start_viewer)

        self.stack.addWidget(self.welcome)
        self.stack.setCurrentWidget(self.welcome)

        self.resize(800, 800)

    # ---------- TRANSITION ----------
    def start_viewer(self, folder):
        images = load_images([folder])

        if not images:
            print("No images found.")
            return

        navigator = ImageNavigator(images)
        self.viewer = ImageViewer(navigator)

        self.stack.addWidget(self.viewer)
        self.stack.setCurrentWidget(self.viewer)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
