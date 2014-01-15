from __main__ import vtk, qt, ctk, slicer
import time
import thread 
class CusUtils:
    def __init__(self):
        print "init CusUtils"
    def timer(self,no,interval):
        cnt = 0  
        while cnt<100000:  
            print 'Thread:(%d) Time:%s\n'%(no, time.ctime()) 
            slicer.util.quit()
            time.sleep(interval)  
            cnt+=1  
        thread.exit_thread()  
class PathDao:
    dbPath="/Users/lichuan/Desktop/slicerdata/ctkDICOM.sql"
    freesurferPath="/bas/freesurfer/"
    tempfileName="bastempfile"
    pythonHome="/dev_lic/SlicerPy/helloPython/code/"
    def __init__(self):
        pass        