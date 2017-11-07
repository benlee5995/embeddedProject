import socket

host = ''
port = 2000
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(backlog)

print ("server started and listening")
while True:
    client, address = s.accept()
    print ("accepted client")
    while True:
        data = client.recv(size)
        if data:
            print ("received data: " + data.decode())
            client.send(data)

print ("closing client")
client.close()

