import numpy as np
from PIL import Image
from PyQt5 import QtWidgets


class SimpleImageEditor:
    def __init__(self, path):
        self.original = np.asarray(Image.open(path))
        self.actual = self.original.copy()
        self.app = QtWidgets.QApplication([])
        self.main_window = QtWidgets.QWidget()
        self.main_window.setWindowTitle('Simple Image Editor')
        self.main_window.show()

    def exec(self):
        self.app.exec()

    def save_image(self, file_name):
        Image.fromarray(np.uint8(self.actual)).save(file_name)

    def reset_image(self):
        self.actual = self.original.copy()

