'''
Created on Feb 2, 2015
@author: Oliver Stein
mail: oliver.stein@cern.ch
'''


'''
Rosy Readout Cividec
subscripts and classes for client.py

'''

import socket
import time
import sys
import numpy as np

# Custom class for handling output (see printer.py)
from printer import gen

g = gen()

# Class for communicating with ROSY 
class RosyClient(object):
    def __init__(self):
        #Creates a IP-socket 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.data = [] 
    def set_timeout(self,time_out,pflag):
        g.tprinter('Setting time out',pflag)
        self.to = time_out
        g.printer('Timeout: '+str(self.to)+'s',pflag)    
    # Gives the port and IP to the RosyClient class    
    def ip_port(self,ip,port,pflag):
        g.tprinter('Setting server ip and port',pflag)
        self.ip = ip
        self.port = port
        g.printer('server IP:'+str(self.ip),pflag)
        g.printer('server port:'+str(self.port),pflag)
        
        
    # Receiving module
    # Waits for the server response 
    # n is the max number of bytes, which can be received
    # m is the list index of the splitted received message
    # '\nhello\n -> [\n, hello,\n][1]->'hello'  
    def rec (self,n,m,pflag):
#         g.printer('waiting for server response.',pflag)


    
        
        try:
            r = self.s.recv(n)
        except socket.error as e:
            g.errprinter(e,pflag)   
        
        out = r.split('\n')[m]

        
        g.rprinter(str(out),pflag)

        
        return out 
    
    # Sending module
    def sen(self,mes,pflag):
        g.printer('sending string to server: \n'+str(mes),pflag)
        self.s.send(mes)
        
    # Module for setting up the connection to the ROSY-box
    def start_connection(self,pflag):
        # Check if IP and port are defined 
        # if not script stops
        try:
            self.ip
        except:
            g.errprinter('IP not set',pflag)
            
        try:   
            self.port
        except:
            g.errprinter('Port not set',pflag)
            
        try:
            self.to
        except:
            g.printer('timout not set',pflag)
            g.printer('setting timeout to 10s',pflag)
            self.to = 10
        
        # Start Initialising
        g.tprinter('Initialising ROSY connection',pflag)
        g.printer('IP address: '+str(self.ip),pflag)
        g.printer('Port: '+str(self.port),pflag)
        try:
            # tries to connect to the server (IP and port)
            self.s.settimeout(self.to)
            self.s.connect((self.ip,self.port))
        except socket.error as e:
            print e
        # Sends first message to server
        # Command to server     
        self.mes = 'hello\n'
        self.sen(self.mes,pflag)
        # Server response
        self.ret = self.rec(1024,1,pflag)
        
        
        # Next message
        # Command to server 
        self.mes = 'version 1.0\n'
        self.sen(self.mes,pflag)
        self.ret = self.rec(1024,1,pflag)
        
        

        g.printer('Connection established',pflag)
    
    # Module for getting the available devices from the server
    def get_device(self,pflag):
        g.tprinter('Getting devices',pflag)
        
        # Command to server
        self.mes = 'function getDevices\n'
        self.sen(self.mes,pflag)
        self.ret = self.rec(1024,2,pflag)
        
#         ret = str('[{id:0,name:"pico6402-AT626/042",devHandler:1},{id:0,name:"pico6402-AT626/042",devHandler:1}]')
        # Formatting the response string 
        self.ret =self.ret.split('[')[1].split(']')[0].split('{')
        self.info = []
        for i in self.ret:
            if i.startswith('id'):
                k = i.split('}')[0].split(',')
                k[0]=k[0].split(':')
                k[0][1]=int(k[0][1])
                k[1]=k[1].split(':')
                k[2]=k[2].split(':')
                k[2][1]=int(k[2][1])
                self.info.append(k)
        
        # Output of the found devices
        g.printer('found devices:',pflag)
        num = 1
        for i in self.info:
            g.printer('Device '+str(num),pflag)
            for k in i:
                g.printer(k,pflag)
            num = num+1
    
    # Module for acquiring a device
    # dev_num is the device number  
    def acquire_device(self,dev_num,pflag):
        g.tprinter('Acquiring device ',pflag)
        # Test self.info string
        try: 
            self.info
        except:
            g.printer('self.info not defined',pflag)
            sys.exit('script stop')
            
#         g.printer(len(self.info),pflag)
        if dev_num > len(self.info):
            g.errprinter(str(dev_num)+'larger than len(self.info)',pflag)
            
        
        # Command to server 
        self.mes = 'function acquireDevice\n'+str(dev_num)+'\n' 
        
#         g.printer(self.mes,pflag)
        self.sen(self.mes,pflag)
        self.ret = self.rec(1024,1,pflag)
        self.dev_id = self.ret.split(':')[1]
        
        time.sleep(1)
        
        
        g.printer('Device id\n'+str(self.dev_id),pflag)
#         g.printer(self.dev_id,pflag)

    # New Histogram Module
    def hist_new(self,pflag):
        g.tprinter('New hist module',pflag)
        self.s.send('function setMode\n')
        self.s.send(str(self.dev_id)+'\n')
        self.s.send('HISTOGRAM\n')
        time.sleep(1)
        res = self.s.recv(1024)
        g.printer(res,pflag)
        self.s.send('procedure setupHist\n')
        self.s.send(str(self.dev_id)+'\n')
        self.s.send('0.025\n')
        time.sleep(1)
        res = self.s.recv(1024)
        g.printer(res,pflag)
   
    # Module for setting the threshold of the Histogram mode
    def hist_threshold(self,thresh,pflag):
        g.tprinter('Set histogram threshold to:\n'+str(thresh),pflag)
        self.hist_threshold = thresh
    
    # Module for setting the acquired device to histogram mode
    def hist_setup(self,dev_id,pflag):
        g.tprinter('Setting up histogram mode',pflag)
        
        # Checks if hist_thresholdis defined
        # if not it is set to 0.1
        try: 
            self.hist_threshold 
            g.printer('Histogram threshold: \n'+str(self.hist_threshold),pflag)
        except:
            self.hist_threshold = .1     
        
        # Checks if the dev_id is defined 
        # if not the script stops
        try:
            self.dev_id 
        except:
            g.errprinter('no device found',pflag)
        
        # Command to server 
        # Sets device with id dev_id to histogram mode
        self.mes = 'function setMode\n'+str(dev_id)+'\nHISTOGRAM\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        self.ret = self.rec(1024,1,pflag)
        time.sleep(1)
        
        # Command to server 
        # Sets the threshold for the device 
        self.mes = 'procedure setupHist\n'+str(self.dev_id)+'\n'+str(self.hist_threshold)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        self.ret = self.rec(1024,1,pflag)
        
        time.sleep(1)
        
        # Command to server 
        # Arms the device 
        self.mes = 'procedure arm\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        self.ret = self.rec(1024,1,pflag)
        
        time.sleep(1)
        # Command to server 
        # Requests the status of the device
        self.mes = 'function getStatus\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        rec = self.s.recv(1024)
        g.printer(str(rec),pflag)
#         for i in range(0,10):
#             time.sleep(2)
#             g.printer(str(i),pflag)
#         self.ret = self.rec(1024,0,pflag)
    def get_status(self,pflag):
        g.tprinter('Requesting device status',pflag)
        self.mes = 'function getStatus\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        rec = self.s.recv(1024)
        g.printer(str(rec),pflag)
        return rec
        
    # Module for retrieving histogram data from 
    def get_histdata(self,dev_id,pflag):
        g.tprinter('Requesting data from device '+str(dev_id),pflag)
        
        # Command to server 
        # Requests histogram data from device
        self.mes = 'function getHistData\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        # Expecting data 
        self.ret = self.rec(1024**2,1,pflag)
        self.data = self.ret 
        g.printer(self.data,pflag)
   
   
    # Module for stopping the acquisition 
    def stop_acquisition(self,dev_id,pflag):
        g.tprinter('Stopping the data acquisition on device'+str(dev_id),pflag)
        # Command to server 
        # Requests histogram data from device
        self.mes = 'procedure stopAcquistion\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        # Expecting data 
        self.ret = self.rec(1024**2,1,pflag)
        self.data = self.ret
    
    

    # Module for setting up the POST MORTEM mode
    def pm_setup(self,dev_id,pflag):
        g.tprinter('Setting up post mortem mode',pflag)
        

        
        # Command to server 
        # Sets device with id dev_id to PM mode
        g.printer('set device to Post Mortem mode',pflag)
        self.mes = 'function setMode\n'+str(dev_id)+'\nPOST_MORTEM\n' 
        self.sen(self.mes,pflag)
        self.ret = self.rec(1024,1,pflag)
        
        time.sleep(1)
        
        # Setup parameters
        # Channel setup
        #Single channel
        channel ='A' 
        # All channels (A,B,C,D)
#         channel ='ALL' 
        # Trigger delay in seconds
        delay = 0.004
        # Range and code of the channels
        # 100 mV 3
        # 200 mV 4
        # 500 mV 5
        #   1  V 6
        #   2  V 7
        #   5  V 8
        
        range_a = 3
        range_b = 3
        range_c = 3
        range_d = 3
        
        # Command to server 
        # Command consists of dev_id, channels, delay, range of channels
        g.printer('set Post Mortem parameters (channels, delay, ranges)',pflag)
        self.mes = 'procedure setupPostmortem\n'+str(self.dev_id)+'\n'+str(channel)+'\n'+str(delay)+'\n'+str(range_a)+'\n'+str(range_b)+'\n'+str(range_c)+'\n'+str(range_c)+'\n'+str(range_d)+'\n'  
        self.sen(self.mes,pflag)
        time.sleep(1)
        self.ret = self.rec(1024,1,pflag)
        
        time.sleep(1)
        
        # Command to server 
        # Arms the device 
        g.printer('arm the device',pflag)
        self.mes = 'procedure arm\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        self.ret = self.rec(1024,1,pflag)
        
        

        
    # Closes the connection to the server  
    def get_pmdata(self,pflag):
        g.tprinter('Requesting data from device '+str(self.dev_id),pflag)
        
        # Command to server 
        # Requests histogram data from device
        self.mes = 'function getData\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        # Expecting data 
        self.ret = self.rec(1024**2,0,pflag)
        self.data = self.ret 
        g.printer(self.data,pflag)
    
    # Simple loop module requesting the device status
    # Loop stops if get setatus returns READY
    def get_status_loop(self,t,niter,pflag):
        g.tprinter('Running get_status_loop',pflag)
        g.printer('number of iterations '+str(niter),pflag)
        # Loop requesting the status of the device niter times and sleeps for t seconds 
        for i in range(niter):
            g.printer('requesting device status',pflag)
            g.printer(str(i)+' iteration of '+str(niter),pflag)
            out = self.get_status(0)
            out = out.split('\n')[1]
            # If the status of the device is READY, loop ends
            if out == 'READY':
                g.printer('Device status is READY \n exit loop',pflag)
                break
            else:
                g.printer('Device NOT READY',pflag)
            
            g.printer(str(out),pflag)
            time.sleep(t)
            
        g.printer('ending get_status_loop',pflag)
            
        
    # Module for releasing the device    
    def release_device(self,pflag):
        g.tprinter('Release device '+str(self.dev_id),pflag)
        
        # Command to server 
        # Requests histogram data from device
        self.mes = 'procedure releaseDevice\n'+str(self.dev_id)+'\n' 
        self.sen(self.mes,pflag)
        time.sleep(1)
        self.ret = self.rec(1024,1,pflag)
        
#         time.sleep(1)
#         self.ret = self.rec(1024,0,pflag)
        
        
    def bye_rosy(self,pflag):
        g.tprinter('closing rosy connection',pflag)
        self.mes = 'byerosy\n' 
        self.sen(self.mes,pflag)
        
              
    def close_connection(self,pflag):
        g.tprinter('closing server connection to:',pflag)
        g.printer('IP:'+str(self.ip),pflag)
        g.printer('Port:'+str(self.port),pflag)
        
        self.s.close()
        g.printer('connection closed',pflag)
        