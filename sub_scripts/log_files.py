'''
Created on Jan 22, 2015
@author: Oliver Stein
mail: oliver.stein@cern.ch
'''


'''
Script with functions to setup the log file.

'''

# Default Packages

import sys
import os
import numpy as np
import csv
import matplotlib.pyplot as plt
import numpy as np
import shutil as st
import pickle 
from time import strftime, localtime, time
import time
import glob

from printer import gen


g = gen()


class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

class log_files():
    
    # Setting up the log file in the directory where the script is saved
    def log_file_set(self,path,name,pflag):
        g.tprinter('Initialising log file',pflag)
        if not os.path.exists(os.path.join(path,'log_files')):
            os.mkdir(os.path.join(path,'log_files'))
        
        # Directory of the script 
        self.c_dir = path
        
        # Directory of the script 
        self.l_dir = os.path.join(path,'log_files')
        
        # Create time string
        self.creat_time = strftime("%Y%m%d_%H%M", localtime())
        
        # Path and name of the log file
        self.log_file_path=os.path.join(path,'log_files',str(name)+'_'+self.creat_time+'.txt')
        g.printer('log file path:',pflag)
        g.printer(self.log_file_path,pflag)
        
        # Head of the log file
        print ''
        self.log_file=open(self.log_file_path,'w+')
        
        print >> self.log_file, '-------------------------------------------------------' 
        print >> self.log_file, 'main.py Log_file'
        print >> self.log_file, ''
        print >> self.log_file, 'Script_file dir: '+str(self.c_dir)
        print >> self.log_file, 'Log_file dir: '+str(self.l_dir)
        print >> self.log_file, 'Log_file name: '+str(name)+'_'+self.creat_time+'.txt'
        print >> self.log_file, ''
        print >> self.log_file, 'date: '+strftime("%a, %d %b %Y", localtime())
        print >> self.log_file, 'time: '+strftime("%H:%M:%S", localtime())
        print >> self.log_file, ''
        print >> self.log_file, '-------------------------------------------------------'
#         print >> self.log_file, 'current directory: '+str(self.c_dir)
#         print >> self.log_file, 'root directory: '+str(self.start)
        print >> self.log_file, ''
#         print >> self.log_file, self.out
        print >> self.log_file, ''
    
        # Closing file
        self.log_file.close()
        g.printer('log file successful created',pflag)
    # Returns the path of the log file
    def log_path(self):
        return self.log_file_path

    def log_file_cleaner(self, path):
        for fl in glob.glob(os.path.join(path,'log*.txt')):
            os.remove(fl)
