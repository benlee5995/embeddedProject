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
        if(self.isReset == False):
            self.startButton = QPushButton('Start', self) 
            self.resetButton = QPushButton('Reset', self)

            self.b00 = QPushButton('b00', self)
            self.b01 = QPushButton('b01', self)
            self.b02 = QPushButton('b02', self)
            self.b03 = QPushButton('b03', self)
            self.b10 = QPushButton('b10', self)
            self.b11 = QPushButton('b11', self)
            self.b12 = QPushButton('b12', self)
            self.b13 = QPushButton('b13', self)
            self.b20 = QPushButton('b20', self)
            self.b21 = QPushButton('b21', self)
            self.b22 = QPushButton('b22', self)
            self.b23 = QPushButton('b23', self)
            self.b30 = QPushButton('b30', self)
            self.b31 = QPushButton('b31', self)
            self.b32 = QPushButton('b32', self)
            self.b33 = QPushButton('b33', self)

            self.startButton.move(10,10)
            self.resetButton.move(10,50)
            self.b00.move(300,50)
            self.b01.move(400,50)
            self.b02.move(500,50)
            self.b03.move(600,50)
            self.b10.move(300,150)
            self.b11.move(400,150)
            self.b12.move(500,150)
            self.b13.move(600,150)
            self.b20.move(300,250)
            self.b21.move(400,250)
            self.b22.move(500,250)
            self.b23.move(600,250)
            self.b30.move(300,350)
            self.b31.move(400,350)
            self.b32.move(500,350)
            self.b33.move(600,350)

            self.b00.resize(25,25)
            self.b01.resize(25,25)
            self.b02.resize(25,25)
            self.b03.resize(25,25)
            self.b10.resize(25,25)
            self.b11.resize(25,25)
            self.b12.resize(25,25)
            self.b13.resize(25,25)
            self.b20.resize(25,25)
            self.b21.resize(25,25)
            self.b22.resize(25,25)
            self.b23.resize(25,25)
            self.b30.resize(25,25)
            self.b31.resize(25,25)
            self.b32.resize(25,25)
            self.b33.resize(25,25)

            self.startButton.clicked.connect(self.on_click)
            self.resetButton.clicked.connect(self.on_click)
            self.b00.clicked.connect(self.on_click)
            self.b01.clicked.connect(self.on_click)
            self.b02.clicked.connect(self.on_click)
            self.b03.clicked.connect(self.on_click)
            self.b10.clicked.connect(self.on_click)
            self.b11.clicked.connect(self.on_click)
            self.b12.clicked.connect(self.on_click)
            self.b13.clicked.connect(self.on_click)
            self.b20.clicked.connect(self.on_click)
            self.b21.clicked.connect(self.on_click)
            self.b22.clicked.connect(self.on_click)
            self.b23.clicked.connect(self.on_click)
            self.b30.clicked.connect(self.on_click)
            self.b31.clicked.connect(self.on_click)
            self.b32.clicked.connect(self.on_click)
            self.b33.clicked.connect(self.on_click)

        self.b00.setStyleSheet('background-color: white; color: white}')
        self.b01.setStyleSheet('background-color: white; color: white}')
        self.b02.setStyleSheet('background-color: white; color: white}')
        self.b03.setStyleSheet('background-color: white; color: white}')
        self.b10.setStyleSheet('background-color: white; color: white}')
        self.b11.setStyleSheet('background-color: white; color: white}')
        self.b12.setStyleSheet('background-color: white; color: white}')
        self.b13.setStyleSheet('background-color: white; color: white}')
        self.b20.setStyleSheet('background-color: white; color: white}')
        self.b21.setStyleSheet('background-color: white; color: white}')
        self.b22.setStyleSheet('background-color: white; color: white}')
        self.b23.setStyleSheet('background-color: white; color: white}')
        self.b30.setStyleSheet('background-color: white; color: white}')
        self.b31.setStyleSheet('background-color: white; color: white}')
        self.b32.setStyleSheet('background-color: white; color: white}')
        self.b33.setStyleSheet('background-color: white; color: white}')

    def initStats(self):
        if(self.isReset == False):
            self.stats = QLineEdit(self)
            self.status = QLineEdit(self)
            self.stats.move(10, 90)
            self.stats.resize(100, 300)
            self.status.move(300, 10)
            self.status.resize(300, 30)
            self.status.setEnabled(False)

        self.status.setText("Press Start to Play")
        self.stats.setText("stats")
 
    def initUI(self):
        self.setWindowTitle('Snake Team1')
        self.setGeometry(10, 10, 800, 500)

        self.x = 400
        self.y = 150
        self.lastMove = ['LEFT', 'UP']
        self.timer = QBasicTimer()
        self.snakeArray = [[self.x, self.y], [self.x+ 25, self.y], [self.x + 50, self.y], [self.x + 75, self.y], [self.x + 100, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = False
        self.isOver = False
        self.speed = 800
        self.nodeCheck = False
        self.isPaused = True
        self.isStart = False
        self.isFood = False
        self.isReset = False
        
        self.initButtons()
        self.initStats()

        self.show()

    def resetUI(self):
        self.x = 400
        self.y = 150
        self.lastMove = ['LEFT', 'UP']
        self.timer = QBasicTimer()
        self.snakeArray = [[self.x, self.y], [self.x+ 25, self.y], [self.x + 50, self.y], [self.x + 75, self.y], [self.x + 100, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = False
        self.isOver = False
        self.speed = 800
        self.nodeCheck = False
        self.isPaused = True
        self.isStart = False
        self.isFood = False
        self.isReset = True

        self.initButtons()
        self.initStats()

        self.update()

    def start(self):
        if(self.isStart == False):
            self.startButton.isEnabled = False
            self.isStart = True
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
        if(move[0] == "UP"):
            self.y -= 25
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])
        elif (move[0] == "DOWN"):
            self.y += 25
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])
        elif (move[0] == "LEFT"):
            self.x -= 25
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])
        elif (move[0] == "RIGHT"):
            self.x += 25
            self.repaint()
            self.snakeArray.insert(0,[self.x, self.y])

    def drawSnake(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(Qt.green))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], 25, 25)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if(self.isFood == False):
                self.status.setText("Place food at an intersection")
            if(self.isPaused == False):
                self.status.setText("Game is in play")
                if(self.nodeCheck == False):
                    self.tempx = self.x
                    self.tempy = self.y
                    self.nodeCheck = True
                if(len(self.lastMove) != 0):
                    if(self.lastMove[0] == 'LEFT'):
                        if(self.x == (self.tempx - 100)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    elif(self.lastMove[0] == 'RIGHT'):
                        if(self.x == (self.tempx + 100)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    elif(self.lastMove[0] == 'UP'):
                        if(self.y == (self.tempy - 100)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    elif(self.lastMove[0] == 'DOWN'):
                        if(self.y == (self.tempy + 100)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
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
            self.isPaused = True
            self.handler.uiData = 'R'
            self.handler.isUIData = True
            self.resetUI()
        if(self.isStart == True and self.isFood == False) and self.isPaused == True:
            if self.sender().text() == 'b00':
                self.handler.uiData = '00'
                self.handler.isUIData = True
                self.b00.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b01':
                self.handler.uiData = '01'
                self.handler.isUIData = True
                self.b01.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b02':
                self.handler.uiData = '02'
                self.handler.isUIData = True
                self.b02.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b03':
                self.handler.uiData = '03'
                self.handler.isUIData = True
                self.b03.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b10':
                self.handler.uiData = '10'
                self.handler.isUIData = True
                self.b10.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b11':
                self.handler.uiData = '11'
                self.handler.isUIData = True
                self.b11.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b12':
                self.handler.uiData = '12'
                self.handler.isUIData = True
                self.b12.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b13':
                self.handler.uiData = '13'
                self.handler.isUIData = True
                self.b13.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b20':
                self.handler.uiData = '20'
                self.handler.isUIData = True
                self.b20.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b21':
                self.handler.uiData = '21'
                self.handler.isUIData = True
                self.b21.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b22':
                self.handler.uiData = '22'
                self.handler.isUIData = True
                self.b22.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b23':
                self.handler.uiData = '23'
                self.handler.isUIData = True
                self.b23.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b30':
                self.handler.uiData = '30'
                self.handler.isUIData = True
                self.b30.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b31':
                self.handler.uiData = '31'
                self.handler.isUIData = True
                self.b31.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b32':
                self.handler.uiData = '32'
                self.handler.isUIData = True
                self.b32.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
            elif self.sender().text() == 'b33':
                self.handler.uiData = '33'
                self.handler.isUIData = True
                self.b33.setStyleSheet('background-color: red; color: red}')
                self.isFood = True
                self.isPaused = False
                
    @pyqtSlot(str)
    def dataReceive(self, letter):
        self.stats.setText(letter)
        if(letter == 'l'):
            self.lastMove.append('LEFT')
        elif(letter == 'u'):
            self.lastMove.append('UP')
        elif(letter == 'd'):
            self.lastMove.append('DOWN')
        elif(letter == 'r'):
            self.lastMove.append('RIGHT')
        elif(letter == 'p'):
            self.isPaused = True
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
