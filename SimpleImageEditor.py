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
        self.actual = np.rot90(self.actual, -1)

    def rotate_ccw(self):
        self.actual = np.rot90(self.actual)

    def mirror_x(self):
        self.actual = self.actual[::-1]

    def mirror_y(self):
        self.actual = self.actual[::, ::-1]

    def invert_colors(self):
        self.actual = 255 - self.actual

    def greyscale(self):
        for y in range(self.actual.shape[1]):
            for x in range(self.actual.shape[0]):
                grey_component = 0.299 * self.actual[x][y][0] + 0.587 * self.actual[x][y][1] + 0.114 * \
                                 self.actual[x][y][2]
                self.actual[x, y, 0] = grey_component
                self.actual[x, y, 1] = grey_component
                self.actual[x, y, 2] = grey_component

    def lighten(self):
        self.actual = self.actual + (256 - self.actual) * 0.2

    def darken(self):
        self.actual = self.actual * 0.75

    def enhance_edges(self):
        new = self.actual.copy()
        enhance_filter = np.asarray([[ 0, -1,  0],
                                     [-1,  5, -1],
                                     [ 0, -1,  0]])

        for x in range(1, new.shape[0] - 1):
            for y in range(1, new.shape[1] - 1):
                for c in range(new.shape[2]):
                    component = (enhance_filter[0][0] * self.actual[x - 1, y - 1, c]
                                 + enhance_filter[0][1] * self.actual[x - 1, y, c]
                                 + enhance_filter[0][2] * self.actual[x - 1, y + 1, c]
                                 + enhance_filter[1][0] * self.actual[x, y - 1, c]
                                 + enhance_filter[1][1] * self.actual[x, y, c]
                                 + enhance_filter[1][2] * self.actual[x, y + 1, c]
                                 + enhance_filter[2][0] * self.actual[x + 1, y - 1, c]
                                 + enhance_filter[2][1] * self.actual[x + 1, y, c]
                                 + enhance_filter[2][2] * self.actual[x + 1, y + 1, c])
                    if component > 255:
                        component = 255
                    if component < 0:
                        component = 0
                    new[x, y, c] = component

        self.actual = new

    def save_each(self):
        # rotate cw
        self.reset_image()
        self.rotate_cw()
        self.save_image("rotated_cw.jpg")

        # rotate ccw
        self.reset_image()
        self.rotate_ccw()
        self.save_image("rotated_ccw.jpg")

        # mirror x
        self.reset_image()
        self.mirror_x()
        self.save_image("mirrored_x.jpg")

        # mirror y
        self.reset_image()
        self.mirror_y()
        self.save_image("mirrored_y.jpg")

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
