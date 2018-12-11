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

    def rotate_cw(self):
        ...

    def rotate_ccw(self):
        ...

    def mirror(self):
        ...

    def invert_colors(self):
        ...

    def greyscale(self):
        for y in range(self.actual.shape[1]):
            for x in range(self.actual.shape[0]):
                gray_component = 0.299 * self.actual[x][y][0] + 0.587 * self.actual[x][y][1] + 0.114 * self.actual[x][y][2]
                self.actual[x, y, 0] = gray_component
                self.actual[x, y, 1] = gray_component
                self.actual[x, y, 2] = gray_component

    def lighten(self):
        ...

    def darken(self):
        ...

    def enhance_edges(self):
        ...
