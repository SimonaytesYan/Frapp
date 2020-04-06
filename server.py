import socket
from threading import *
import socket
import cv2
 
def server():
    print ("\nServer started at " + str(socket.gethostbyname(socket.gethostname())) + " at port " + str(90) )
    port = 90
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('',port))
    serversocket.listen(10)
   
    capture=cv2.VideoCapture(0)
 
    while (True):
        connection, address = serversocket.accept()
        print ("GOT_CONNECTION")
        ret, frame = capture.read()
        print(frame) #!
        connection.sendall(bytes(str(frame), 'utf-8'))
        connection.close()
    
server()