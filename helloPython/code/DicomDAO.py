import sys
import platform
if (platform.system() == "Darwin"):
    sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload')
elif (platform.system() == "Linux"):
    sys.path.append('/opt/Slicer-4.3.1-1/SlicerPy/helloPython/code')
import sqlite3

class BaseDAO:
	if (platform.system() == "Darwin"):
		ctkDicomConnect = sqlite3.connect("/Users/lichuan/Desktop/slicerdata/ctkDICOM.sql")
	elif (platform.system() == "Linux"):
		ctkDicomConnect = sqlite3.connect("/opt/db/ctkDICOM.sql")
	def __init__(self):
		print "init basedao"
		sqlite3.enable_callback_tracebacks(True)
	def getCursor(self):
		return BaseDAO.ctkDicomConnect.cursor()	

