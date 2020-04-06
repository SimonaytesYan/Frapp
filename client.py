import socket
import threading
import sys
import numpy as np
import cv2
host = "192.168.1.128"
port = 8000
sock = socket.socket()
sock.connect((host, port))

clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((self.ipAddress, self.port))
    received = []
    while True:
        recvd_data = clientsocket.recv(230400).decode('utf-8')
        if not (recvd_data):
            break
        else:
            received.append(recvd_data)
        dataset = ''.join(received)
        image = np.array(dataset)
        print(image) #!
 
        cv2.imwrite('foo.jpg', image)       #исключение
        self.ids.image_source.reload()