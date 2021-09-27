#! /bin/local/python
# _*_ coding: utf-8 _*_
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QAbstractItemView, QListView, QMessageBox

import dialogsearch
import traceback
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt




class dialogsearch_c (QtWidgets.QDialog):

    mIsFirst = True

    def __init__(self,parent) -> None:
        super().__init__()

        self.ui = dialogsearch.Ui_Dialog()
        self.ui.setupUi(self)
        self.pw = parent

        self.setWindowTitle("Search")

        self.ui.lbClose.clicked.connect(self.close)
        self.ui.lbNext.clicked.connect(self.search)

        self.ui.cbFromtop.stateChanged.connect(self.resetMark)
        self.ui.txtSearch.textChanged.connect(self.resetMark)

    def resetMark(self):
        self.mIsFirst = True


    def search(self):

        strsearch = self.ui.txtSearch.text()
        strfromtop = self.ui.cbFromtop.checkState()

        if self.mIsFirst:
            if strsearch.isspace() == False:
                if strfromtop == Qt.Checked:
                    self.lr = self.pw.search(strsearch , 0)
                    self.mIsFirst = False
                else:
                    self.lr = self.pw.search(strsearch , -1)
                    self.mIsFirst = False

            self.pw.showError(str(self.lr))

            if self.lr == -1:
                QMessageBox.information(self,"Info","找不到指定的内容")

        else:
            if self.lr  >= 0:
                self.lr = self.pw.search(strsearch, self.lr + 1)

                self.pw.showError(str(self.lr))

                if self.lr == -1:
                    QMessageBox.information(self,"Info","找不到指定的内容")


