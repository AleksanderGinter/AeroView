import sys
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from loader import load_images
from navigator import ImageNavigator
from ui import ImageViewer


def select_folders():
    folders = []

    while True:
        folder = QFileDialog.getExistingDirectory(
            None,
            "Select Image Folder"
        )

        if not folder:
            break

        folders.append(folder)

        reply = QMessageBox.question(
            None,
            "Add Another Folder?",
            "Do you want to add another folder?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            break

    return folders


def main():
    app = QApplication(sys.argv)

    folders = select_folders()

    if not folders:
        print("No folders selected. Exiting.")
        sys.exit()

    # NOW RETURNS ImageItem objects (important change)
    images = load_images(folders)

    if not images:
        print("No images found in selected folders.")
        sys.exit()

    # Navigator now works with ImageItem objects
    navigator = ImageNavigator(images)

    viewer = ImageViewer(navigator)
    viewer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
