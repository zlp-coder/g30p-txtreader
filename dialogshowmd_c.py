#! /bin/local/python
# _*_ coding: utf-8 _*_
import sqlite3

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QAbstractItemView, QListView

import dialogshowmd
import traceback
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

class dialogshowmd_c(QtWidgets.QDialog):

    pw = None
    blocktext =""


    def __init__(self, parent , id):
        try:
            QtWidgets.QMainWindow.__init__(self)
            self.ui = dialogshowmd.Ui_Dialog()
            self.ui.setupUi(self)

            self.setWindowTitle("remark")

            self.pw = parent
            self.id = id
            self.conn = parent.conn

            data =  self.pw.readMark(self.id)

            if data == None:
                self.ui.txtMarkdown.setText("加载批注失败，没有找到数据。id={}".format(self.id))
            else:
                self.ui.txtMarkdown.setText(data[3] )

            self.ui.lbClosen.clicked.connect(self.close)
            self.ui.lbSave.clicked.connect(self.saveMark)
            self.ui.lbDelete.clicked.connect(self.delMark)

        except Exception as ex:
            traceback.print_exc()
            self.pw.showError(str(ex))

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(a0)

        try:
            if a0.key() == Qt.Key_F12:
                self.saveMark()

        except:
            traceback.print_exc()


    def saveMark(self):
        try:
            node = self.ui.txtMarkdown.toPlainText()
            node = node.replace("'","")
            node = node.replace("\"", "")

            sql = """update book_detail set mark_down = '{}' where id = {}""".format( node ,self.id )
            self.conn.execute(sql)

            self.close()
        except Exception as ex:
            traceback.print_exc()
            self.pw.showError(ex)

    def delMark(self):
        try:
            sql = """delete from book_detail where id = {}""".format(self.id )
            self.conn.execute(sql)

            self.pw.loadBook(self.pw.mLines_begin)
            self.close()

        except Exception as ex:
            traceback.print_exc()
            self.pw.showError(ex)