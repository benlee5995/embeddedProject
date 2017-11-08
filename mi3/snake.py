import sys
from communications import ComHandler
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):
    
    comSignal = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        # initialize variables
        self.title = 'Snake Team1'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 500
        self.initUI()

        # start communications on another thread
        self.handler = ComHandler()
        self.com_thread = QThread()
        self.handler.moveToThread(self.com_thread)
        self.com_thread.start()

        # connect signals and emit to start listening
        self.connectSignals()
        self.comSignal.emit()

    def connectSignals(self):
        self.register(self.handler.dataSignal)
        self.handler.registerListen(self.comSignal)
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # initialize buttons
        startButton = QPushButton('Start', self) 
        resetButton = QPushButton('Reset', self)

        startButton.move(10,10)
        resetButton.move(10,50)

        startButton.clicked.connect(self.on_click)
        resetButton.clicked.connect(self.on_click)

        # initialize line edit
        self.stats = QLineEdit(self)
        self.stats.setText("stats")
        self.stats.move(10, 90)
        self.stats.resize(100, 300)

        self.show()

    def register(self, mySignal):
        mySignal.connect(self.dataReceive)

    @pyqtSlot()
    def on_click(self):
        if self.sender().text() == 'Start':
            self.handler.uiData = 'S'
            self.handler.isUIData = True
            print('Start')
        elif self.sender().text() == 'Reset':
            self.handler.uiData = 'R'
            self.handler.isUIData = True
            print('Reset')

    @pyqtSlot(str)
    def dataReceive(self, letter):
        self.stats.setText(letter)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
