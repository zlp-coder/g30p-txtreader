#! /bin/local/python
# _*_ coding: utf-8 _*_
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QAbstractItemView, QListView

import dialoglist
import traceback
from PyQt5 import QtWidgets, QtGui

class dialoglist_c(QtWidgets.QDialog):

    pw = None

    def __init__(self, parent):
        try:
            QtWidgets.QMainWindow.__init__(self)

            self.ui = dialoglist.Ui_Dialog()
            self.ui.setupUi(self)

            self.setWindowTitle("Chapter List")
            self.pw = parent

            self.ui.listMenu.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.listMenu.setResizeMode(QListView.Adjust)

            self.ui.listMenu.clicked.connect(self.itemSelected)


            strlist = []
            for item in parent.mBookMenu:
                strlist.append(item["title"])

            model = QStringListModel()
            model.setStringList(strlist)
            self.ui.listMenu.setModel(model)
        except:
            traceback.print_exc()


    def itemSelected(self,index):
        for item in self.pw.mBookMenu:
            if item["title"] == index.data():
                self.pw.mLines = item["line"]
                self.pw.mLines_prev = item["line"] - 20 if item["line"] - 20 > 0 else 0
                self.pw.loadBook(item["line"])
                self.close()

