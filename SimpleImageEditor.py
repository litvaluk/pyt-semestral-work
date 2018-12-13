import numpy as np
import os
from PIL import Image
from PyQt5 import QtWidgets, uic, QtGui, QtCore


class SimpleImageEditor:
    def __init__(self):
        # load image
        self.original = None
        self.actual = None

        # create app and main window
        self.app = QtWidgets.QApplication([])
        self.main_window = QtWidgets.QMainWindow()

        # load ui
        with open('ui/main_window.ui') as f:
            self.ui = uic.loadUi(f, self.main_window)

        # set up ui
        self.set_up_ui()

        # open
        self.open_image()

    def exec(self):
        self.app.exec()

    def set_up_ui(self):
        # window properties
        self.main_window.setFixedSize(1280, 720)
        self.main_window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        # icon
        icon = QtGui.QIcon("ui/sie_icon.png")
        self.app.setWindowIcon(icon)

        # logo
        logo_qpixmap = QtGui.QPixmap("ui/sie_logo.png")
        self.ui.logo.setPixmap(logo_qpixmap)

        # image preview
        self.ui.image.setAlignment(QtCore.Qt.AlignCenter)
        self.update_image()

        # # buttons
        self.ui.rotate_cw_btn.clicked.connect(self.rotate_cw)
        self.ui.rotate_ccw_btn.clicked.connect(self.rotate_ccw)
        self.ui.mirror_x_btn.clicked.connect(self.mirror_x)
        self.ui.mirror_y_btn.clicked.connect(self.mirror_y)
        self.ui.invert_colors_btn.clicked.connect(self.invert_colors)
        self.ui.greyscale_btn.clicked.connect(self.greyscale)
        self.ui.lighten_btn.clicked.connect(self.lighten)
        self.ui.darken_btn.clicked.connect(self.darken)
        self.ui.enhance_edges_btn.clicked.connect(self.enhance_edges)
        self.ui.save_btn.clicked.connect(self.save_image)
        self.ui.open_btn.clicked.connect(self.open_image)
        self.ui.reset_btn.clicked.connect(self.reset_image)
        self.ui.exit_btn.clicked.connect(self.app.exit)

        # show window
        self.main_window.show()

    def update_image(self):
        if self.actual is not None:
            Image.fromarray(np.uint8(self.actual)).save("tmp.jpg")
            image_qimage = QtGui.QImage("tmp.jpg")
            os.remove("tmp.jpg")

            if image_qimage.height() > self.ui.image.height() or image_qimage.width() > self.ui.image.width():
                image_qpixmap = QtGui.QPixmap(image_qimage.scaled(self.ui.image.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            else:
                image_qpixmap = QtGui.QPixmap(image_qimage)

            self.ui.image.setPixmap(image_qpixmap)
            self.ui.image.repaint()

    def save_image(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Save failed! No image opened.")
        elif len(self.ui.save_tf.text()) is not 0:
            Image.fromarray(np.uint8(self.actual)).save(str(self.ui.save_tf.text()) + "." + str(self.ui.format_cb.currentText()).lower())
            QtWidgets.QMessageBox.information(self.main_window, "Success", "Image has been saved successfully.")
        else:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Save failed! Image name is not specified.")

    def open_image(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.main_window, caption="Open image", filter="Image files (*.jpg *.png *.bmp)")[0]
        if fname is not '':
            self.original = np.asarray(Image.open(fname).convert("RGB"))
            self.actual = self.original.copy()
            self.update_image()

    def reset_image(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Reset failed! No image opened.")
            return
        self.actual = self.original.copy()
        self.update_image()

    def rotate_cw(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = np.rot90(self.actual, -1)
        self.update_image()

    def rotate_ccw(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = np.rot90(self.actual)
        self.update_image()

    def mirror_x(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = self.actual[::-1]
        self.update_image()

    def mirror_y(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = self.actual[::, ::-1]
        self.update_image()

    def invert_colors(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = 255 - self.actual
        self.update_image()

    def greyscale(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        for y in range(self.actual.shape[1]):
            for x in range(self.actual.shape[0]):
                grey_component = 0.299 * self.actual[x][y][0] + 0.587 * self.actual[x][y][1] + 0.114 * \
                                 self.actual[x][y][2]
                self.actual[x, y, 0] = grey_component
                self.actual[x, y, 1] = grey_component
                self.actual[x, y, 2] = grey_component
        self.update_image()

    def lighten(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = self.actual + (255 - self.actual) * 0.2
        self.update_image()

    def darken(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
        self.actual = self.actual * 0.75
        self.update_image()

    def enhance_edges(self):
        if self.actual is None:
            QtWidgets.QMessageBox.critical(self.main_window, "Failure", "Operation failed! No image opened.")
            return
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
        self.update_image()
