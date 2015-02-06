'''
Created on Jan 23, 2015

@author: Oli
'''
import socket

def Main():
    host = '137.138.196.78'
    port = 3893
    s = socket.socket()
    s.bind((host,port))
    
    message = raw_input("-> ")
    while message != 'q':
        s.send(message)
        data = s.recv(1024)
        print 'Recieved from server: '+str(data)
        message = raw_input("-> ")
    s.close()
    
if __name__ == '__main__':
    Main()
        