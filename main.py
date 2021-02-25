import sys
import platform

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

# GUI FILE
from demo import *

# IMPORT FUNCTIONS
from ui_functions import *


class MainWindow(QMainWindow):
    def set_properties(self):
        """
        :parm blender_paths:all the blender.exe path
        :parm blender_paths:all the blender info dict
        :parm current_path:current_path for combobox
        :return:
        """
        self.blender_paths = []
        self.blender_info = []
        self.current_path = None

    def __init__(self):
        self.set_properties()
        # ui
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MOVE WINDOW
        def moveWindow(event):
            # RESTORE BEFORE MOVE
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.title_bar.mouseMoveEvent = moveWindow

        ## ==> SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)

        # init interface
        self.update_list()
        self.change_bl_info()
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        ## set combobox changes event
        self.ui.comboBox_bl_version.currentTextChanged.connect(lambda: self.change_bl_info())

        ## SHOW
        #####################################################################
        self.show()
        #####################################################################

    ## APP EVENTS
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def update_list(self):
        # save
        self.ui.blender_folder_list.save_all()
        # clear
        self.blender_paths.clear()
        self.ui.blender_folder_list.clear()
        self.ui.comboBox_bl_version.clear()

        # load preference
        self.ui.blender_folder_list.load_all()
        for i in range(self.ui.blender_folder_list.count()):
            path = self.ui.blender_folder_list.item(i).text()
            bl = Blender(path=path)
            self.blender_paths.append(bl.path)
            self.blender_info.append(bl.bl_info)
            self.ui.comboBox_bl_version.addItem(bl.version)

    def change_bl_info(self):
        index = self.ui.comboBox_bl_version.currentIndex()
        if len(self.blender_info) != 0:
            bl_info = self.blender_info[index]
            self.ui.blender_info.setText(
                f'{bl_info["build_time"]}\n{bl_info["path"]}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
