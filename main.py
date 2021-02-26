import sys
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
        # CLOSE
        self.ui.btn_close.clicked.connect(lambda: self.close_window())

        # load preference
        self.load_pref()

        ## SHOW
        #####################################################################
        self.show()
        self.unfade(self.ui.drop_shadow_frame, time=500)
        #####################################################################

        # init interface data
        self.update_list()
        self.change_bl_info()

    # load and sav preference
    def load_pref(self):
        if os.path.exists('pref.json'):
            with open('pref.json', 'r') as f:
                data = json.load(f)
                # load theme
                try:
                    theme_state = data["theme"]
                    theme = 0 if theme_state == 'white' else 2
                    self.ui.checkBox_theme.setCheckState(theme)
                    data.pop("theme")
                except KeyError:
                    self.save_pref()
                    self.ui.checkBox_theme.setCheckState(0)
                    self.set_theme('theme/white.qss')
                # load blender list item
                self.ui.blender_folder_list.addItems(data.values())
        else:
            self.save_pref()

    def save_pref(self):
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
        if self.get_theme_state():
            self.set_theme(qss_file='theme/black.qss')
            with open('pref.json', 'r') as f:
                data = json.load(f)
                data['theme'] = 'black'
                # write theme
                with open('pref.json', 'w') as f:
                    json.dump(data, f)
        else:
            self.set_theme(qss_file='theme/white.qss')

    def set_theme(self, qss_file):
        theme = open(qss_file, 'r', encoding='utf-8').read()
        self.setStyleSheet(theme)
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

    ## fade animaiton
    def fade(self, widget, time=1000):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(time)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget, time=1000):
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
