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

#Path
home =  os.getcwd()
logdir = os.path.join(home,'log_files')
sys.path.append(os.path.join(home,'sub_scripts'))



# Custom Packages
from log_files import log_files
from log_files import Tee
from printer import gen


l = log_files()
g = gen()


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





