# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogsearch.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 79)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 54, 12))
        self.label.setObjectName("label")
        self.txtSearch = QtWidgets.QLineEdit(Dialog)
        self.txtSearch.setGeometry(QtCore.QRect(70, 10, 561, 20))
        self.txtSearch.setObjectName("txtSearch")
        self.lbClose = QtWidgets.QPushButton(Dialog)
        self.lbClose.setGeometry(QtCore.QRect(550, 50, 75, 23))
        self.lbClose.setObjectName("lbClose")
        self.lbNext = QtWidgets.QPushButton(Dialog)
        self.lbNext.setGeometry(QtCore.QRect(460, 50, 75, 23))
        self.lbNext.setObjectName("lbNext")
        self.cbFromtop = QtWidgets.QCheckBox(Dialog)
        self.cbFromtop.setGeometry(QtCore.QRect(10, 50, 151, 16))
        self.cbFromtop.setObjectName("cbFromtop")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Search"))
        self.lbClose.setText(_translate("Dialog", "CLose"))
        self.lbNext.setText(_translate("Dialog", "Go"))
        self.cbFromtop.setText(_translate("Dialog", "From top"))
