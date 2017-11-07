from PyQt5.QtCore import QObject, pyqtSignal
import socket
from PyQt5.QtCore import *

class ComHandler(QObject):
    
    dataSignal = pyqtSignal(str)
    isUIData = False
    uiData = ''
    
    def __init__(self):
        super().__init__()
        self.host = ''
        self.port = 2000
        self.backlog = 5
        self.size = 1024

    def registerListen(self, mySignal):
        print("registered Listen")
        mySignal.connect(self.listenSlot)

    @pyqtSlot()
    def listenSlot(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(self.backlog)
        
        print ("server started and listening")

        while True:
            client, address = s.accept()
            client.settimeout(1)
            print ("accepted client")
            while True:
                try:
                    # receive data in
                    data = client.recv(self.size)
                    if data:
                        print ("received data: " + data.decode())
                        self.dataSignal.emit(data.decode())
                except Exception as e:
                    # send data out
                    if self.isUIData:
                        print("sending out: " + self.uiData)
                        self.isUIData = False
                        client.send(str.encode(self.uiData))

#          print ("closing client")
#            client.close()
 
