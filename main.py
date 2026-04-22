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
        self.welcome = WelcomeScreen("AeroViewLogo.png")
        self.welcome.folder_selected.connect(self.start)

        self.stack.addWidget(self.welcome)
        self.stack.setCurrentWidget(self.welcome)

    # ---------- START APP ----------
    def start(self, case_folder):
        """
        case_folder = e.g. B027/
        """

        dataset = load_images(case_folder)

        if not dataset:
            print("No data found in:", case_folder)
            return

        # ---------- NAVIGATOR ----------
        navigator = ImageNavigator(dataset)

        # ---------- UI ----------
        viewer = ImageViewer(navigator, load_images)

        self.stack.addWidget(viewer)
        self.stack.setCurrentWidget(viewer)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
