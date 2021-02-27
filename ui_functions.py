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

        self.ui.btn_list_remove.clicked.connect(lambda: self.ui.blender_folder_list.remove_current())
        self.ui.btn_list_remove.setAcceptDrops(True)
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

class RemoveButton(QPushButton):
    def __init__(self,parent =None):
        super().__init__(parent)


    def dragEnterEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        event.accept()

# promote
class DropBlenderFolders(QListWidget):
    """PROMOTE"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._placeholder_text = 'Drop Your Blender Folders Here!'

        # 双击可编辑
        self.edited_item = self.currentItem()
        self.close_flag = True
        self.doubleClicked.connect(self.item_double_clicked)
        self.currentItemChanged.connect(self.close_edit)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """回车事件，关闭edit"""
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            if self.close_flag:
                self.close_edit()
            self.close_flag = True

    def edit_new_item(self) -> None:
        """edit一个新的item"""
        self.close_flag = False
        self.close_edit()
        count = self.count()
        self.addItem('')
        item = self.item(count)
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)

    def item_double_clicked(self, modelindex: QtCore.QModelIndex) -> None:
        """双击事件"""
        self.close_edit()
        item = self.item(modelindex.row())
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)

    def close_edit(self, *_) -> None:
        """关闭edit"""
        if self.edited_item and self.isPersistentEditorOpen(self.edited_item):
            self.closePersistentEditor(self.edited_item)


    def remove_current(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def get_item_list(self):
        return [self.item(i).text() for i in range(self.count())]

    # place holder
    @property
    def placeholder_text(self):
        return self._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, text):
        self._placeholder_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QtGui.QPainter(self.viewport())
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                self.placeholder_text, QtCore.Qt.ElideLeft, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), QtCore.Qt.AlignCenter, elided_text)
            painter.restore()
        else:
            self._placeholder_text = 'Drag to add/remove/reorder\nDouble click to edit, "Enter" to confirm Edit'
            painter = QtGui.QPainter(self.viewport())
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                self.placeholder_text, QtCore.Qt.ElideLeft, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom , elided_text)
            painter.restore()
    # EVENTS
    ########################################
    def dragMoveEvent(self, event):
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(DropBlenderFolders, self).dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = []
            for url in event.mimeData().urls():
                paths.append(url.toLocalFile())
            self.addItems(paths)
            event.accept()
        else:
            super(DropBlenderFolders, self).dropEvent(event)

# utils
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

        try:
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
        except Exception:
            self.path = None
            self.bl_info = {}
