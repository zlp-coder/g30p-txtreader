#! /bin/local/python
# _*_ coding: utf-8 _*_
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QAbstractItemView, QListView, QApplication

import dialogmarkdown
import traceback
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

class dialogmarkdown_c(QtWidgets.QDialog):

    pw = None
    blocktext =""

    def __init__(self, parent, title, blocktext):
        try:
            QtWidgets.QDialog.__init__(self)

            self.ui = dialogmarkdown.Ui_Dialog()
            self.ui.setupUi(self)

            self.setWindowTitle("批注")
            self.pw = parent

            self.ui.lbTitle.setText( title)
            self.blocktext = blocktext
            self.linetitle = title

            self.ui.buttonBox.accepted.connect(self.saveMark)
            self.ui.buttonBox.rejected.connect(self.cancle)
            self.ui.txtMark.keyPressEvent.connect()

        except:
            traceback.print_exc()


    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(a0)

        try:
            if a0.key() == Qt.Key_F12:
                self.saveMark()

            if a0.key() == Qt.Key_Escape:
                self.cancle()

        except:
            traceback.print_exc()


    def cancle(self):
        self.close()


    def saveMark(self):
        try:
            s = self.ui.txtMark.toPlainText()

            if s.isspace() == False:
                self.pw.saveMark(s, self.linetitle , self.blocktext)

                if str.lower(self.pw.mFtype) == ".txt":
                    self.pw.loadBook(self.pw.mLines_begin)
                if str.lower(self.pw.mFtype) == ".pdf" or str.lower(self.pw.mFtype) == ".epub":
                    self.pw.loadBook(self.pw.mLines)

                self.close()
        except Exception as ex:
            traceback.print_exc()
            self.pw.showError(str(ex))