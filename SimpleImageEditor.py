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

    def save_each(self):
        # rotate cw
        self.reset_image()
        self.rotate_cw()
        self.save_image("rotated_cw.jpg")

        # rotate ccw
        self.reset_image()
        self.rotate_ccw()
        self.save_image("rotated_ccw.jpg")

        # mirror
        self.reset_image()
        self.mirror()
        self.save_image("mirrored.jpg")

        # invert colors
        self.reset_image()
        self.invert_colors()
        self.save_image("inverted_colors.jpg")

        # greyscale
        self.reset_image()
        self.greyscale()
        self.save_image("greyscaled.jpg")

        # lighten
        self.reset_image()
        self.lighten()
        self.save_image("lightened.jpg")

        # darken
        self.reset_image()
        self.darken()
        self.save_image("darkened.jpg")

        # enhance edges
        self.reset_image()
        self.enhance_edges()
        self.save_image("enhanced_edges.jpg")
