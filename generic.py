from PyQt5 import QtGui, QtCore, QtWidgets
from datetime import timedelta

class mysteryTime(timedelta):
    def __sub__(self, other):
        return self
    def __eq__(self, other):
        return (type(other) is mysteryTime)
    def __neq__(self, other):
        return (type(other) is not mysteryTime)
    def __hash__(self):
        return 0

class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)
    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())
    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(key.lower())
    def has_key(self, key):
        return key.lower() in super(CaseInsensitiveDict, self)
    def __delitem__(self, key):
        super(CaseInsensitiveDict, self).__delitem__(key.lower())

class PesterList(list):
    def __init__(self, l):
        self.extend(l)

class PesterIcon(QtGui.QIcon):
    def __init__(self, *x):
        QtGui.QIcon.__init__(self, x[0])
        if type(x[0]) in [str]:
            self.icon_pixmap = QtGui.QPixmap(x[0])
        else:
            self.icon_pixmap = None
    def realsize(self):
        if self.icon_pixmap:
            return self.icon_pixmap.size()
        else:
            try:
                return self.availableSizes()[0]
            except IndexError:
                return None

class RightClickList(QtWidgets.QListWidget):
    def contextMenuEvent(self, event):
        #fuckin Qt
        if event.reason() == QtGui.QContextMenuEvent.Mouse:
            listing = self.itemAt(event.pos())
            self.setCurrentItem(listing)
            optionsMenu = self.getOptionsMenu()
            if optionsMenu:
                optionsMenu.popup(event.globalPos())
    def getOptionsMenu(self):
        return self.optionsMenu

class RightClickTree(QtWidgets.QTreeWidget):
    def contextMenuEvent(self, event):
        if event.reason() == QtGui.QContextMenuEvent.Mouse:
            listing = self.itemAt(event.pos())
            self.setCurrentItem(listing)
            optionsMenu = self.getOptionsMenu()
            if optionsMenu:
                optionsMenu.popup(event.globalPos())
    def getOptionsMenu(self):
        return self.optionsMenu

class MultiTextDialog(QtWidgets.QDialog):
    def __init__(self, title, parent, *queries):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        if len(queries) == 0:
            return
        self.inputs = {}
        layout_1 = QtWidgets.QHBoxLayout()
        for d in queries:
            label = d["label"]
            inputname = d["inputname"]
            value = d.get("value", "")
            l = QtWidgets.QLabel(label, self)
            layout_1.addWidget(l)
            self.inputs[inputname] = QtWidgets.QLineEdit(value, self)
            layout_1.addWidget(self.inputs[inputname])
        self.ok = QtWidgets.QPushButton("OK", self, clicked=self.accept)
        self.ok.setDefault(True)
        self.cancel = QtWidgets.QPushButton("CANCEL", self, clicked=self.reject)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addLayout(layout_1)
        layout_0.addLayout(layout_ok)

        self.setLayout(layout_0)
    def getText(self):
        r = self.exec_()
        if r == QtWidgets.QDialog.Accepted:
            retval = {}
            for (name, widget) in self.inputs.items():
                retval[name] = str(widget.text())
            return retval
        else:
            return None

class MovingWindow(QtWidgets.QFrame):
    def __init__(self, *x, **y):
        QtWidgets.QFrame.__init__(self, *x, **y)
        self.moving = None
        self.moveupdate = 0
    def mouseMoveEvent(self, event):
        if self.moving:
            move = event.globalPos() - self.moving
            self.move(move)
            self.moveupdate += 1
            if self.moveupdate > 5:
                self.moveupdate = 0
                self.update()
    def mousePressEvent(self, event):
        if event.button() == 1:
            self.moving = event.globalPos() - self.pos()
    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.update()
            self.moving = None

class NoneSound(object):
    def play(self): pass
    def setVolume(self, v): pass

class WMButton(QtWidgets.QPushButton):
    def __init__(self, icon, parent=None):
        QtWidgets.QPushButton.__init__(self, icon, "", parent)
        self.setIconSize(icon.realsize())
        self.resize(icon.realsize())
        self.setFlat(True)
        self.setStyleSheet("QPushButton { padding: 0px; }")
        self.setAutoDefault(False)
