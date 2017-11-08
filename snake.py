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
            self.startButton.clicked.connect(self.on_click)
            self.resetButton.clicked.connect(self.on_click)

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

            self.buttonGroup = QButtonGroup(self)
            self.buttonGroup.addButton(self.b00)
            self.buttonGroup.addButton(self.b01)
            self.buttonGroup.addButton(self.b02)
            self.buttonGroup.addButton(self.b03)
            self.buttonGroup.addButton(self.b10)
            self.buttonGroup.addButton(self.b11)
            self.buttonGroup.addButton(self.b12)
            self.buttonGroup.addButton(self.b13)
            self.buttonGroup.addButton(self.b20)
            self.buttonGroup.addButton(self.b21)
            self.buttonGroup.addButton(self.b22)
            self.buttonGroup.addButton(self.b23)
            self.buttonGroup.addButton(self.b30)
            self.buttonGroup.addButton(self.b31)
            self.buttonGroup.addButton(self.b32)
            self.buttonGroup.addButton(self.b33)

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

            for button in self.buttonGroup.buttons():
                button.resize(25,25)
                button.clicked.connect(self.on_click)
                
        for button in self.buttonGroup.buttons():
            button.setStyleSheet('background-color: white; color: white}')
            button.setEnabled(True)
        self.b11.setStyleSheet('background-color: green; color: green}')
        self.b12.setStyleSheet('background-color: green; color: green}')
        self.b11.setEnabled(False)
        self.b12.setEnabled(False)

    def initStats(self):
        if(self.isReset == False):
            self.stats = QLineEdit(self)
            self.status = QLineEdit(self)
            self.stats.move(10, 90)
            self.stats.resize(100, 300)
            self.status.move(300, 10)
            self.status.resize(300, 30)
            self.status.setEnabled(False)
            self.stats.setEnabled(False)
            self.status.setStyleSheet('background-color: white; color: black}')
            self.stats.setStyleSheet('background-color: white; color: black}')

        self.status.setText("Press Start to Play")
        self.stats.setText("Food Eaten: 0")
 
    def initUI(self):
        self.setWindowTitle('Snake Team1')
        self.setGeometry(10, 10, 800, 500)
        self.isReset = False
        self.resetUI()
        self.isReset = True
        self.show()

    def resetUI(self):
        self.x = 400
        self.y = 150
        self.lastMove = ['LEFT', 'UP']
        self.timer = QBasicTimer()
        self.bodyLength = 100
        self.foodEaten = 0
        self.snakeArray = [[self.x, self.y],
                           [self.x+ 25, self.y],
                           [self.x + 50, self.y],
                           [self.x + 75, self.y],
                           [self.x + 100, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = False
        self.isOver = False
        self.speed = 400
        self.nodeCheck = False
        self.isPaused = True
        self.isStart = False
        self.isFood = False
        self.isEat = False
        self.isGrow = False

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
        if(self.isGrow == True):    # handle snake body growth/deletion
            if(self.count == 3):
                self.isGrow = False
            else:
                self.count += 1
        else:     
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
        qp.setBrush(QColor(Qt.darkGreen))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], 25, 25)

    def checkOverlap(self):
        for button in self.buttonGroup.buttons():
            self.isOverlap = False
            print(len(self.snakeArray))
            for node in self.snakeArray:
                if(button.x() == node[0] and button.y() == node[1]):
                    button.setStyleSheet('background-color: green; color: green}')
                    self.isOverlap = True
                    button.setEnabled(False)
            if(self.isOverlap == False and (button.x() != self.foodx or button.y() != self.foody)):
                button.setStyleSheet('background-color: white; color: white}')
                button.setEnabled(True)

    def onEat(self):
        self.status.setText("Food was eaten")
        self.isPaused = True
        self.isFood = False
        self.isGrow = True
        self.count = 0
        self.foodEaten += 1
        self.stats.setText("Food Eaten: " + str(self.foodEaten))

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if(self.isFood == False):   # wait for food
                self.status.setText("Place food at an intersection")
            if(self.isPaused == False):
                self.status.setText("Game is in play")
                if(self.nodeCheck == False):    # head at a button
                    self.tempx = self.x
                    self.tempy = self.y
                    self.nodeCheck = True
                    if(self.x == self.foodx and self.y == self.foody):  # snake head is at food
                        self.onEat()
                if(len(self.lastMove) != 0):    # check if move has completed
                    if(self.lastMove[0] == 'LEFT'):
                        if(self.x == (self.tempx - self.bodyLength)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    elif(self.lastMove[0] == 'RIGHT'):
                        if(self.x == (self.tempx + self.bodyLength)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    elif(self.lastMove[0] == 'UP'):
                        if(self.y == (self.tempy - self.bodyLength)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    elif(self.lastMove[0] == 'DOWN'):
                        if(self.y == (self.tempy + self.bodyLength)):
                            if(len(self.lastMove) != 0):
                                self.lastMove.pop(0)
                                self.nodeCheck = False
                        else:
                            self.movement(self.lastMove)
                            self.repaint()
                    self.checkOverlap()
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
                self.setButtonData()
                self.b00.setStyleSheet('background-color: red; color: red}')
                self.foodx = 300
                self.foody = 50
            elif self.sender().text() == 'b01':
                self.handler.uiData = '01'
                self.setButtonData()
                self.b01.setStyleSheet('background-color: red; color: red}')
                self.foodx = 400
                self.foody = 50
            elif self.sender().text() == 'b02':
                self.handler.uiData = '02'
                self.setButtonData()
                self.b02.setStyleSheet('background-color: red; color: red}')
                self.foodx = 500
                self.foody = 50
            elif self.sender().text() == 'b03':
                self.handler.uiData = '03'
                self.setButtonData()
                self.b03.setStyleSheet('background-color: red; color: red}')
                self.foodx = 600
                self.foody = 50
            elif self.sender().text() == 'b10':
                self.handler.uiData = '10'
                self.setButtonData()
                self.b10.setStyleSheet('background-color: red; color: red}')
                self.foodx = 300
                self.foody = 150
            elif self.sender().text() == 'b11':
                self.handler.uiData = '11'
                self.setButtonData()
                self.b11.setStyleSheet('background-color: red; color: red}')
                self.foodx = 400
                self.foody = 150
            elif self.sender().text() == 'b12':
                self.handler.uiData = '12'
                self.setButtonData()
                self.b12.setStyleSheet('background-color: red; color: red}')
                self.foodx = 500
                self.foody = 150
            elif self.sender().text() == 'b13':
                self.handler.uiData = '13'
                self.setButtonData()
                self.b13.setStyleSheet('background-color: red; color: red}')
                self.foodx = 600
                self.foody = 150
            elif self.sender().text() == 'b20':
                self.handler.uiData = '20'
                self.setButtonData()
                self.b20.setStyleSheet('background-color: red; color: red}')
                self.setButtonData()
                self.foodx = 300
                self.foody = 250
            elif self.sender().text() == 'b21':
                self.handler.uiData = '21'
                self.setButtonData()
                self.b21.setStyleSheet('background-color: red; color: red}')
                self.foodx = 400
                self.foody = 250
            elif self.sender().text() == 'b22':
                self.handler.uiData = '22'
                self.setButtonData()
                self.b22.setStyleSheet('background-color: red; color: red}')
                self.foodx = 500
                self.foody = 250
            elif self.sender().text() == 'b23':
                self.handler.uiData = '23'
                self.setButtonData()
                self.b23.setStyleSheet('background-color: red; color: red}')
                self.foodx = 600
                self.foody = 250
            elif self.sender().text() == 'b30':
                self.handler.uiData = '30'
                self.setButtonData()
                self.b30.setStyleSheet('background-color: red; color: red}')
                self.foodx = 300
                self.foody = 350
            elif self.sender().text() == 'b31':
                self.handler.uiData = '31'
                self.setButtonData()
                self.b31.setStyleSheet('background-color: red; color: red}')
                self.foodx = 400
                self.foody = 350
            elif self.sender().text() == 'b32':
                self.handler.uiData = '32'
                self.setButtonData()
                self.b32.setStyleSheet('background-color: red; color: red}')
                self.foodx = 500
                self.foody = 350
            elif self.sender().text() == 'b33':
                self.handler.uiData = '33'
                self.setButtonData()
                self.b33.setStyleSheet('background-color: red; color: red}')
                self.foodx = 600
                self.foody = 350

    def setButtonData(self):
        self.handler.isUIData = True
        self.isFood = True
        self.isPaused = False
                
    @pyqtSlot(str)
    def dataReceive(self, letter):
        #self.stats.setText(letter)
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
