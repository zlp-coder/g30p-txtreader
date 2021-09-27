g30p阅读器
==
Txt小说阅读器,不联网，没有广告，简单的自用版本。

* 支持Txt阅读，PDF阅读，左右键盘翻页
* Txt的阅读界面支持 Style 配置
* 支持浏览 zip 包中的文件，可以用来看漫画 
* 自动记录阅读进度
* 支持批注


![](https://github.com/zlp-coder/g30p-txtreader/blob/main/ui-demo.jpg)

Install
==
Win7 64位打包：
[下载](https://github.com/zlp-coder/g30p-txtreader/blob/main/g30p-txtreader.zip)

Technologies
==
* python3
* pyqt5 
* sqlite

启动脚本 g30p-txtreader.py

工程使用 Pychram 编写，python环境在根目录 env\下（太大没有上传）。

Pyinstaller 打包，打包后的Exe在 g30p-txtreader.zip

UI 使用 Qt Creator 4.3 设计，Qt工程在 g30p-txtreader-ui\目录下。设计完成的界面使用Pyuic工具转成Python类。配置方式：

```java
Program：g30p-txtreader\env\Scripts\python.exe
Argument：-m PyQt5.uic.pyuic $FileName$ -o ../$FileNameWithoutExtension$.py
Working directory：$FileDir$
```

Interpreter
==

* PyMuPDF	1.18.17	1.18.19
* PyQt5	5.15.4	5.15.4
* PyQt5-Qt5	5.15.2	
* PyQt5-sip	12.9.0	12.9.0
* altgraph	0.17.2	
* coverage	5.5	
* future	0.18.2	
* importlib-metadata	4.8.1	
* numpy	1.21.2	
* opencv-python	4.5.3.56	
* pefile	2021.9.3	
* pip	21.2.4	
* pyinstaller	4.5.1	
* pyinstaller-hooks-contrib	2021.3	
* pymupdf-fonts	1.0.3	
* pyperclip	1.8.2	
* pywin32-ctypes	0.2.0	
* setuptools	58.0.4	
* typing-extensions	3.10.0.2	
* zipp	3.5.0	




