'''
Created on Jan 22, 2015
@author: Oliver Stein
mail: oliver.stein@cern.ch
'''


'''
Script with output functions.

'''
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

    def loop_info(self,i,maxi,flag):
        if flag == 1: 
            print ''
            print '=============================================================='
            print 'start analysing file nr. '+str(i)+' of '+str(maxi)
            print '=============================================================='
            print ''
        else:
            pass