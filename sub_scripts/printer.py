'''
Created on Jan 22, 2015
@author: Oliver Stein
mail: oliver.stein@cern.ch
'''


'''
Script with output functions.

'''
# from termcolor import colored
import sys

class gen():
    
    # Prints string as follows
    # Used at beginning of every function
    def tprinter(self,string,flag):
        if flag == 1: 
            print ''
            print '--------------------------------------------------------------'
            print str(string)
            print '--------------------------------------------------------------'
            print ''
        else:
            pass
    # simple print function     
    def printer(self,string,flag):
        if flag == 1: 
            print str(string)
            print ''
        else:
            pass
    # print function used for server response    
    def rprinter(self,string,flag):
        if flag ==1:
            print ''
            print 'Response from server:'
            print string
            print ''
        else:
            pass
    def errprinter(self,string,flag):
        if flag ==1:
            print ''
            print 'Error occured:'
            print str(string)
            print ''
            print 'Stop script'
            sys.exit(str(string))
            print ''
        else:
            pass
        
        
    def loop_info(self,i,maxi,flag):
        if flag == 1: 
            print ''
            print '=============================================================='
            print 'start analysing file nr. '+str(i)+' of '+str(maxi)
            print '=============================================================='
            print ''
        else:
            pass