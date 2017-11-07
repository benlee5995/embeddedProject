import sys, random
from communications import ComHandler
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):
    
    comSignal = pyqtSignal()
    
    def __init__(self):
        super().__init__()

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
    
    def register(self, mySignal):
        mySignal.connect(self.dataReceive)

    def initButtons(self):
        startButton = QPushButton('Start', self) 
        resetButton = QPushButton('Reset', self)

        b00 = QPushButton('b00', self)
        b01 = QPushButton('b01', self)
        b02 = QPushButton('b02', self)
        b03 = QPushButton('b03', self)
        b10 = QPushButton('b10', self)
        b11 = QPushButton('b11', self)
        b12 = QPushButton('b12', self)
        b13 = QPushButton('b13', self)
        b20 = QPushButton('b20', self)
        b21 = QPushButton('b21', self)
        b22 = QPushButton('b22', self)
        b23 = QPushButton('b23', self)
        b30 = QPushButton('b30', self)
        b31 = QPushButton('b31', self)
        b32 = QPushButton('b32', self)
        b33 = QPushButton('b33', self)

        startButton.move(10,10)
        resetButton.move(10,50)
        b00.move(300,350)
        b01.move(300,250)
        b02.move(300,150)
        b03.move(300,50)
        b10.move(400,350)
        b11.move(400,250)
        b12.move(400,150)
        b13.move(400,50)
        b20.move(500,350)
        b21.move(500,250)
        b22.move(500,150)
        b23.move(500,50)
        b30.move(600,350)
        b31.move(600,250)
        b32.move(600,150)
        b33.move(600,50)

        b00.resize(15,15)
        b01.resize(15,15)
        b02.resize(15,15)
        b03.resize(15,15)
        b10.resize(15,15)
        b11.resize(15,15)
        b12.resize(15,15)
        b13.resize(15,15)
        b20.resize(15,15)
        b21.resize(15,15)
        b22.resize(15,15)
        b23.resize(15,15)
        b30.resize(15,15)
        b31.resize(15,15)
        b32.resize(15,15)
        b33.resize(15,15)

        b00.setStyleSheet('QPushButton{color: white}')
        b01.setStyleSheet('QPushButton{color: white}')
        b02.setStyleSheet('QPushButton{color: white}')
        b03.setStyleSheet('QPushButton{color: white}')
        b10.setStyleSheet('QPushButton{color: white}')
        b11.setStyleSheet('QPushButton{color: white}')
        b12.setStyleSheet('QPushButton{color: white}')
        b13.setStyleSheet('QPushButton{color: white}')
        b20.setStyleSheet('QPushButton{color: white}')
        b21.setStyleSheet('QPushButton{color: white}')
        b22.setStyleSheet('QPushButton{color: white}')
        b23.setStyleSheet('QPushButton{color: white}')
        b30.setStyleSheet('QPushButton{color: white}')
        b31.setStyleSheet('QPushButton{color: white}')
        b32.setStyleSheet('QPushButton{color: white}')
        b33.setStyleSheet('QPushButton{color: white}')

        startButton.clicked.connect(self.on_click)
        resetButton.clicked.connect(self.on_click)
        b00.clicked.connect(self.on_click)
        b01.clicked.connect(self.on_click)
        b02.clicked.connect(self.on_click)
        b03.clicked.connect(self.on_click)
        b10.clicked.connect(self.on_click)
        b11.clicked.connect(self.on_click)
        b12.clicked.connect(self.on_click)
        b13.clicked.connect(self.on_click)
        b20.clicked.connect(self.on_click)
        b21.clicked.connect(self.on_click)
        b22.clicked.connect(self.on_click)
        b23.clicked.connect(self.on_click)
        b30.clicked.connect(self.on_click)
        b31.clicked.connect(self.on_click)
        b32.clicked.connect(self.on_click)
        b33.clicked.connect(self.on_click)


    def initStats(self):
        self.stats = QLineEdit(self)
        self.stats.setText("stats")
        self.stats.move(10, 90)
        self.stats.resize(100, 300)
 
    def initUI(self):
        self.setWindowTitle('Snake Team1')
        self.setGeometry(10, 10, 800, 500)

        self.x = 300
        self.y = 350
        self.lastMove = 'RIGHT'
        self.timer = QBasicTimer()
        self.snakeArray = [[self.x, self.y], [self.x-12, self.y], [self.x-24, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = False
        self.isOver = False
        self.speed = 500
        
        self.initButtons()
        self.initStats()

        self.show()

    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawSnake(qp)


    def movement(self, move):
        self.snakeArray.pop()
        if(move == "UP"):
            print('up')
            self.y -= 12
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])
        elif (move == "DOWN"):
            self.y += 12
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])
        elif (move == "LEFT"):
            self.x -= 12
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])
        elif (move == "RIGHT"):
            self.x += 12
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])

    def drawSnake(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(255, 80, 0, 255))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], 12, 12)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.movement(self.lastMove)
            self.repaint()
        else:
            QFrame.timerEvent(self, event)
            
    @pyqtSlot()
    def on_click(self):
        print('onclick')
        if self.sender().text() == 'Start':
            self.handler.uiData = 'S'
            self.handler.isUIData = True
            print('start')
            # start game
            self.start()
        elif self.sender().text() == 'Reset':
            self.handler.uiData = 'R'
            self.handler.isUIData = True
        elif self.sender().text() == 'b00':
            print('00')
            self.handler.uiData = '00'
            self.handler.isUIData = True
        elif self.sender().text() == 'b01':
            self.handler.uiData = '01'
            self.handler.isUIData = True
        elif self.sender().text() == 'b02':
            self.handler.uiData = '02'
            self.handler.isUIData = True
        elif self.sender().text() == 'b03':
            self.handler.uiData = '03'
            self.handler.isUIData = True
        elif self.sender().text() == 'b10':
            self.handler.uiData = '10'
            self.handler.isUIData = True
        elif self.sender().text() == 'b11':
            self.handler.uiData = '11'
            self.handler.isUIData = True
        elif self.sender().text() == 'b12':
            self.handler.uiData = '12'
            self.handler.isUIData = True
        elif self.sender().text() == 'b13':
            self.handler.uiData = '13'
            self.handler.isUIData = True
        elif self.sender().text() == 'b20':
            self.handler.uiData = '20'
            self.handler.isUIData = True
        elif self.sender().text() == 'b21':
            self.handler.uiData = '21'
            self.handler.isUIData = True
        elif self.sender().text() == 'b22':
            self.handler.uiData = '22'
            self.handler.isUIData = True
        elif self.sender().text() == 'b23':
            self.handler.uiData = '23'
            self.handler.isUIData = True
        elif self.sender().text() == 'b30':
            self.handler.uiData = '30'
            self.handler.isUIData = True
        elif self.sender().text() == 'b31':
            self.handler.uiData = '31'
            self.handler.isUIData = True
        elif self.sender().text() == 'b32':
            self.handler.uiData = '32'
            self.handler.isUIData = True
        elif self.sender().text() == 'b33':
            self.handler.uiData = '33'
            self.handler.isUIData = True
            
    @pyqtSlot(str)
    def dataReceive(self, letter):
        self.stats.setText(letter)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
