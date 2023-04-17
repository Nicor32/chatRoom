import server_window
import server_back
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
import sys


class MyWindow(QMainWindow, server_window.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.Button_start.clicked.connect(self.run_server)

    def run_server(self):
        self.Text_chat.append("服务器已启动")
        server_ins = server_back.Server('localhost', 8888)
        server_ins.run()
        self.Text_chat.append("交互完成")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
