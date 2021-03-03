# coding: UTF-8
import sys
import subprocess
import platform
import os, json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

# GUI FILE
from demo import *

# images
import images_rc

# IMPORT FUNCTIONS
from ui_functions import *

from theme.qss import dark as dark_theme
from theme.qss import white as white_theme

from utils.blender_info import *


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
        QMainWindow.__init__(self, None)
        # QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint) # keep on top
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

        # CLOSE
        self.ui.btn_close.clicked.connect(lambda: self.close_window())
        # theme
        self.ui.checkBox_theme.stateChanged.connect(lambda: self.theme_state_change())
        # drop to load file
        self.ui.launch_button.itemDropped.connect(lambda: self.load_file_by_drop())
        # folder list auto save with drop
        self.ui.blender_folder_list.update_list.connect(lambda: self.update_list())
        self.ui.btn_list_remove.update_list.connect(lambda: self.remove_list())
        # load preference
        self.load_pref()

        ## SHOW
        #####################################################################
        self.show()
        self.unfade(self.ui.drop_shadow_frame, time=250)
        #####################################################################

        # init interface data
        self.update_list()
        self.change_bl_info()

    def load_file_by_drop(self):
        file = self.ui.launch_button.file
        blender = self.blender_paths[self.ui.comboBox_bl_version.currentIndex()]

        try:
            file = self.ui.launch_button.file
            filename = os.path.basename(file)
            dir = os.path.dirname(file)
            cmd1 = f'cd {dir}'
            cmd2 = f'"{blender}" {filename}'

            cmd = cmd1 + " & " + cmd2
            os.system(cmd)
        except Exception as e:
            msg_box = QtWidgets.QMessageBox
            msg_box.question(self, 'Error', 'Can not Open File', msg_box.Ok)

    # load and sav preference
    def load_pref(self):
        if os.path.exists('pref.json'):
            with open('pref.json', 'r') as f:
                data = json.load(f)
                # load theme
                if 'theme' in data:
                    theme_state = data["theme"]
                    theme = 0 if theme_state == 'white' else 2
                    self.ui.checkBox_theme.setCheckState(theme)
                    self.set_theme(theme)
                    data.pop("theme")
                # load blender list item
                self.ui.blender_folder_list.addItems(data.values())
        # save
        self.save_pref()

    def save_pref(self):
        print('save!')
        dict = {}
        for i in range(self.ui.blender_folder_list.count()):
            dict[i] = self.ui.blender_folder_list.item(i).text()

        if self.get_theme_state():
            dict['theme'] = 'dark'
        else:
            dict['theme'] = 'white'

        try:
            with open('pref.json', 'w') as f:
                json.dump(dict, f, indent=4)
        except Exception:
            msg_box = QtWidgets.QMessageBox
            msg_box.question(self, 'Error', 'Can Not Save Preference!', msg_box.Ok)

    def get_theme_state(self):
        return self.ui.checkBox_theme.isChecked()

    def theme_state_change(self):
        if self.get_theme_state() == 0:
            self.set_theme(use_dark_theme=False)
        else:
            self.set_theme(use_dark_theme=True)

    def set_theme(self, use_dark_theme=False):
        # use theme
        theme = dark_theme if use_dark_theme else white_theme
        # self.setStyleSheet(theme)
        self.ui.drop_shadow_frame.setStyleSheet(theme)
        self.ui.checkBox_theme.setStyleSheet(theme)

        self.ui.btn_minimize.setStyleSheet(theme)
        self.ui.btn_close.setStyleSheet(theme)
        self.ui.btn_list_remove.setStyleSheet(theme)
        self.ui.btn_list_refresh.setStyleSheet(theme)
        self.ui.btn_preference.setStyleSheet(theme)
        self.ui.btn_home.setStyleSheet(theme)

        self.ui.comboBox_bl_version.setStyleSheet(theme)
        self.ui.launch_button.setStyleSheet(theme)

        self.ui.label_title.setStyleSheet(theme)

        self.ui.blender_folder_list.setStyleSheet(theme)
        self.ui.blender_folder_list.verticalScrollBar().setStyleSheet(theme)

    ## fade animaiton
    def fade(self, widget, time=1000):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(time)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget, time=500):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(time)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    ## APP EVENTS
    ########################################################################
    def close_window(self):
        self.save_pref()
        self.close()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def remove_list(self):
        self.ui.blender_folder_list.remove_current()
        self.update_list()

    def update_list(self):
        self.save_pref()
        # clear
        self.blender_paths.clear()
        self.ui.blender_folder_list.clear()
        self.ui.comboBox_bl_version.clear()

        # load preference
        self.load_pref()
        for i in range(self.ui.blender_folder_list.count()):
            path = self.ui.blender_folder_list.item(i).text()
            bl = Blender(path=path)
            if bl.path:
                self.blender_paths.append(bl.path)
                self.blender_info.append(bl.bl_info)
                self.ui.comboBox_bl_version.addItem(bl.version)
            else:
                msg_box = QtWidgets.QMessageBox
                msg_box.question(self, 'Error', f'There is not "blender.exe" in path:\n{path}',
                                 msg_box.Ok)

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
