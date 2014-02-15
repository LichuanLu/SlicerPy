#!/usr/bin/python
# -*- coding: utf-8 -*-

from __main__ import vtk, qt, ctk, slicer
import sys
import platform
if (platform.system() == "Darwin"):
    sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload')
elif (platform.system() == "Linux"):
    sys.path.append('/opt/Slicer-4.3.1-1/SlicerPy/helloPython/code')
# import sqlite3
from qt import QTableWidget,QTableWidgetItem,QPushButton,QWidget,QLabel,QProcess
from DicomDAO import BaseDAO
from BrainASUtils import PathDao
import os
import subprocess
import shutil
# cannot import , need investigates
# from PatientDao import PatientDao,ScanResult,Patient

#
# DicomAnalyze class
#

class DicomAnalyze:

    def __init__(self, parent):
        parent.title = 'DicomAnalyze'
        parent.categories = ['BrainAS']
        parent.dependencies = []
        parent.contributors = ['Lichuan Lu'
                               , 'Xiang Li']  # replace with "Firstname Lastname (Org)"
        parent.helpText = \
            """
    help text of DicomAnalyze module
    """
        parent.acknowledgementText = \
            """
    acknowledgement Text of DicomAnalyze module."""  # replace with organization, grant and thanks.

        self.parent = parent


#
# qDicomAnalyzeWidget
#

class DicomAnalyzeWidget:

    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
        self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()

    def setup(self):

    # Instantiate and connect widgets ...
    # Add vertical spacer

        self.initWidget()
        self.reloadButton = qt.QPushButton('Reload')
        self.reloadButton.toolTip = 'Reload this module.'
        self.reloadButton.name = 'DicomAnalyze Reload'
        self.layout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)





    def onReload(self, moduleName='DicomAnalyze'):
        """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """

        import imp
        import sys
        import os
        import slicer

        widgetName = moduleName + 'Widget'

    # reload the source code
    # - set source file path
    # - load the module to the global space

        filePath = eval('slicer.modules.%s.path' % moduleName.lower())
        p = os.path.dirname(filePath)
        if not sys.path.__contains__(p):
            sys.path.insert(0, p)
        fp = open(filePath, 'r')
        globals()[moduleName] = imp.load_module(moduleName, fp,
                filePath, ('.py', 'r', imp.PY_SOURCE))
        fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent

        parent = slicer.util.findChildren(name='DicomAnalyze Reload'
                )[0].parent()
        for child in parent.children():
            try:
                child.hide()
            except AttributeError:
                pass

    # Remove spacer items

        item = parent.layout().itemAt(0)
        while item:
            parent.layout().removeItem(item)
            item = parent.layout().itemAt(0)

    # create new widget inside existing parent

        globals()[widgetName.lower()] = \
            eval('globals()["%s"].%s(parent)' % (moduleName,
                 widgetName))
        globals()[widgetName.lower()].setup()

    def initWidget(self):
        self.font = qt.QFont()
        self.font.setBold(True)
        self.font.setPixelSize(15)
        self.tableTitle = QLabel("Full Records Table:")
        self.tableTitle.setFont(self.font)

        self.layout.addWidget(self.tableTitle)

        self.dbConnect = BaseDAO.ctkDicomConnect
        self.initDatabase()
        self.updateDatebase()

        #TODO
        #need to add function to update database from the temp file and add refresh button
        cu=self.dbConnect.cursor()

        #cu.execute("select b.UID as UID, b.PatientsName as PName, a.StudyDate as Date  from Studies as a,Patients as b where a.PatientsUID = b.UID")
        cu.execute("select a.Patient_UID as PUID, a.PatientsName as Name , b.StudyDate as Date , a.Status as Status , a.IsNormal as PGroup from Patients_extend as a ,Studies as b where a.Patient_UID = b.PatientsUID")
        res = cu.fetchall()
        cu.close()
        #status means process or done or not process , maybe add two list to work on start process and change group , group is able to use check box for each list item , and start process will load not process item to the list and start conduct
        
        #headers = ['UID','PName','Date','Description','NormalGroup','Status']
        headers = ['PUID','PName','Date','Status','','PGroup','']

     
        length = len(res)+2
        self.table = AllRecordTable(self,headers,res,length,7) 
        self.table.name = "AllRecordsTable"
        self.table.setColumnWidth(4,40)
        self.table.setColumnWidth(6,49)
        self.layout.addWidget(self.table)
        #two button ,refresh and save to db
    def updateDatebase(self):
        try:
            cu = self.dbConnect.cursor()
            cu.execute("select Patient_UID as PUID , Foldername as FolderName , Status from Patients_extend")
            res = cu.fetchall()
            for patient in res:
                tempfilePath = PathDao.freesurferPath+patient[1]+'/'+PathDao.tempfileName
                tempfile = open(tempfilePath)
                lines = tempfile.readlines()
                length = len(lines)
                PUID = int(patient[0])
                if length == 2 and "Done" in lines[1]:
                    #update database to 2
                    #print "lines:"+lines[2].strip()
                    print "lines:"+lines[1].strip()
                    print "lines:"+lines[0].strip()
                    cu.execute('update Patients_extend set Status = 2 where Patient_UID = ?',(PUID,))
                # elif length == 2:
                #     print "lines:"+lines[1].strip()
                    #check the time and if overtime should update status to 0 and kill process
                elif length == 1:
                    print "lines:"+lines[0].strip()
                    #check the time if overtime 6 miniute then update status to 0
                elif length == 0:
                    print "lines:"+"0"
                    cu.execute('update Patients_extend set Status = 0 where Patient_UID = ?',(PUID,))
                BaseDAO.ctkDicomConnect.commit()
        except Exception, e:
            raise
        finally:
            cu.close()
            if len(res) > 0:
                tempfile.close()


       
       
    def initDatabase(self):
        #insert new record to table of patient_extend 
        cuPExtend = self.dbConnect.cursor()
        cuPExtend.execute("select a.UID as UID , a.PatientsName as PatientsName , a.PatientsBirthDate as PatientsBirthDate, a.PatientsSex as PatientsSex , a.PatientsAge as PatientsAge from Patients as a where a.UID not in (select Patient_UID from Patients_extend)")
        resPExtend = cuPExtend.fetchall()
        cuPExtendInsert = self.dbConnect.cursor()
        print resPExtend
        for pExtendRow in resPExtend:
            try:
                print "pExtendRow"+str(pExtendRow)
                nowdate = datetime.datetime.now()
                if pExtendRow[4]:
                    age = pExtendRow[4]
                else:
                    cuPExtend.execute('SELECT StudyDate FROM Studies WHERE PatientsUID = ?',(pExtendRow[0],))
                    resStudyDate = cuPExtend.fetchone()
                    birthdate = datetime.datetime.strptime(pExtendRow[2],'%Y-%m-%d')
                    studyDate = datetime.datetime.strptime(resStudyDate[0],'%Y-%m-%d')
                    #age = nowdate.year - birthdate.year
                    age = studyDate.year - birthdate.year
            #status 0 means not handle , 1 mean processing , 2 means done
                namelist = pExtendRow[1].split(' ')
                namelistStr = "_".join(namelist)
                foldername = str(pExtendRow[0])+'_'+namelistStr+'_'+str(time.mktime(nowdate.timetuple()))
                #create folder to fs function should be attached to the function of processing, read folder name from database
                print "folername"+str(foldername)
                #create folder and file if don't exits
                folderpath = PathDao.freesurferPath+foldername
                #print folderpath
                if not os.path.exists(folderpath): os.makedirs(folderpath)
                fsdatafolder = folderpath+'/data'
                if not os.path.exists(fsdatafolder): os.makedirs(fsdatafolder)
                tempFilepath = folderpath+'/'+PathDao.tempfileName
                open(tempFilepath, 'a').close()

                cuPExtendInsert.execute("insert into Patients_extend (Patient_UID,PatientsName,PatientsSex,PatientsAge,Foldername,Status,IsNormal) values(?,?,?,?,?,0,0)",(pExtendRow[0],pExtendRow[1],pExtendRow[3],age,foldername))
            except:
                print 'get or insert error of patient_extend'
                #traceback.print_exc()
                continue
        self.dbConnect.commit()
        cuPExtendInsert.close()
        cuPExtend.close()
    # def changeGroupHandler(self,PUID):
    #     print "change group handler---"+str(PUID)
    # def changeStatusHanlder(self,PUID,Status):
    #     print "change status handler---"+str(PUID)+"---"+str(Status)
    def handleItemClicked(self,item):
        print item
        print self.table.item(item.row(),0).text()


                
class MyTable(QTableWidget):
    def __init__(self,headers,data, *args): 
        print data
        QTableWidget.__init__(self, *args) 
        self.headers = headers
        self.data = data
        self.newitemlist = []   
        self.setmydata() 
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.resizeColumnsToContents() 
        self.resizeRowsToContents()
    def setmydata(self):
        self.setHorizontalHeaderLabels(self.headers)
        for n, item in enumerate(self.data): 
            for m, key in enumerate(self.headers):
                cnt = '%s'% item[m]
                newitem = QTableWidgetItem(cnt)
                #newitem = QPushButton(self)
                newitem.setText(cnt)
                #example don't contain this , but the gabage system will kill the object after the table init , so i add one more call for each in the list
                self.newitemlist.append(newitem)
                #self.setCellWidget(n, m, newitem)
                self.setItem(n, m, newitem)


class AllRecordTable(MyTable):
    def __init__(self,mainInstance,headers,data, *args):
        self.mainInstance = mainInstance
        MyTable.__init__(self,headers,data,*args)
        print "myinstance"+str(self.mainInstance)
    def setmydata(self):
        self.setHorizontalHeaderLabels(self.headers)
        self.setContentData()
        
                    #self.setItem(n, m, newBtn)
    def setContentData(self):
        for n, item in enumerate(self.data): 
            for m, key in enumerate(self.headers):
                print item
                print str(m)+"--"+key
                if key:
                    if m == 5:
                        cnt = self.getGroupText(item[4])
                    elif m == 3:
                        #set text for status
                        cnt = self.getStatusText(item[3])
                    else:
                        cnt = '%s'% item[m]
                    
                    newitem = QTableWidgetItem(cnt)
                    #newitem = QPushButton(self)
                    newitem.setText(cnt)
                    #example don't contain this , but the gabage system will kill the object after the table init , so i add one more call for each in the list
                    self.newitemlist.append(newitem)
                    #self.setCellWidget(n, m, newitem)
                    self.setItem(n, m, newitem)
                else:
                    newBtn = QButton(self)
                    #newBtn = QTableWidgetItem()
                    self.newitemlist.append(newBtn)
                    if m == 4:
                        #self.setBtnName(newBtn,'status',item)
                        newBtn.name = 'btnSARTable-%s-%s-%s'%(item[0],item[3],n)
                        #newBtn.setDisabled(False)
                        newBtn.button.show()
                        print "setContentData:"+"new btn show:"+newBtn.name
                        btnText = "Start"
                        if item[3] == 1:
                            #newBtn.setDisabled(True)
                            newBtn.button.hide()
                            print "setContentData:"+"new btn hide:"+newBtn.name

                        elif item[3] == 2:
                            btnText = "Rerun"
                        newBtn.setText(btnText)                        
                        #self.connect(newBtn,qt.SIGNAL("clicked()"),self.changeStatusHanlder)
                        #newBtn.clicked.connect(self.changeStatusHanlder)
                    elif m == 6:
                        #self.setBtnName(newBtn,'group',item)
                        newBtn.name = 'btnGARTable-%s-%s-%s'%(item[0],item[4],n)
                        newBtn.setText("Change")
                        #self.connect(newBtn,qt.SIGNAL("clicked()"),self.changeGroupHandler)
                        #newBtn.clicked.connect(self.changeGroupHandler)
                    self.setCellWidget(n, m, newBtn)
    def setBtnName(self,newBtn,typeStr,item):
        if typeStr == 'group':
            newBtn.name = 'btnGARTable-%s-%s-%s'%(item[0],item[4],n)
            newBtn.setText("Change")

        elif typeStr == 'status':
            newBtn.name = 'btnSARTable-%s-%s-%s'%(item[0],item[3],n)
            #newBtn.setDisabled(False)
            newBtn.show()
            btnText = "Start"
            if item[3] == 1:
                #newBtn.setDisabled(True)
                newBtn.hide()
            elif item[3] == 2:
                btnText = "Rerun"
            newBtn.setText(btnText)


    def getStatusText(self,code):
        if code == 0:
           return 'Not Start'
        elif code == 1:
            return 'Processing'
        elif code == 2:
            return 'Done'
        else:
            return ''
    def getGroupText(self,code):
        if code == 0:
            return 'Patient'
        elif code == 1:
            return 'Normal'
        else:
            return ''
    def refreshTable(self,row,typeStr,value):
        print "refresh table view"
        if typeStr == 'group':
            newtext = self.getGroupText(value)
            self.item(row,5).setText(newtext)
        elif typeStr == 'status':
            newtext = self.getStatusText(value)
            self.item(row,3).setText(newtext)

        # self.clearContents()
        # cu = BaseDAO.ctkDicomConnect.cursor()        
        # cu.execute("select a.Patient_UID as PUID, a.PatientsName as Name , b.StudyDate as Date , a.Status as Status , a.IsNormal as PGroup from Patients_extend as a ,Studies as b where a.Patient_UID = b.PatientsUID")
        # res = cu.fetchall()
        # cu.close()
        # self.data = res
        # self.newitemlist = [] 
        # self.setContentData()
        #TODO need to add clean folder function
    def cleanFolder(self,PUID):
        cu = BaseDAO.ctkDicomConnect.cursor()
        try:
            cu.execute('select Foldername from Patients_extend  where Patient_UID = ?',(PUID,))
            res = cu.fetchone()
            print "clearn"+str(res)
            folder = PathDao.freesurferPath+res[0]
            print folder
            fsFolder = folder+'/data'
            # for the_file in os.listdir(folder):
            #     file_path = os.path.join(folder, the_file)
            shutil.rmtree(fsFolder) 
            # tempFilepath = folder+'/'+PathDao.tempfileName
            # tempfile = open(tempFilepath, 'a')
            # tempfile.truncate()
            if not os.path.exists(fsFolder): os.makedirs(fsFolder)
        except:
            print 'clean folder error'
            traceback.print_exc()
        finally:
            cu.close()
            # tempfile.close()

    def runFreesurfer(self,PUID):
        cu = BaseDAO.ctkDicomConnect.cursor()
        try:
            cu.execute("select a.Foldername as TargetFolder , d.Filename as FileName from Patients_extend as a , Studies as b , Series as c ,  Images as d where b.PatientsUID = a.Patient_UID and b.StudyInstanceUID = c.StudyInstanceUID and c.SeriesInstanceUID = d.SeriesInstanceUID and c.SeriesDescription like '%%MPRAGE%%' and a.Patient_UID = ?",(PUID,))
            res = cu.fetchone()
            print res
            if res:
                shellPath = PathDao.pythonHome+'script/prepare.sh'
                freesurferPath = PathDao.freesurferPath+res[0]
                targetDataPath = freesurferPath+'/data'
                fileName = res[1]
                tempFile = freesurferPath+'/'+PathDao.tempfileName
                open(tempFile, 'w').close()
                print "targetDataPath:"+targetDataPath
                print "fileName:"+fileName
                print "tempFile:"+tempFile
                #subprocess.call([shellPath,targetDataPath,fileName,tempFile])
                command = shellPath
                args = [targetDataPath,fileName,tempFile]
                process = QProcess()
                process.startDetached(command,args)
        except:
            print "run freesurfer error"
            traceback.print_exc()
        finally:
            cu.close()
            

class QButton(QWidget):
    def __init__(self, parent=None):
       # print parent
        QWidget.__init__(self, parent)
        self.button = QPushButton('Button', self)
        self.button.setStyleSheet('QPushButton {color: white;background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(190, 49, 8), stop:1 rgba(255, 10, 4));padding: 2px;}')
        self.name='default'
        self.button.clicked.connect(self.calluser)
    def calluser(self):
        print(self.name)
        actionList = self.name.split('-')
        prefix = actionList[0]
        if prefix == 'btnGARTable':
        #    print self.parent()
             self.updateGroup(actionList[1],actionList[2],actionList[3])
        elif prefix == 'btnSARTable':
             self.updateStatus(actionList[1],actionList[2],actionList[3])
        #    print self.parent()
             
        #TODO need to modify the temp file to processing
    def updateStatus(self,PUID,code,row):
        #temp file can be concat , target folder can be read from database,then find one dicom data from db 
        cu = BaseDAO.ctkDicomConnect.cursor()
        PUID = int(PUID)
        try:
            if code != '1':
                cu.execute('update Patients_extend set Status = 1 where Patient_UID = ?',(PUID,))
            BaseDAO.ctkDicomConnect.commit()
            if code == '2':
                self.parent().parent().cleanFolder(PUID)
            row = int(row)
            self.parent().parent().refreshTable(row,'status',1)
            #self.button.setDisabled(True)
            self.button.hide()
            self.name = 'btnSARTable-%s-%s-%s'%(PUID,1,row)
            print "run freesurfer"
            self.parent().parent().runFreesurfer(PUID)
        except:
            print 'error of updateGroup'
            traceback.print_exc()
        finally:
            cu.close()

        #handle name and then get info and handle
    def updateGroup(self,PUID,code,row):
        cu = BaseDAO.ctkDicomConnect.cursor()
        print "code:"+str(code)+"PUID:"+str(PUID)
        PUID = int(PUID)
        try:
            if code == '0':
                cu.execute('update Patients_extend set IsNormal = 1 where Patient_UID = ?',(PUID,))
                res = 1
            elif code == '1':
                cu.execute('update Patients_extend set IsNormal = 0 where Patient_UID = ?',(PUID,))
                res = 0
            BaseDAO.ctkDicomConnect.commit()
            row = int(row)
            self.parent().parent().refreshTable(row,'group',res)
            self.name = 'btnGARTable-%s-%s-%s'%(PUID,res,row)
        except:
            print 'error of updateGroup'
            traceback.print_exc()
        finally:
            cu.close()


    def setText(self,str):
        self.button.setText(str)



