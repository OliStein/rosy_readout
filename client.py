'''
Created on Jan 22, 2015
@author: Oliver Stein
mail: oliver.stein@cern.ch
'''


'''
Main script for connecting and communincating with Cividec ROSY box
'''

# Default Packages

import sys
import os
import numpy as np
import socket
import time
#Path
home =  os.getcwd()
logdir = os.path.join(home,'log_files')
sys.path.append(os.path.join(home,'sub_scripts'))


# Custom Packages
from log_files import *
from printer import gen
from rosy_connect import *

l = log_files()
g = gen()
rc = RosyClient()

'''
Print Flag
If pflag = 1, print output in gen() will be displayed
If pflag = 0, no print output will be displayed 
This applies for the log file as well
'''
pflag = 1

# Setting up the log file
# It will be stored in the log_files directory, 
# which if not existing will be created in home dir
l.log_file_set(home,'log',pflag)

# Writes the normal console output in the log file as well
f = open(l.log_path(),'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)

'''
Main
'''

# IP and port of the server
ip = '137.138.196.78'
port = 3893
# dev_id ='rosy'
# timeout for communication with server  in seconds 
timeout = 10

# give ip, port and timeout to rc 
rc.ip_port(ip,port,pflag)
rc.set_timeout(timeout,pflag)

# setting up the connection to the server 
rc.start_connection(pflag)
# getting the devices connected to the server
rc.get_device(pflag)
# acquire device (rec.dev_id needed)
rc.acquire_device(0,pflag)

#--------------------------------
# Setup for POST MORTEM 
#--------------------------------

# setting post mortem mode
rc.pm_setup(rc.dev_id,pflag)

rc.get_status_loop(2,10,pflag)

# rc.get_pmdata(pflag)
#--------------------------------
# Setup for HISTOGRAM
#--------------------------------

# rc.hist_new(pflag)

# setting histogram threshold
# rc.hist_threshold(1,pflag)
# setting histogram mode
# rc.hist_setup(rc.dev_id,pflag)

# for i in range(0,10):
#     rc.get_status(pflag)
#     g.printer('Iterator '+str(i),pflag)
#     time.sleep(2)


# requesting histogrm data
# rc.get_histdata(rc.dev_id,pflag)

#stops data acquistion
# rc.stop_acquisition(rc.dev_id,pflag)

#releases the device, still connected to server 
rc.release_device(pflag)

# closes connection to server    
rc.close_connection(pflag)



