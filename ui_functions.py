import os
import time
import json
## ==> GUI FILE
from main import *

## ==> GLOBALS

GLOBAL_STATE = 0
THEME = 0

class UIFunctions(MainWindow):

    ## ==> UI DEFINITIONS
    def uiDefinitions(self):
        # REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # SET DROPSHADOW WINDOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        # APPLY DROPSHADOW TO FRAME
        self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)

        # theme check
        self.ui.checkBox_theme.stateChanged.connect(lambda :self.theme_state_change())

        # MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        # CLOSE
        self.ui.btn_close.clicked.connect(lambda: self.close())

        # ==> CREATE SIZE GRIP TO RESIZE WINDOW
        # self.sizegrip = QSizeGrip(self.ui.frame_grip)
        # self.sizegrip.setStyleSheet(
        #     "QSizeGrip { width: 10px; height: 10px; margin: 5px } QSizeGrip:hover { background-color: rgb(50, 42, 94) }")
        # self.sizegrip.setToolTip("Resize Window")

        # DropBlenderFolders
        self.ui.blender_folder_list.setAlternatingRowColors(True)
        self.ui.btn_list_remove.clicked.connect(lambda: self.ui.blender_folder_list.remove_current())
        self.ui.btn_list_refresh.clicked.connect(lambda: self.update_list())

        # set launcher
        self.ui.launch_button.clicked.connect(
            lambda: os.startfile(self.blender_paths[self.ui.comboBox_bl_version.currentIndex()]))

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



class DropBlenderFolders(QListWidget):
    """PROMOTE"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.load_all()

    def load_all(self):
        if os.path.exists('pref.json'):
            with open('pref.json', 'r') as f:
                data = json.load(f)
                self.addItems(data.values())

    def remove_current(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def save_all(self):
        dict = {}
        for i in range(self.count()):
            dict[i] = self.item(i).text()
        with open('pref.json', 'w') as f:
            json.dump(dict, f, indent=4)

    def get_item_list(self):
        return [self.item(i).text() for i in range(self.count())]

    # events
    # drag and drop file
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = []
            for url in event.mimeData().urls():
                paths.append(url.toLocalFile())
            self.addItems(paths)
            event.accept()


class Blender():
    """
    :parm bl_info:{
                    'name'      : self.name,
                    'build_time': self.build_time,
                    'path'      : self.path,
                    'version'   : self.version,
                    }
    """

    def __init__(self, path):
        self.bl_info = {}
        self.generate_info_dict(path)

    def generate_info_dict(self, path):
        dir = path.replace('\n', '')
        self.path = os.path.join(dir, 'blender.exe')
        dirname = os.path.basename(os.path.dirname(self.path))

        try:
            version = dirname.split('-')[1]
        except:
            version = dirname[7:]

        self.name = dirname
        self.version = version
        self.build_time = time.ctime(os.stat(self.path).st_mtime)
        # dict
        self.bl_info = {
            'name'      : self.name,
            'build_time': self.build_time,
            'path'      : self.path,
            'version'   : self.version,
        }
