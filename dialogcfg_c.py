#! /bin/local/python
# _*_ coding: utf-8 _*_
import sqlite3

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QAbstractItemView, QListView, QMessageBox

import dialogcfg
import traceback
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

class dialogcfg_c(QtWidgets.QDialog):

    def __init__(self, parent ):
        try:
            QtWidgets.QMainWindow.__init__(self)
            self.ui = dialogcfg.Ui_Dialog()
            self.ui.setupUi(self)

            self.setWindowTitle("Setup")
            self.pw = parent

            self.ui.lbClose.clicked.connect(self.close)
            self.ui.lbConfirm.clicked.connect(self.applyStyle)

            self.ui.txtReadStyle.setText(self.pw.readConfig("READ_STYLE"))

            self.ui.txtList.clear()
            self.ui.txtList.append("background-color: rgb(233, 250, 255);color: rgb(85, 85, 85);"
                                   "font-family: Microsoft YaHei;font-size: 15px; letter-spacing: 0.2em;line-height:150%;")
            self.ui.txtList.append("")
            self.ui.txtList.append("background-color: rgb(0, 0, 0);color: rgb(0, 255, 0);"
                                   "font-family: Microsoft YaHei;font-size: 15px; letter-spacing: 0.1em;line-height:150%;")

        except Exception as ex:
            traceback.print_exc()
            self.pw.showError(ex)


    def applyStyle(self):

        strStyle = self.ui.txtReadStyle.toPlainText()

        try:
            self.pw.ui.txtMain.setStyleSheet(strStyle)
        except Exception as ex:
            QMessageBox.show(self,"Info" , "设置失败：" +  str(ex))
        else:
            self.pw.writeConfig("READ_STYLE", strStyle)