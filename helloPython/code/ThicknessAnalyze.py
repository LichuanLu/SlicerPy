#!/usr/bin/python
# -*- coding: utf-8 -*-

from __main__ import vtk, qt, ctk, slicer
from qt import QLabel
from DicomDAO import BaseDAO
from BrainASUtils import PathDao


# cannot import , need investigates
# from PatientDao import PatientDao,ScanResult,Patient

#
# ThicknessAnalyze class
#

class ThicknessAnalyze:

    def __init__(self, parent):
        parent.title = 'ThicknessAnalyze'
        parent.categories = ['BrainAS']
        parent.dependencies = []
        parent.contributors = ['Lichuan Lu'
                               , 'Xiang Li']  # replace with "Firstname Lastname (Org)"
        parent.helpText = \
            """
    help text of ThicknessAnalyze module
    """
        parent.acknowledgementText = \
            """
    acknowledgement Text of ThicknessAnalyze module."""  # replace with organization, grant and thanks.
        parent.icon = qt.QIcon(':Icons/Medium/SlicerDownloadMRHead.png')

        self.parent = parent



#
# qThicknessAnalyzeWidget
#

class ThicknessAnalyzeWidget:

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

        # self.layout.addStretch(1)
        self.font = qt.QFont()
        self.font.setBold(True)
        self.font.setPixelSize(15)
        self.listTitle = QLabel("Record List:")
        self.listTitle.setFont(self.font)

        self.layout.addWidget(self.listTitle)

        self.qt_scan_result_list = qt.QTreeWidget()

    # descending order as default

        self.qt_scan_result_list.setSortingEnabled(1)
        self.qt_scan_result_list.setHeaderLabels(['PUID','Name','Age','Group'])
        patient_dao = PatientDao()
        scan_results = patient_dao.getSResultList()
        item_list = []
        for result in scan_results:
            #print str(result[0]) + ',' + result[1]+','+result[2]+','+result[3]
            item = qt.QTreeWidgetItem([result[0], result[1],result[2],result[3]])
            item_list.append(item)

        # item.content = result

        self.qt_scan_result_list.insertTopLevelItems(0, item_list)

    # add double click handler

        self.qt_scan_result_list.connect('itemDoubleClicked (QTreeWidgetItem *,int)'
                , self.onTreeItemDoubleClicked)
        self.layout.addWidget(self.qt_scan_result_list)

    # Add vertical spacer


        self.reloadButton = qt.QPushButton('Reload')
        self.reloadButton.toolTip = 'Reload this module.'
        self.reloadButton.name = 'ThicknessAnalyze Reload'
        self.layout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)
    # # Collapsible button
    # # sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    # # sampleCollapsibleButton.text = "A collapsible button"
    # # self.layout.addWidget(sampleCollapsibleButton)

    # # Layout within the sample collapsible button
    # # sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # # HelloWorld button
    # # (Insert Section A text here)
    # # (be sure to match indentation of the rest of this
    # # code)
    # # HelloWorld button

    #     helloWorldButton = qt.QPushButton('Hello world1')
    #     helloWorldButton.toolTip = \
    #         "Print 'Hello world' in standard ouput."
    #     self.layout.addWidget(helloWorldButton)
    #     helloWorldButton.connect('clicked(bool)',
    #                              self.onHelloWorldButtonClicked)

    # # Add vertical spacer

    #     self.layout.addStretch(1)

    # # Set local var as instance attribute

    #     self.helloWorldButton = helloWorldButton

    # def onHelloWorldButtonClicked(self):
    #     print 'Hello World !'

    # # (Insert Section B text here)
    # # (be sure to match indentation of the rest of this
    # # code)

    #     qt.QMessageBox.information(slicer.util.mainWindow(),
    #                                'Slicer Python', 'Hello World!')

    def onTreeItemDoubleClicked(self, item, index):
        print str(index) + ',' + item.text(0) + ',' + item.text(1)
        # slicer.util.loadScene("/Users/lichuan/Desktop/subjects/bert/slicerBertScene.mrml")
        cu = BaseDAO.ctkDicomConnect.cursor()
        try:
            cu.execute('SELECT Foldername FROM Patients_extend where Patient_UID = ?',(int(item.text(0)),))
            res = cu.fetchone()


            # print "clearn"+str(res)
            # folder = PathDao.freesurferPath+res[0]
            # print folder
            # fsFolder = folder+'/data'
            # # for the_file in os.listdir(folder):
            # #     file_path = os.path.join(folder, the_file)
            # shutil.rmtree(fsFolder) 
            # # tempFilepath = folder+'/'+PathDao.tempfileName
            # # tempfile = open(tempFilepath, 'a')
            # # tempfile.truncate()
            # if not os.path.exists(fsFolder): os.makedirs(fsFolder)

            folder = PathDao.freesurferPath+res[0]+'/data'
            #add patient name and result in path
            current_path = folder + '/'+'bert'
            self.loadResultScene(current_path,True)
        except:
            print 'get patients extend list error'
            traceback.print_exc()
        finally:
            cu.close()


     

    def loadResultScene(self,path,init):     
        # if init , then clear the scene
        if init:
            slicer.mrmlScene.Clear(0)
        ln = slicer.util.getNode(pattern='vtkMRMLLayoutNode*')
        ln.SetViewArrangement(1)
        #load the volumn
        print path
        volumn_path = path + '/mri/brain.mgz'
        slicer.util.loadVolume(volumn_path)
        #load model
        lh_model_path = path + '/surf/lh.white'
        rh_model_path = path + '/surf/rh.white'
        # self.loadResultModel(lh_model_path)
        # self.loadResultModel(rh_model_path)
        #load label
        lh_label_path = path + '/label/lh.aparc.annot'
        rh_label_path = path + '/label/rh.aparc.annot'
        # self.loadResultLabel(lh_label_path,'lh')
        # self.loadResultLabel(rh_label_path,'rh')
        self.loadResultModel(lh_model_path,lh_label_path,'lh')
        self.loadResultModel(rh_model_path,rh_label_path,'rh')

        
    def loadResultModel(self,mpath,lpath,name):   
        from slicer import app
        from vtk import vtkCollection
        print mpath     
        slicer.util.loadModel(mpath)
        model_id = slicer.util.getNode(name).GetID()
        print model_id
        properties = {'fileName':lpath, 'modelNodeId':model_id}
        filetype = 'ScalarOverlayFile'
        success = app.coreIOManager().loadNodes(filetype, properties)
        print success


    def onReload(self, moduleName='ThicknessAnalyze'):
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

        parent = slicer.util.findChildren(name='ThicknessAnalyze Reload'
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


# module PatientDao

class PatientDao:

    def __init__(self):
        print 'init PatientDAO'

    #TODO 
    #update the sql
    def getNormalList(self,agelow,agehigh,sex,count):
        print str(agelow)+","+str(agehigh)+","+sex+","+str(count)
        cu = BaseDAO.ctkDicomConnect.cursor()
        try:
            if sex == 'All':
                cu.execute("SELECT Patient_UID,PatientsName,PatientsAGE,PatientsSex,Foldername FROM Patients_extend where Status = 2 and PatientsAge <= ? and PatientsAge >= ? and IsNormal=1  limit ?",(agehigh,agelow,count,))
            elif sex == 'Male':
                cu.execute("SELECT Patient_UID,PatientsName,PatientsAGE,PatientsSex,Foldername FROM Patients_extend where Status = 2 and PatientsAge <= ? and PatientsAge >= ? and PatientsSex = 'M' and IsNormal=1  limit ?",(agehigh,agelow,count,))
            elif sex == 'Female':
                cu.execute("SELECT Patient_UID,PatientsName,PatientsAGE,PatientsSex,Foldername FROM Patients_extend where Status = 2 and PatientsAge <= ? and PatientsAge >= ? and PatientsSex = 'F' and IsNormal=1  limit ?",(agehigh,agelow,count,))

            res = cu.fetchall()
            return res
        except:
            print 'get normal list error'
            traceback.print_exc()
        finally:
            cu.close()

    def getSResultList(self):
        cu = BaseDAO.ctkDicomConnect.cursor()
        try:
            cu.execute('SELECT Patient_UID,PatientsName,PatientsAGE,IsNormal FROM Patients_extend where Status = 2')
            res = cu.fetchall()
            resList = []
            # cannot update tuple using this way , have to update the list component to display text or change the tuple to list
            for resData in res:
                resData = list(resData)
                text = self.getGroupText(resData[3])
                print "group text:"+text
                resData[3] = text 
                resList.append(resData)


            # print "clearn"+str(res)
            # folder = PathDao.freesurferPath+res[0]
            # print folder
            # fsFolder = folder+'/data'
            # # for the_file in os.listdir(folder):
            # #     file_path = os.path.join(folder, the_file)
            # shutil.rmtree(fsFolder) 
            # # tempFilepath = folder+'/'+PathDao.tempfileName
            # # tempfile = open(tempFilepath, 'a')
            # # tempfile.truncate()
            # if not os.path.exists(fsFolder): os.makedirs(fsFolder)
            return resList
        except:
            print 'get patients extend list error'
            traceback.print_exc()
        finally:
            cu.close()
        # self.patient = Patient('Li Gang')
        # return self.patient.scan_result_list

    def getGroupText(self,code):
        if code == 0:
            return 'Patient'
        elif code == 1:
            return 'Normal'
        else:
            return ''

# class ScanResult:

#     def __init__(self, name, file_path):
#         self.name = name
#         self.file_path = file_path
#         print 'init ScanResult'


# class Patient:

#     def __init__(self, name):
#         self.name = name
#         self.initResultList()

#     def initResultList(self):
#         scan1 = ScanResult('2013-10-20', 'bert')
#         scan2 = ScanResult('2012-11-21', 'bert')
#         scan3 = ScanResult('2012-11-20', 'bert')
#         scan4 = ScanResult('2011-11-20', 'bert')
#         self.scan_result_list = []
#         self.scan_result_list.append(scan1)
#         self.scan_result_list.append(scan2)
#         self.scan_result_list.append(scan3)
#         self.scan_result_list.append(scan4)

