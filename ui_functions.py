import os
import time
import json

## ==> GUI FILE
from main import *

## ==> GLOBALS
GLOBAL_STATE = 0


class UIFunctions(MainWindow):

    ## ==> UI DEFINITIONS
    def uiDefinitions(self):
        # REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        """use image instead of effect"""
        # SET DROPSHADOW WINDOW
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(20)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(0, 0, 0, 100))
        # self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)

        # ==> CREATE SIZE GRIP TO RESIZE WINDOW
        # self.sizegrip = QSizeGrip(self.ui.frame_grip)
        # self.sizegrip.setStyleSheet(
        #     "QSizeGrip { width: 10px; height: 10px; margin: 5px } QSizeGrip:hover { background-color: rgb(50, 42, 94) }")
        # self.sizegrip.setToolTip("Resize Window")

        # DropBlenderFolders
        self.ui.blender_folder_list.setAlternatingRowColors(True)
        self.ui.blender_folder_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.ui.blender_folder_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.ui.btn_list_remove.setAcceptDrops(True)
        self.ui.btn_list_remove.clicked.connect(lambda: self.remove_list())

        self.ui.btn_list_refresh.clicked.connect(lambda: self.update_list())

        # set launcher
        self.ui.launch_button.clicked.connect(
            lambda: os.startfile(self.blender_paths[self.ui.comboBox_bl_version.currentIndex()]))
        ## set combobox changes event
        self.ui.comboBox_bl_version.currentTextChanged.connect(lambda: self.change_bl_info())
        # set icon
        self.ui.btn_preference.setIcon(QIcon(':/img/settings.png'))
        self.ui.btn_home.setIcon(QIcon(':/img/settings.png'))
        self.ui.btn_list_refresh.setIcon(QIcon(':/img/refresh.png'))
        self.ui.btn_list_remove.setIcon(QIcon(':/img/del.png'))
        # set stackedWidget
        self.ui.btn_preference.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_pref))
        self.ui.btn_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_home))

        ## RETURN STATUS IF WINDOWS IS MAXIMIZE OR RESTAURED

    def returnStatus():
        return GLOBAL_STATE
