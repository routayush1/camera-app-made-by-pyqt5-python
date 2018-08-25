from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5 import QtCore

import os
import sys
import time


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setMinimumSize(QtCore.QSize(927, 506))
        self.setMaximumSize(QtCore.QSize(927, 506))

        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            pass #quit

        self.status = QStatusBar()
        self.setStatusBar(self.status)


        self.save_path = ""

        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)

        # Set the camera sensors(between 0,1,2) for your webcam .
        self.select_camera(2)


        camera_toolbar = QToolBar("Camera")
        camera_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(camera_toolbar)

        photo_action = QAction(QIcon(os.path.join('images', 'camera-black.png')), "Take photo...", self)
        photo_action.setStatusTip("Take photo of current view")
        photo_action.triggered.connect(self.take_photo)
        camera_toolbar.addAction(photo_action)




        self.setWindowTitle("ayush camera")
        self.show()

    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda i, e, s: self.alert(s))
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image %04d captured" % self.save_seq))

        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0

    def take_photo(self):
        self.viewfinder.setContrast(100)


        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.save_path, "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )))
        self.save_seq += 1



if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("ayush camera")

    window = MainWindow()
    app.exec_()