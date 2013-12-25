#!/usr/bin/python
# -*- coding: utf-8 -*-

from __main__ import vtk, qt, ctk, slicer
# import sys
# sys.path.append('/dev_lic/SlicerPy/helloPython/code')
# import PatientDaoModule

# cannot import , need investigates
# from PatientDao import PatientDao,ScanResult,Patient

#
# Helloing class
#

class Helloing:

    def __init__(self, parent):
        parent.title = 'Helloing'
        parent.categories = ['test1']
        parent.dependencies = []
        parent.contributors = ['Jean-Christophe Fillion-Robin (Kitware)'
                               , 'Steve Pieper (Isomics)',
                               'Sonia Pujol (BWH)']  # replace with "Firstname Lastname (Org)"
        parent.helpText = \
            """
    Example of scripted loadable extension for the HelloPython tutorial.
    """
        parent.acknowledgementText = \
            """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.,
Steve Pieper, Isomics, Inc., and Sonia Pujol, Brigham and Women's Hospital and was 
partially funded by NIH grant 3P41RR013218-12S1 (NAC) and is part of the National Alliance 
for Medical Image Computing (NA-MIC), funded by the National Institutes of Health through the 
NIH Roadmap for Medical Research, Grant U54 EB005149."""  # replace with organization, grant and thanks.
        self.parent = parent


#
# qHelloingWidget
#

class HelloingWidget:

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

        self.reloadButton = qt.QPushButton('Reload')
        self.reloadButton.toolTip = 'Reload this module.'
        self.reloadButton.name = 'Helloing Reload'
        self.layout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)

    # Add vertical spacer

        self.layout.addStretch(1)

        self.qt_scan_result_list = qt.QTreeWidget()

    # descending order as default

        self.qt_scan_result_list.setSortingEnabled(1)
        self.qt_scan_result_list.setHeaderLabels(['name', 'file_path'])
        patient_dao = PatientDao()
        scan_results = patient_dao.getSResultList()
        item_list = []
        for result in scan_results:
            print result.name + ',' + result.file_path
            item = qt.QTreeWidgetItem([result.name, result.file_path])
            item_list.append(item)

        # item.content = result

        self.qt_scan_result_list.insertTopLevelItems(0, item_list)

    # add double click handler

        self.qt_scan_result_list.connect('itemDoubleClicked (QTreeWidgetItem *,int)'
                , self.onTreeItemDoubleClicked)
        self.layout.addWidget(self.qt_scan_result_list)

    # Add vertical spacer

        self.layout.addStretch(1)

    # Collapsible button
    # sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    # sampleCollapsibleButton.text = "A collapsible button"
    # self.layout.addWidget(sampleCollapsibleButton)

    # Layout within the sample collapsible button
    # sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # HelloWorld button
    # (Insert Section A text here)
    # (be sure to match indentation of the rest of this
    # code)
    # HelloWorld button

        helloWorldButton = qt.QPushButton('Hello world1')
        helloWorldButton.toolTip = \
            "Print 'Hello world' in standard ouput."
        self.layout.addWidget(helloWorldButton)
        helloWorldButton.connect('clicked(bool)',
                                 self.onHelloWorldButtonClicked)

    # Add vertical spacer

        self.layout.addStretch(1)

    # Set local var as instance attribute

        self.helloWorldButton = helloWorldButton

    def onHelloWorldButtonClicked(self):
        print 'Hello World !'

    # (Insert Section B text here)
    # (be sure to match indentation of the rest of this
    # code)

        qt.QMessageBox.information(slicer.util.mainWindow(),
                                   'Slicer Python', 'Hello World!')

    def onTreeItemDoubleClicked(self, item, index):
        print str(index) + ',' + item.text(0) + ',' + item.text(1)
        # slicer.util.loadScene("/Users/lichuan/Desktop/subjects/bert/slicerBertScene.mrml")
        base_path = "C:\\subjects\\data"
        #add patient name and result in path
        current_path = base_path + '/'+item.text(1)
        self.loadResultScene(current_path,True)

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


    def onReload(self, moduleName='Helloing'):
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

        parent = slicer.util.findChildren(name='Helloing Reload'
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

    def getSResultList(self):
        self.patient = Patient('Li Gang')
        return self.patient.scan_result_list


class ScanResult:

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        print 'init ScanResult'


class Patient:

    def __init__(self, name):
        self.name = name
        self.initResultList()

    def initResultList(self):
        scan1 = ScanResult('2013-10-20', '45')
        scan2 = ScanResult('2012-11-21', '47')
        scan3 = ScanResult('2012-11-20', '48')
        scan4 = ScanResult('2011-11-20', '49')
        self.scan_result_list = []
        self.scan_result_list.append(scan1)
        self.scan_result_list.append(scan2)
        self.scan_result_list.append(scan3)
        self.scan_result_list.append(scan4)

