# -*- coding:utf-8 -*-
class PatientDao:
	def __init__(self):
		print "init PatientDAO"

	def getSResultList(self):
		self.patient = Patient("Li Gang")
		return self.patient.scan_result_list


class ScanResult:	
	def __init__(self,name,file_path):
		self.name = name
		self.file_path = file_path
		print "init ScanResult"


class Patient:
	def __init__(self,name):
		self.name = name
		self.initResultList()
	def initResultList(self):
		scan1 = ScanResult("2013-10-20","test path1")
		scan2 = ScanResult("2012-11-21","test path2")
		scan3 = ScanResult("2012-11-20","test path3")
		self.scan_result_list = []
		self.scan_result_list.append(scan1)
		self.scan_result_list.append(scan2)
		self.scan_result_list.append(scan3)




