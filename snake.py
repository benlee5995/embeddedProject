import sys, random
from communications import ComHandler
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from astar import *
import math

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
            #scoreboard
            self.scoreboard = QLabel('Scoreboard', self)
            self.scoreboard.move(10,200)
            
            self.f = QLabel('1.', self)
            self.f.move(10, 233)
            self.s = QLabel('2.', self)
            self.s.move(10, 263)
            self.t = QLabel('3.', self)
            self.t.move(10, 293)
            
            self.first = QLineEdit('Josh', self)
            self.first.move(25, 230)
            self.first.resize(125,25)
            self.first.setEnabled(False)

            self.sec = QLineEdit('Afsayh', self)
            self.sec.move(25, 260)
            self.sec.resize(125,25)
            self.sec.setEnabled(False)

            self.third = QLineEdit('Joey', self)
            self.third.move(25, 290)
            self.third.resize(125,25)
            self.third.setEnabled(False)

            self.firstScore = QLineEdit('2', self)
            self.firstScore.move(147, 230)
            self.firstScore.resize(25, 25)
            self.firstScore.setEnabled(False)
            self.secScore = QLineEdit('1', self)
            self.secScore.move(147, 260)
            self.secScore.resize(25, 25)
            self.secScore.setEnabled(False)
            self.thirdScore = QLineEdit('0', self)
            self.thirdScore.move(147, 290)
            self.thirdScore.resize(25, 25)
            self.thirdScore.setEnabled(False)


            #start reset buttons
            self.startButton = QPushButton('Start', self) 
            self.resetButton = QPushButton('Reset', self)
            self.startButton.resize(130, 30)
            self.resetButton.resize(130, 30)
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
            button.setStyleSheet('background-color: white; color: white')
            button.setEnabled(True)
        self.b11.setStyleSheet('background-color: green; color: green')
        self.b12.setStyleSheet('background-color: green; color: green')
        self.b11.setEnabled(False)
        self.b12.setEnabled(False)

    def initStats(self):
        if(self.isReset == False):
            self.stats = QLineEdit(self)
            self.status = QLineEdit(self)
            self.stats.move(10, 90)
            self.stats.resize(130, 100)
            self.status.move(300, 10)
            self.status.resize(450, 30)
            self.status.setEnabled(False)
            self.stats.setEnabled(False)
            self.status.setStyleSheet('background-color: white; color: black')
            self.stats.setStyleSheet('background-color: white; color: black')

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
        self.lastMove = []
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
        #self.speed = 1200
        self.speed = 50
        self.nodeCheck = False
        self.isPaused = True
        self.isStart = False
        self.isFood = False
        self.isEat = False
        self.isGrow = False
        self.prev = ['LEFT']
        self.forTail = ["1"]
        self.tori = "L"
        self.win = False

        self.initButtons()
        self.initStats()

        self.update()

    def start(self):
        #reinitialize scoreboard
        self.first.setEnabled(False)
        self.sec.setEnabled(False)
        self.third.setEnabled(False)
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
            for node in self.snakeArray:
                if(button.x() == node[0] and button.y() == node[1]):
                    button.setStyleSheet('background-color: green; color: green')
                    self.isOverlap = True
                    button.setEnabled(False)
            if(self.isOverlap == False and (button.x() != self.foodx or button.y() != self.foody)):
                button.setStyleSheet('background-color: white; color: white')
                button.setEnabled(True)

    def onEat(self):
        self.status.setText("Food was eaten")
        self.isPaused = True
        self.isFood = False
        self.isGrow = True
        self.count = 0
        self.foodEaten += 1
        if(int(self.foodEaten) >=15):
            self.stats.setText("Food Eaten: " + str(self.foodEaten))
            self.status.setText("Game Won! Enter name and press reset to play again")
            self.isPaused = True
            self.changeScore()
            self.win = True
            for button in self.buttonGroup.buttons():
                button.setEnabled(False)
        else:
            self.stats.setText("Food Eaten: " + str(self.foodEaten))
    def changeScore(self):
        print("FOOD EATEN: ")
        print(self.foodEaten)
        print("FIRST SCORE: ")

        if(self.foodEaten >= int(self.firstScore.text())):
           self.third.setText(self.sec.text())
           self.thirdScore.setText(self.secScore.text())
           self.sec.setText(self.first.text())
           self.secScore.setText(self.firstScore.text())
           self.first.setText(" - ")
           self.first.setEnabled(True)
           self.firstScore.setText(str(self.foodEaten))

        elif(self.foodEaten >= int(self.secScore.text())):
           self.third.setText(self.sec.text())
           self.thirdScore.setText(self.secScore.text())
           self.sec.setText(" - ")
           self.sec.setEnabled(True)
           self.secScore.setText(str(self.foodEaten))

        elif(self.foodEaten >= int(self.thirdScore.text())):
           self.third.setText(" - ")
           self.third.setEnabled(True)
           self.thirdScore.setText(str(self.foodEaten))

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if(self.isFood == False and self.win == False):   # wait for food
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
                    if(len(self.lastMove) == 1):
                        self.prev = self.lastMove[0]
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
                    elif(self.lastMove[0] == 'P'):
                        print("LOSE")
                        self.status.setText("You Lose! Enter name and press reset")
                        self.isPaused = True
                        self.changeScore()
                        for button in self.buttonGroup.buttons():
                            button.setEnabled(False)

                    self.checkOverlap()
        else:
            QFrame.timerEvent(self, event)
    
    @pyqtSlot()
    def on_click(self):
        #print('onclick')
        if self.sender().text() == 'Start':
            self.handler.uiData = 'S'
            self.handler.isUIData = True
            #print('start')
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
                self.b00.setStyleSheet('background-color: red; color: red')
                self.foodx = 300
                self.foody = 50
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (0,0), self.prev)
            elif self.sender().text() == 'b01':
                self.handler.uiData = '01'
                self.setButtonData()
                self.b01.setStyleSheet('background-color: red; color: red')
                self.foodx = 400
                self.foody = 50
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (0,1), self.prev)
            elif self.sender().text() == 'b02':
                self.handler.uiData = '02'
                self.setButtonData()
                self.b02.setStyleSheet('background-color: red; color: red')
                self.foodx = 500
                self.foody = 50
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (0,2), self.prev)
            elif self.sender().text() == 'b03':
                self.handler.uiData = '03'
                self.setButtonData()
                self.b03.setStyleSheet('background-color: red; color: red')
                self.foodx = 600
                self.foody = 50
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (0,3), self.prev)
            elif self.sender().text() == 'b10':
                self.handler.uiData = '10'
                self.setButtonData()
                self.b10.setStyleSheet('background-color: red; color: red')
                self.foodx = 300
                self.foody = 150
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (1,0), self.prev)
            elif self.sender().text() == 'b11':
                self.handler.uiData = '11'
                self.setButtonData()
                self.b11.setStyleSheet('background-color: red; color: red')
                self.foodx = 400
                self.foody = 150
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (1,1), self.prev)
            elif self.sender().text() == 'b12':
                self.handler.uiData = '12'
                self.setButtonData()
                self.b12.setStyleSheet('background-color: red; color: red')
                self.foodx = 500
                self.foody = 150
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (1,2), self.prev)
            elif self.sender().text() == 'b13':
                self.handler.uiData = '13'
                self.setButtonData()
                self.b13.setStyleSheet('background-color: red; color: red')
                self.foodx = 600
                self.foody = 150
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (1,3), self.prev)
            elif self.sender().text() == 'b20':
                self.handler.uiData = '20'
                self.setButtonData()
                self.b20.setStyleSheet('background-color: red; color: red')
                self.setButtonData()
                self.foodx = 300
                self.foody = 250
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (2,0), self.prev)
            elif self.sender().text() == 'b21':
                self.handler.uiData = '21'
                self.setButtonData()
                self.b21.setStyleSheet('background-color: red; color: red')
                self.foodx = 400
                self.foody = 250
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (2,1), self.prev)
            elif self.sender().text() == 'b22':
                self.handler.uiData = '22'
                self.setButtonData()
                self.b22.setStyleSheet('background-color: red; color: red')
                self.foodx = 500
                self.foody = 250
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (2,2), self.prev)
            elif self.sender().text() == 'b23':
                self.handler.uiData = '23'
                self.setButtonData()
                self.b23.setStyleSheet('background-color: red; color: red')
                self.foodx = 600
                self.foody = 250
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (2,3), self.prev)
            elif self.sender().text() == 'b30':
                self.handler.uiData = '30'
                self.setButtonData()
                self.b30.setStyleSheet('background-color: red; color: red')
                self.foodx = 300
                self.foody = 350
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (3,0), self.prev)
            elif self.sender().text() == 'b31':
                self.handler.uiData = '31'
                self.setButtonData()
                self.b31.setStyleSheet('background-color: red; color: red')
                self.foodx = 400
                self.foody = 350
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (3,1), self.prev)
            elif self.sender().text() == 'b32':
                self.handler.uiData = '32'
                self.setButtonData()
                self.b32.setStyleSheet('background-color: red; color: red')
                self.foodx = 500
                self.foody = 350
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (3,2), self.prev)
            elif self.sender().text() == 'b33':
                self.handler.uiData = '33'
                self.setButtonData()
                self.b33.setStyleSheet('background-color: red; color: red')
                self.foodx = 600
                self.foody = 350
                self.lastMove = self.getDirections(self.snakeArray, self.foodEaten, (3,3), self.prev)

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
                

    def getDirections(self, snakeArray, size, dest, prev):
        arr = []
        print(snakeArray, size, dest, prev)
        for i in range(0, len(snakeArray), 4):
            to_go = (  int((snakeArray[i][1] - 50) / 100 ) , int((snakeArray[i][0] / 100) - 3)   )
            arr.append(to_go)
        
        ac_size = size+2

        dArr = getDir(arr, ac_size, dest, prev)
        stopchar = ["P"]
        #send dArr[1] to Josh
        print("dArr[0]: ", dArr[0])
        print("dArr[1]: ", dArr[1])
        dArr[1].append("P")
        self.handler.updateCommands(dArr[1])
        print("self before: ", self.forTail, self.foodEaten)

        prev_ones = 0
        
        if (self.foodEaten == 0):
            self.handler.updateTailCommands(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-1]+stopchar)
            self.tori = calctori(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-1]+stopchar, self.tori)
        elif (self.foodEaten == 1):
            if dArr[1][:-1][-2] == "L" or dArr[1][:-1][-2] == "R":
                self.handler.updateTailCommands(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-3]+stopchar)
                self.tori = calctori(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-3]+stopchar, self.tori)
            else:
                self.handler.updateTailCommands(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-2]+stopchar)
                self.tori = calctori(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-2]+stopchar, self.tori)
        elif (self.foodEaten > 1):
            #equation = num_ones -1 + Dfloor((num_ones -1 / foodEaten))
            num_ones = dArr[1][:-1].count("1") - 1
            num_ds = math.floor((num_ones)/ self.foodEaten)
            if num_ones == 0:
                prev_ones = 0
                cur = arr[-1]
                cur1 = arr[-2]

                move1 = (cur1[0] - cur[0], cur1[1] - cur[1])

                if( self.tori == "L" and move1 == (1, 0) ):
                    self.handler.updateTailCommands(["L", "P"])
                    self.tori = calctori(["L", "P"], self.tori)
                elif( self.tori == "L" and move1 == (-1, 0) ):
                    self.handler.updateTailCommands(["R", "P"])
                    self.tori = calctori(["R", "P"], self.tori)
                elif( self.tori == "L" and move1 == (0, 1) ):
                    self.handler.updateTailCommands(["R", "R", "P"])
                    self.tori = calctori(["R", "R", "P"], self.tori)
                elif( self.tori == "L" and move1 == (0, -1) ):
                    #do nothing
                    e = 1 + 1
                elif( self.tori == "R" and move1 == (1, 0) ):
                    self.handler.updateTailCommands(["R", "P"])
                    self.tori = calctori(["R", "P"], self.tori)
                elif( self.tori == "R" and move1 == (-1, 0) ):
                    self.handler.updateTailCommands(["L", "P"])
                    self.tori = calctori(["L", "P"], self.tori)
                elif( self.tori == "R" and move1 == (0, 1) ):
                    #do nothing
                    e = 1 + 1
                elif( self.tori == "R" and move1 == (0, -1) ):
                    self.handler.updateTailCommands(["L", "L", "P"])
                    self.tori = calctori(["L", "L", "P"], self.tori)
                elif( self.tori == "U" and move1 == (1, 0) ):
                    self.handler.updateTailCommands(["L", "L", "P"])
                    self.tori = calctori(["L", "L", "P"], self.tori)
                elif( self.tori == "U" and move1 == (-1, 0) ):
                    #do nothing
                    e = 1 + 1
                elif( self.tori == "U" and move1 == (0, 1) ):
                    self.handler.updateTailCommands(["R", "P"])
                    self.tori = calctori(["R", "P"], self.tori)
                elif( self.tori == "U" and move1 == (0, -1) ):
                    self.handler.updateTailCommands(["L", "P"])
                    self.tori = calctori(["L", "P"], self.tori)
                elif( self.tori == "D" and move1 == (1, 0) ):
                    self.handler.updateTailCommands(["L", "P"])
                    #do nothing
                    e = 1 + 1
                elif( self.tori == "D" and move1 == (-1, 0) ):
                    self.handler.updateTailCommands(["L", "L", "P"])
                    self.tori = calctori(["L", "L", "P"], self.tori)
                elif( self.tori == "D" and move1 == (0, 1) ):
                    self.handler.updateTailCommands(["L", "P"])
                    self.tori = calctori(["L", "P"], self.tori)
                elif( self.tori == "D" and move1 == (0, -1) ):
                    self.handler.updateTailCommands(["R", "P"])
                    self.tori = calctori(["R", "P"], self.tori)
                
                    
            if num_ones == 1:
                prev_ones = 1
                cur = arr[-1]
                cur1 = arr[-2]
                dirArr = []

                dirArr, self.tori = forJoshTail([cur1], cur, self.tori)

                self.handler.updateTailCommands(dirArr+stopchar)
                
            elif num_ones == 2:
                prev_ones = 2
                cur = arr[-1]
                cur1 = arr[-2]
                cur2 = arr[-3]
                dirArr = []

                dirArr, self.tori = forJoshTail([cur1, cur2], cur, self.tori)

                self.handler.updateTailCommands(dirArr+stopchar)
                
                       
            elif num_ones == 3:
                prev_ones = 3
                cur = arr[-1]
                cur1 = arr[-2]
                cur2 = arr[-3]
                cur3 = arr[-4]
                dirArr = []

                dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                self.handler.updateTailCommands(dirArr+stopchar)
                
                    
            elif num_ones == 4:
                prev_ones = 4
                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)
                
                elif len(arr) >= 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)
                    
            elif num_ones == 5:
                prev_ones = 5

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 6:
                prev_ones = 6

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 7:
                prev_ones = 7

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 8:
                prev_ones = 8

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 9:
                prev_ones = 9

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 10:
                prev_ones = 10

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 11:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 11:
                prev_ones = 11

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 11:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 12:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 12:
                prev_ones = 12

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 11:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 12:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 13:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 13:
                prev_ones = 13

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 11:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 12:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 13:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 14:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    cur13 = arr[-14]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12, cur13], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 14:
                prev_ones = 14

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 11:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 12:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 13:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 14:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    cur13 = arr[-14]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12, cur13], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 15:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    cur13 = arr[-14]
                    cur14 = arr[-15]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12, cur13, cur14], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

            elif num_ones == 15:
                prev_ones = 15

                if len(arr) < 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 5:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 6:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 7:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 8:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 9:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 10:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 11:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 12:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 13:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 14:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    cur13 = arr[-14]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12, cur13], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) == 15:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    cur13 = arr[-14]
                    cur14 = arr[-15]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12, cur13, cur14], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                elif len(arr) >= 16:
                    cur = arr[-1]
                    cur1 = arr[-2]
                    cur2 = arr[-3]
                    cur3 = arr[-4]
                    cur4 = arr[-5]
                    cur5 = arr[-6]
                    cur6 = arr[-7]
                    cur7 = arr[-8]
                    cur8 = arr[-9]
                    cur9 = arr[-10]
                    cur10 = arr[-11]
                    cur11 = arr[-12]
                    cur12 = arr[-13]
                    cur13 = arr[-14]
                    cur14 = arr[-15]
                    cur15 = arr[-16]
                    dirArr = []

                    dirArr, self.tori = forJoshTail([cur1, cur2, cur3, cur4, cur5, cur6, cur7, cur8, cur9, cur10, cur11, cur12, cur13, cur14, cur15], cur, self.tori)

                    self.handler.updateTailCommands(dirArr+stopchar)

                
            #self.handler.updateTailCommands(self.forTail+dArr[1][:-1][:len(dArr[1][:-1])-(self.foodEaten)]+stopchar)
        print(self.foodEaten)
        return dArr[0]


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
