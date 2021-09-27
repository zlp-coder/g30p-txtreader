#! /bin/local/python
# _*_ coding: utf-8 _*_
import codecs
import os
import sys
import traceback
from tkinter import Image

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont, QKeyEvent, QKeySequence, QImage, QPixmap, QColor, QCursor, QTextCursor, \
    QWheelEvent
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QAction, QTextEdit, QLabel, QFileDialog, \
    QVBoxLayout, QGraphicsScene, QMenu, QSpacerItem, QSizePolicy, QPushButton, QGraphicsItem
from PyQt5.QtCore import Qt, QTimer, QPoint
from pip._vendor import chardet

import dialoglist
import dialogsearch_c
import dialogshowmd
import mainwindow
import sqlite3
import json
import re
import pyperclip
from functools import partial

import fitz
import zipfile
import cv2
import numpy


from dialogcfg_c import dialogcfg_c
from dialoglist_c import dialoglist_c
from dialogmarkdown_c import dialogmarkdown_c
from dialogshowmd_c import dialogshowmd_c


class mainwindow_c(QtWidgets.QMainWindow):
    conn = sqlite3.connect('g30p-txtreader.db')
    encoding = "gbk"
    mFullname = ""
    mFname = ""
    mFtype = ""
    mLines = 0
    mLines_end = 0
    mLines_begin = 0
    mLines_prev = 0
    mAllLines = 0
    mBookMenu = []
    mMark_data = []

    mPdfResize = 1.5

    mImageResize = 1.0

    mImageXStep = 0.1
    mImageYStep = 0.1

    mImageX = 0.1
    mImageY = 0.1

    mReadStyle = "background-color: rgb(233, 250, 255);color: rgb(85, 85, 85);font-family: Microsoft YaHei;font-size: 15px; letter-spacing: 0.2em;line-height:150%;"

    def __init__(self):
        try:
            QtWidgets.QMainWindow.__init__(self)

            self.ui = mainwindow.Ui_MainWindow()
            self.ui.setupUi(self)

            self.setFocus()
            self.setWindowTitle("g30p阅读器")
            self.showMaximized()

            self.initDBCfg()
            self.initDBBookList()
            self.initDBBookDetail()

            #self.ui.mainToolBar.addAction(QAction(QIcon(os.getcwd() + "/res/b2.ico"), "open", self))
            #self.ui.mainToolBar.addAction(QAction(QIcon(os.getcwd() + "/res/b4.ico"), "list", self))
            #self.ui.mainToolBar.addAction(QAction(QIcon(os.getcwd() + "/res/b3.ico"), "search", self))
            #self.ui.mainToolBar.addAction(QAction(QIcon(os.getcwd() + "/res/b7.ico"), "setup", self))

            self.ui.mainToolBar.addAction(QAction(QIcon(self.resource_path(os.path.join("res", "b2.ico"))), "open", self))
            self.ui.mainToolBar.addAction(QAction(QIcon(self.resource_path(os.path.join("res", "b4.ico"))), "list", self))
            self.ui.mainToolBar.addAction(QAction(QIcon(self.resource_path(os.path.join("res", "b3.ico"))), "search", self))
            self.ui.mainToolBar.addAction(QAction(QIcon(self.resource_path(os.path.join("res", "b7.ico"))), "setup", self))

            self.ui.mainToolBar.actionTriggered[QAction].connect(self.toolbarClicked)

            self.statusMessage = QLabel("", self.ui.statusBar)
            self.ui.statusBar.addWidget(self.statusMessage,1)

            self.statusHelp = QLabel("", self.ui.statusBar)
            self.ui.statusBar.addWidget(self.statusHelp ,1)

            self.popMenu = QMenu()
            markdown = QAction("增加批注", self)
            markdown.triggered.connect(self.markdown)
            self.popMenu.addAction(markdown)
            copymenu = QAction("复制", self)
            copymenu.triggered.connect(self.copySelected)
            self.popMenu.addAction(copymenu)

            self.popMenuPDF = QMenu()
            self.popMenuPDF.addAction(markdown)

            qvPage1 = QVBoxLayout()
            qvPage1.addWidget(self.ui.txtMain)
            self.ui.page_1.setLayout(qvPage1)

            qvPage2 = QVBoxLayout()
            qvPage2.addWidget(self.ui.graphicsView)
            self.ui.page_2.setLayout(qvPage2)

            self.ui.txtMain.setOpenLinks(False)
            self.ui.txtMain.anchorClicked.connect(self.txtClicked)

            self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.ui.graphicsView.installEventFilter(self)
            self.ui.graphicsView.verticalScrollBar().setEnabled(False)
            self.ui.graphicsView.wheelEvent = self.scene_wheelEvent

            QTimer.singleShot(20, self.postLoad)

            self.scene = QGraphicsScene()

            pdfResize = self.readConfig("PdfResize")
            if pdfResize.isspace():
                self.mPdfResize = 1.2
                self.writeConfig("PdfResize" , "1.2")
            else:
                self.mPdfResize = float(pdfResize)

            imageResize = self.readConfig("ImageResize")
            if imageResize.isspace():
                self.mImageResize = 1.0
                self.writeConfig("ImageResize" , "1.2")
            else:
                self.mImageResize = float(imageResize)

            # Test code:

            # z = zipfile.ZipFile("E:\DownLoad\999.zip", "r")
            # # 打印zip文件中的文件列表
            # for filename in z.namelist():
            #     print('File:', filename)
            # # 读取zip文件中的第一个文件
            # first_file_name = z.namelist()[1]
            # content = z.read(first_file_name)
            #
            # image = QImage.fromData(content)
            # qimage2 =QPixmap.fromImage(image)
            #
            # scene = QGraphicsScene()
            # scene.addPixmap(qimage2)
            # scene.addText("hello world")
            #
            # self.ui.graphicsView.setScene(scene)
            # self.ui.stackedWidget.setCurrentIndex(1)

            # self.ui.stackedWidget.setCurrentIndex(1)
            #
            # #doc = fitz.open(r"D:\LUKE\LukeWikipedia\readinglist\写在身体上.pdf")
            # doc = fitz.open(r"E:\DownLoad\66746.epub")
            #
            # print(str(doc.pageCount))
            #
            # page = doc.loadPage(3)
            #
            # trans = fitz.Matrix(1.5, 1.5).prerotate(0)
            # pix = page.getPixmap(matrix=trans,alpha=False)
            # fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            # qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
            #
            # # image = QImage(r"E:\DownLoad\584_20210914104225937.jpg")
            # qimage2 =QPixmap.fromImage(qimage)
            #
            # scene = QGraphicsScene()
            # scene.addPixmap(qimage2)
            # scene.addText("hello world")
            #

        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))

    def txtClicked(self, url):
        try:
            id = str(url.path())

            if id.isspace(): return

            diag = dialogshowmd_c(self, id)
            diag.exec()

        except Exception as ex:
            traceback.print_exc()
            self.showError(ex)


    def toolbarClicked(self, obj):
        try:
            lbText = obj.text()
            if lbText == "open": self.openFile()
            if lbText == "list": self.listMenu()
            if lbText == "search": self.openSearch()
            if lbText == "setup": self.openCfg()

        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(a0)
        try:
            if a0.key() == Qt.Key_Right:
                if str.lower(self.mFtype) == ".txt":
                    if self.mLines_end > self.mAllLines:
                        self.mLines_end = self.mAllLines - 20

                    self.mLines_prev = self.mLines
                    self.loadBook(self.mLines_end)

                if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
                    here = self.ui.graphicsView.verticalScrollBar().value()

                    if (here + self.mPdfStepHeight) < self.mLines_end * self.mPdfPageHeigh:
                        nextstep = here + self.mPdfStepHeight
                        self.ui.graphicsView.verticalScrollBar().setValue(nextstep)

                        self.mLines = self.mLines_begin if here <= self.mPdfPageHeigh else \
                            int(here / self.mPdfPageHeigh) + 2
                        self.writeLines(self.mFname, self.mLines)

                        self.statusMessage.setText("{} ({}/{})".format(self.mFname, str(self.mLines_begin) + "-"
                                                                       + str(self.mLines_end) + " " + str(self.mLines),
                                                                       self.mAllLines))
                    else:
                        self.loadBook(self.mLines)

                if str.lower(self.mFtype) == ".zip":
                    self.mLines_prev = self.mLines
                    self.mLines = self.mLines + 1 if self.mLines + 1 < self.mAllLines else self.mAllLines
                    self.loadBook(self.mLines)

            if a0.key() == Qt.Key_Left:
                if str.lower(self.mFtype) == ".txt":
                    self.loadBook(self.mLines_prev)
                    self.mLines_prev = self.mLines_prev - 20 if self.mLines_prev - 20 > 0 else 0

                if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
                    here = self.ui.graphicsView.verticalScrollBar().value()

                    if (here - self.mPdfStepHeight) > self.mLines_begin * self.mPdfPageHeigh:
                        nextstep = here - self.mPdfStepHeight if here - self.mPdfStepHeight >0 else 0
                        self.ui.graphicsView.verticalScrollBar().setValue(nextstep)

                        self.mLines = self.mLines_begin if here <= self.mPdfPageHeigh else \
                            int(here / self.mPdfPageHeigh) + 2
                        self.mLines = self.mLines -1 if self.mLines -1 > 0 else 0
                        self.writeLines(self.mFname, self.mLines)

                        self.statusMessage.setText("{} ({}/{})".format(self.mFname, str(self.mLines_begin) + "-"
                                                                       + str(self.mLines_end) + " " + str(self.mLines),
                                                                       self.mAllLines))
                    else:
                        self.loadBook(self.mLines)

                if str.lower(self.mFtype) == ".zip":
                    self.mLines_prev = self.mLines
                    self.mLines = self.mLines - 1 if self.mLines - 1 >= 1 else 1
                    self.loadBook(self.mLines)

            if a0.key() == Qt.Key_F12 :
                self.close()

            if a0.key() == Qt.Key_Equal:
                if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
                    v = self.mPdfResize + 0.1
                    if v > 2.5: v = 2.5
                    self.mPdfResize = v
                    self.writeConfig("PdfResize", self.mPdfResize)
                    self.loadBook(self.mLines)

                if str.lower(self.mFtype) == ".zip":
                    v = self.mImageResize + 0.1
                    if v > 2.5: v = 2.5
                    self.mImageResize = v
                    self.writeConfig("ImageResize", self.mImageResize)
                    self.loadBook(self.mLines)


            if a0.key() == Qt.Key_Minus:
                if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
                    v = self.mPdfResize - 0.1
                    if v < 1.0: v = 1.0
                    self.mPdfResize = v
                    self.writeConfig("PdfResize", self.mPdfResize)
                    self.loadBook(self.mLines)

                if str.lower(self.mFtype) == ".zip":
                    v = self.mImageResize - 0.1
                    if v < 0.5: v = 0.5
                    self.mImageResize = v
                    self.writeConfig("ImageResize", self.mImageResize)
                    self.loadBook(self.mLines)

        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        super().contextMenuEvent(event)

        if str.lower(self.mFtype) == ".txt":
            self.popMenu.exec(QCursor.pos())

        if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
            self.popMenuPDF.exec(QCursor.pos())


    def openFile(self):
        try:
            lastPath = self.readConfig("LAST_PATH")
            if lastPath == "" or lastPath == None:
                lastPath =os.getcwd()

            fname, ftype = QFileDialog.getOpenFileName(self, "Open file", lastPath,
                                                       "All support(*.txt; *.pdf; *.epub; *.zip)")

            if fname == "": return

            fshortname = os.path.basename(fname)
            ftype = os.path.splitext(fshortname)[1]

            self.writeConfig("LAST_PATH", os.path.dirname(fname))

            sqlSelBook = "select * from book_list where book_name = '{}'".format(fshortname)
            res = self.conn.execute(sqlSelBook).fetchall()

            # txt encoding check
            if str.lower(ftype) == ".txt":
                try:
                    f = codecs.open(fname, mode='rU', encoding="GBK")
                    f.readline()
                    f.close()
                except:
                    a = 1
                else:
                    self.encoding="GBK"

                try:
                    f = codecs.open(fname, mode='rU', encoding="GB2312")
                    f.readline()
                    f.close()
                except:
                    a = 1
                else:
                    self.encoding="GB2312"

                try:
                    f = codecs.open(fname, mode='rU', encoding="UTF-8")
                    f.readline()
                    f.close()
                except:
                    a = 1
                else:
                    self.encoding="UTF-8"

            if len(res) == 0:

                if str.lower(ftype) == ".txt":
                    with codecs.open(fname, mode='rb') as f:
                        self.book_data = f.readlines()
                        count =len(self.book_data)
                        f.close()

                    b1 = []
                    b2 = []
                    b3 = []
                    for index, sb in enumerate(self.book_data):
                        try:
                            lines = bytes.decode(sb, encoding=self.encoding)
                        except:
                            lines = "\r\n"

                        if len(lines) <= 50:

                            matchObj1 = re.match(r"[\s]*?第.*?[章|回](.*)",lines)
                            if matchObj1:
                                t = {}
                                t["title"] = lines
                                t["line"] = index
                                b1.append(t)

                            matchObj2 = re.match(r"\b[一二三四五六七八九百千万]\s.*?", lines)
                            if matchObj2:
                                t = {}
                                t["title"] = lines
                                t["line"] = index
                                b2.append(t)

                            matchObj3 = re.match(r"Chapter\s[0-9]+", lines)
                            if matchObj3:
                                t = {}
                                t["title"] = lines
                                t["line"] = index
                                b3.append(t)

                    #取最长的一组
                    maxlen = max( len(b1) , len(b2)  , len(b3))
                    if len(b1) == maxlen: self.mBookMenu = b1
                    if len(b2) == maxlen: self.mBookMenu = b2
                    if len(b3) == maxlen: self.mBookMenu = b3

                    sqlInsBook = "insert into book_list( book_name,readlines, alllines, book_index, book_location) values('{}',{},{},'{}','{}')" \
                        .format(fshortname, 0, count, json.dumps(self.mBookMenu)  ,fname)
                    self.conn.execute(sqlInsBook)
                    self.conn.commit()

                if str.lower(ftype) == ".pdf" or str.lower(ftype) == ".epub":
                    doc = fitz.open(fname)

                    count = doc.pageCount

                    self.mBookMenu = []
                    i = 0
                    while i<count:
                        t = {}
                        t["title"] = "Page" + str(i)
                        t["line"] = i
                        self.mBookMenu.append(t)
                        i+=1

                    sqlInsBook = "insert into book_list( book_name,readlines, alllines, book_index, book_location) values('{}',{},{},'{}','{}')" \
                        .format(fshortname, 0, count, json.dumps(self.mBookMenu)  ,fname)
                    self.conn.execute(sqlInsBook)
                    self.conn.commit()

                if str.lower(ftype) == ".zip":
                    z = zipfile.ZipFile(fname, "r")

                    self.mBookMenu = []
                    count = 0
                    for zip_filename in z.namelist():
                        t = {}
                        t["title"] = zip_filename
                        t["line"] = count
                        self.mBookMenu.append(t)
                        count += 1

                    sqlInsBook = "insert into book_list( book_name,readlines, alllines, book_index, book_location) values('{}',{},{},'{}','{}')" \
                        .format(fshortname, 0, count, json.dumps(self.mBookMenu), fname)
                    self.conn.execute(sqlInsBook)
                    self.conn.commit()

                self.mFname = fshortname
                self.mFullname = fname
                self.mLines = 0
                self.mAllLines = count
                self.mFtype = ftype
                self.mLines_prev = 0
            else:
                with codecs.open(fname, mode='rb') as f:
                    self.book_data = f.readlines()
                    f.close()

                self.mFname = res[0][1]
                self.mLines = res[0][2]
                self.mAllLines = res[0][3]
                self.mBookMenu = json.loads(res[0][4])
                self.mFullname = res[0][5]
                self.mFtype = ftype
                self.mLines_prev = self.mLines - 20 if self.mLines - 20 > 0 else 0

            self.loadBook(self.mLines)
        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def readConfig(self, key ):
        try:
            sql = "select cfg_key, cfg_value from g30pconfig where cfg_key='{}'".format(key)
            data = self.conn.execute(sql)
            r = data.fetchall()

            if len(r) == 0:
                sql2 = "insert into g30pconfig(cfg_key, cfg_value) values('{}',{})".format(key, "NULL")
                self.conn.execute(sql2)
                self.conn.commit()
                return ""
            else:
                return r[0][1]
        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def writeConfig(self, key, value):
        try:
            sql = "update g30pconfig set cfg_value='{}' where cfg_key='{}'".format(value, key)
            self.conn.execute(sql)
            self.conn.commit()

        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def writeLines(self , bookName, line):
        try:
            sql = "update book_list set readlines={} where book_name='{}'".format(line, bookName)
            self.conn.execute(sql)
            self.conn.commit()
        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))



    def initDBCfg(self):
        sqlCheck = "select count(*) from sqlite_master where type='table' and name='g30pconfig'"
        cursorCheck = self.conn.execute(sqlCheck)

        countCheck = 0
        for row in cursorCheck:
            countCheck = int(row[0])

        if countCheck == 0:
            sqlTable = """
                CREATE TABLE g30pconfig (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                        cfg_key text , cfg_value text)
                 """
            self.conn.execute(sqlTable)



    def initDBBookList(self):
        sqlCheck = "select count(*) from sqlite_master where type='table' and name='book_list'"
        cursorCheck = self.conn.execute(sqlCheck)

        countCheck = 0
        for row in cursorCheck:
            countCheck = int(row[0])

        if countCheck == 0:
            sqlTable = """
                CREATE TABLE book_list (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                        book_name text , readlines int, alllines int , book_index text, book_location TEXT)
                 """
            self.conn.execute(sqlTable)




    def initDBBookDetail(self):
        sqlCheck = "select count(*) from sqlite_master where type='table' and name='book_detail'"
        cursorCheck = self.conn.execute(sqlCheck)

        countCheck = 0
        for row in cursorCheck:
            countCheck = int(row[0])

        if countCheck == 0:
            sqlTable = """
                CREATE TABLE book_detail (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                        p_name text , mark_index text , mark_down text, mark_title text)
                 """
            self.conn.execute(sqlTable)


    def loadBook(self, firstlines):
        try:
            if self.mFullname == "" or self.mFullname == None: return
            if firstlines > self.mAllLines: return

            self.loadMark()

            self.mLines_begin = self.mLines
            self.mLines = firstlines

            if str.lower(self.mFtype) == ".txt":
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.txtMain.setStyleSheet(self.mReadStyle)

                self.ui.page_1.show()
                self.ui.txtMain.clear()

                continue_mark = True
                index = firstlines
                rows = 0
                lastLine = ""
                while continue_mark:
                    try:
                        lines = bytes.decode( self.book_data[index], encoding= self.encoding)
                        lines = lines.replace("\r","")
                        lines = lines.replace("\n", "")
                    except:
                        lines = "\r\n"

                    for i in self.checkMark(lines):
                        sNode = str(i[2]).encode(encoding="utf-8")
                        lines = lines.replace(i[4], i[4] + "[markId:{}]".format(i[0]))

                    if  (lines.isspace() and lastLine.isspace()) == False:
                        lines = lines.replace("\n", "")
                        self.ui.txtMain.append(lines)
                        lastLine = lines

                    firstlines += 1
                    index += 1
                    rows += 1

                    if self.ui.txtMain.verticalScrollBar().maximum() > 0:
                        strtmp = self.ui.txtMain.toPlainText().split("\n")
                        strtmp = strtmp[0: -3]


                        htmlstr = "<html>"
                        for s in strtmp:
                            s = re.sub(r"\[markId:(.*?)\]" , r"<a href='mark:\1'>[批]</a>" , s)
                            htmlstr += s + "<br/>"
                        htmlstr += "</html>"

                        self.ui.txtMain.clear()
                        self.ui.txtMain.setHtml(htmlstr)

                        firstlines -= 2 if rows > 2 else 0
                        continue_mark = False

                        self.mLines_end = firstlines
                        self.statusMessage.setText("{} ({}/{})".format(self.mFname, self.mLines, self.mAllLines))
                        self.statusHelp.setText("选中文字，右键增加批注； F12快速关闭 ")

            if str.lower(self.mFtype) == ".pdf":
                self.ui.stackedWidget.setCurrentIndex(1)
                self.scene.clear()

                doc = fitz.open(self.mFullname)
                self.book_data = doc

                firstPage = firstlines - 4 if firstlines - 4 > 0 else 0
                maxline = firstlines + 5 if firstlines + 5 <= self.mAllLines else self.mAllLines

                page = self.book_data.loadPage(firstPage)

                trans = fitz.Matrix(self.mPdfResize, self.mPdfResize).prerotate(0)
                pix = page.getPixmap(matrix=trans, alpha=False)
                fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
                qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
                qpiximage = QPixmap.fromImage(qimage)

                self.scene.addPixmap(qpiximage)

                for markrow, markData in enumerate(self.checkMark(firstPage)):
                    sNode = QPushButton(r"批注")
                    sNode.clicked.connect(partial(self.pdfShowMark,markData[0]))
                    objNode = self.scene.addWidget(sNode)
                    objNode.setPos(pix.width, markrow * 25)

                self.mViewHeight = self.ui.graphicsView.height()
                self.mPdfPageHeigh = pix.height

                if self.mPdfPageHeigh <= self.mViewHeight:
                    self.mPdfStepHeight = self.mPdfPageHeigh
                else:
                    self.mPdfStepHeight = self.mViewHeight

                i = firstPage + 1
                while i <= maxline:
                    page = self.book_data.loadPage(i)

                    trans = fitz.Matrix(self.mPdfResize, self.mPdfResize).prerotate(0)
                    pix = page.getPixmap(matrix=trans, alpha=False)
                    fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
                    qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
                    qpiximage = QPixmap.fromImage(qimage)

                    obj = self.scene.addPixmap(qpiximage)

                    locationpageX = 0
                    locationpageY = 0
                    if i % 2 == 0:
                        if pix.height <= self.mViewHeight:
                            locationpageY = pix.height * int(i / 2)
                        else:
                            locationpageY = pix.height * i
                    else:
                        if pix.height <= self.mViewHeight:
                            locationpageX = pix.width
                            locationpageY = pix.height * int(i / 2)
                        else:
                            locationpageY = pix.height * i

                    obj.setPos(locationpageX, locationpageY)

                    for markrow, markData in enumerate(self.checkMark(i)):
                        sNode = QPushButton(r"批注")
                        sNode.clicked.connect(partial(self.pdfShowMark, markData[0]))
                        objNode = self.scene.addWidget(sNode)
                        objNode.setPos(locationpageX + pix.width, locationpageY - pix.height +  markrow * 25)

                    i += 1

                self.mLines_end = maxline
                self.mLines_begin = firstPage

                self.ui.graphicsView.setScene(self.scene)
                # self.ui.graphicsView.verticalScrollBar().maximum()
                self.ui.graphicsView.verticalScrollBar().setValue(firstlines * self.mPdfPageHeigh - self.mViewHeight - self.mViewHeight)

                self.statusMessage.setText("{} ({}/{})".format(self.mFname,  str(self.mLines_begin) + "-"
                                                               + str(self.mLines_end) +" " + str(self.mLines), self.mAllLines))
                self.statusHelp.setText("+-缩放，左右翻页，右键批注，F12快速关闭 ")

            if str.lower(self.mFtype) == ".zip":
                self.ui.stackedWidget.setCurrentIndex(1)
                self.scene.clear()

                z = zipfile.ZipFile(self.mFullname)
                self.book_data = z

                bmp_name = z.namelist()[self.mLines - 1]
                bmp_type = str.lower(os.path.splitext(bmp_name)[1])

                if bmp_type != ".bmp" and bmp_type != ".jpeg" and bmp_type != ".jpg" and bmp_type != ".jpeg":
                    self.mLines_prev = self.mLines
                    self.mLines += 1
                    self.loadBook(self.mLines)
                    return

                content = z.read(bmp_name)
                img = cv2.imdecode( numpy.array(bytearray(content)), cv2.COLOR_RGBA2BGR)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                height, width = img.shape[:2]
                size = (int(width * self.mImageResize), int(height *  self.mImageResize))
                img = cv2.resize(img , size)

                qimage = QImage(img[:],img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
                qimage2 = QPixmap.fromImage(qimage)

                #image = QImage.fromData(content)

                # image = image((newwidth, newheight), Image.ANTIALIAS)

                #qimage2 =QPixmap.fromImage(image)

                self.scene = QGraphicsScene()
                o = self.scene.addPixmap(qimage2)
                o.setFlags(QGraphicsItem.ItemIsMovable)

                self.mImageXStep = size[0] / 100
                self.mImageYStep = size[1] / 100

                self.ui.graphicsView.setScene(self.scene)

                self.mLines_end = firstlines
                self.statusMessage.setText("{} ({}/{})".format(self.mFname, self.mLines, self.mAllLines))
                self.statusHelp.setText("+-缩放")

            self.writeConfig("LAST_READ", self.mFname)
            self.writeLines(self.mFname, self.mLines)


        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def postLoad(self):
        try:
            stmp = self.readConfig("LAST_READ")
            if stmp != "" and stmp != None:
                self.mFname = stmp

                sql = "select * from book_list where book_name = '{}'".format(stmp)
                resCure = self.conn.execute(sql)
                res = resCure.fetchall()

                if len(res) > 0:
                    self.mLines = res[0][2]
                    self.mAllLines = res[0][3]
                    self.mBookMenu = json.loads(res[0][4])
                    self.mFullname = fname = res[0][5]
                    self.mFtype = os.path.splitext(self.mFullname)[1]
                    self.mLines_prev = self.mLines - 20 if self.mLines - 20 > 0 else 0

                    if str.lower(self.mFtype) == ".txt":
                        stmp = self.readConfig("READ_STYLE")
                        if stmp != "" and stmp != None:
                            self.mReadStyle = stmp
                        else:
                            self.writeConfig("READ_STYLE", self.mReadStyle)

                        self.ui.txtMain.setStyleSheet(self.mReadStyle)

                        try:
                            f = codecs.open(fname, mode='rU', encoding="GBK")
                            f.readline()
                            f.close()
                        except:
                            a = 1
                        else:
                            self.encoding = "GBK"

                        try:
                            f = codecs.open(fname, mode='rU', encoding="GB2312")
                            f.readline()
                            f.close()
                        except:
                            a = 1
                        else:
                            self.encoding = "GB2312"

                        try:
                            f = codecs.open(fname, mode='rU', encoding="UTF-8")
                            f.readline()
                            f.close()
                        except:
                            a = 1
                        else:
                            self.encoding = "UTF-8"

                        with codecs.open(fname, mode='rb') as f:
                            self.book_data = f.readlines()
                            count = len(self.book_data)
                            f.close()

                    if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
                        self.book_data = fitz.open(fname)
                        #count = self.book_data.pageCount

                    self.loadBook(self.mLines)
        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def listMenu(self):
        try:
            dialist = dialoglist_c(self)
            lr = dialist.exec()
        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def markdown(self):
        try:

            if str.lower(self.mFtype) == ".txt":
                tc = self.ui.txtMain.textCursor()
                s = str(tc.selectedText())

                tc.select(QTextCursor.LineUnderCursor)
                s2 = str(tc.selectedText())
                s2 = s2.replace("[批]","")

                if s.isspace() : return
                s = s.split("\n")[-1]

                dialogmarkdown = dialogmarkdown_c(self, s , s2)
                dialogmarkdown.exec()

            if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub":
                dialogmarkdown = dialogmarkdown_c(self, str(self.mLines) , self.mFname)
                dialogmarkdown.exec()

        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def saveMark(self, s, title , mark_index):
        try:
            title = title.replace("'","")
            title = title.replace("\"", "")

            sql = """insert into book_detail (p_name, mark_index, mark_down,mark_title) values ('{}','{}','{}','{}')"""\
                .format(self.mFname , mark_index, s , title )

            self.conn.execute(sql)
        except Exception as ex:
            traceback.print_exc()
            self.showError(ex)


    def checkMark(self , sblock):
        if str.lower(self.mFtype) == ".txt":
            ll = []
            for i in self.mMark_data:
                if sblock.find(i[2]) >= 0:
                    ll.append(i)
            return ll

        if str.lower(self.mFtype) == ".pdf" or str.lower(self.mFtype) == ".epub" :
            ll = []
            for i in self.mMark_data:
                if str(i[4]) == str(sblock):
                    ll.append(i)
            return ll


    def loadMark(self):
        try:
            sql = """select id, p_name, mark_index, mark_down,mark_title from book_detail where p_name = '{}'"""\
                .format(self.mFname)

            lr = self.conn.execute(sql)

            if lr:
                self.mMark_data.clear()
                self.mMark_data = lr.fetchall()
        except Exception as ex:
            traceback.print_exc()
            self.showError(ex)


    def showError(self, sMessage):
        self.statusHelp.setText("Error: " + str(sMessage))


    def copySelected(self):
        pyperclip.copy(self.ui.txtMain.textCursor().selectedText())

    def openSearch(self):
        try:
            if str.lower(self.mFtype) == ".txt":
                dialist = dialogsearch_c.dialogsearch_c(self)
                lr = dialist.exec()
        except Exception as ex:
            traceback.print_exc()
            self.showError(str(ex))


    def search(self, str ,beginline = -1) :
        if str.lower(self.mFtype) == ".txt":
            if beginline == -1:
                for i, s  in enumerate(self.book_data):

                    try:
                        s = bytes.decode( s, encoding= self.encoding)
                    except:
                        s = ""

                    if i >= self.mLines_begin:

                        if s.find(str) >= 0:
                            self.mLines = i
                            self.loadBook(i)
                            self.mLines_prev = i -10 if i - 10 > 0 else 0
                            return self.mLines_begin
                return -1
            else:
                for i, s  in enumerate(self.book_data):
                    try:
                        s = bytes.decode( s, encoding= self.encoding)
                    except:
                        s = ""

                    if i >= beginline:
                       if s.find(str) >=0:
                            self.mLines = i
                            self.loadBook(i)
                            self.mLines_prev = i -10 if i - 10 >0 else 0
                            return self.mLines_begin
                return -1


    def readMark(self, id):
        try:
            sql = """Select * from book_detail where id = {}""".format(id)
            res = self.conn.execute(sql)

            data = res.fetchall()

            if len(data) == 1:
                return data[0]
            else:
                return None

        except Exception as ex:
            traceback.print_exc()
            self.showError(ex)


    def openCfg(self):
        if str.lower(self.mFtype) == ".txt":
            dlg = dialogcfg_c(self)
            dlg.exec()


    def pdfShowMark(self,id):
        diag = dialogshowmd_c(self, id)
        diag.exec()


    def scene_wheelEvent(self, event):
        angle = event.angleDelta()

        self.showError("000--" + str(angle))

        v = 0
        if angle.y() > 0:
            v = self.mImageResize + 0.1
            if v > 2.5: v = 2.5
        else:
            v = self.mImageResize - 0.1
            if v < 0.5: v = 0.5

        self.mImageResize = v
        self.writeConfig("ImageResize", self.mImageResize)
        self.loadBook(self.mLines)

    def resource_path(self,relative_path):
        if getattr(sys, 'frozen', False): #是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
