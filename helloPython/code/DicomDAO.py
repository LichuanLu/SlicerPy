import sys
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload')
import sqlite3

class BaseDAO:
	ctkDicomConnect = sqlite3.connect("/Users/lichuan/Desktop/slicerdata/ctkDICOM.sql")
	def __init__(self):
		print "init basedao"
		sqlite3.enable_callback_tracebacks(True)
	def getCursor(self):
		return BaseDAO.ctkDicomConnect.cursor()	

