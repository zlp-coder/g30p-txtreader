#! /bin/local/python
# _*_ coding: utf-8 _*_

import sys
from PyQt5.QtWidgets import QApplication

import mainwindow_c

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = mainwindow_c.mainwindow_c()
    w.show()

    sys.exit(app.exec_())