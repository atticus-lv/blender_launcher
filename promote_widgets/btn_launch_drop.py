import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class DropOpenFile(QPushButton):
    itemDropped = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def dragMoveEvent(self, event):
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        self.file = None
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().endswith('.blend'):
                    self.file = url.toLocalFile()
                    self.itemDropped.emit()
                    event.accept()
