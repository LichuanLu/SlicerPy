#!/usr/bin/python
# -*- coding: utf-8 -*-
from __main__ import vtk, qt, ctk, slicer

import sys
sys.path.append('/dev_lic/SlicerPy/helloPython/code')
from BrainASUtils import CusUtils

#
# HelloSharpen
#

class RootModule:

    def __init__(self, parent):
        parent.title = 'RootModule'
        parent.categories = ['BrainAS']
        parent.dependencies = []
        parent.contributors = ['Lichuan Lu'
                               , 'Xiang Li']  # replace with "Firstname Lastname (Org)"
        parent.helpText = \
            """
    help text of RootModule
    """
        parent.acknowledgementText = \
            """
    acknowledgementText of RootModule"""  # replace with organization, grant and thanks.
        self.parent = parent


#
# qHelloPythonWidget
#

class RootModuleWidget:

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

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)  
        self.reloadButton = qt.QPushButton('Reload')
        self.reloadButton.toolTip = 'Reload this module.'
        self.reloadButton.name = 'RootModule Reload'
        self.layout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)
        self.initMainPage()      
        # self.testedit = qt.QLineEdit(self)
        # self.testedit.name = "mytestedit"
        # self.layout.addWidget(self.testedit)
       
    def onReload(self, moduleName='RootModule'):
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

        parent = slicer.util.findChildren(name='%s Reload'
                % moduleName)[0].parent()
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

    def initMainPage(self):
        if Login().exec_() == qt.QDialog.Accepted:
            print Login.role
            if(Login.role == "USER"):
                #hide widget
                print "hide widget"
                self.hideWidget("actionFileAddData")
                self.hideWidget("actionFileSaveScene")
                self.hideWidget("actionEditApplicationSettings")
                self.hideWidget("actionWindowPythonInteractor")
                self.hideWidget("menuHelp")
                self.hideWidget("actionFileLoadData")
                self.hideWidget("actionFileSaveScene")
                self.hideWidget("actionViewExtensionsManager")
                self.hideWidget("actionWindowPythonInteractor")
                self.hideWidget("actionHelpKeyboardShortcuts")
                self.hideWidget("actionHelpInterfaceDocumentation")
                self.hideWidget("actionHelpBrowseTutorials")
                self.hideWidget("actionHelpSlicerPublications")
                self.hideWidget("actionHelpVisualBlog")
                self.hideWidget("actionHelpReportBugOrFeatureRequest")
                self.hideWidget("actionHelpAboutSlicerApp")
                #hide module selection toolbar
                self.toggleWidgetByClass(slicer.qSlicerModuleSelectorToolBar,'hidden')
            elif (Login.role == "ADMIN"):
                #show module selection toolbar
                self.toggleWidgetByClass(slicer.qSlicerModuleSelectorToolBar,'show')
        else:
            #print "slicer quit"
            cusUtils = CusUtils()
            thread.start_new_thread(cusUtils.timer, (1,1))  

      
    def toggleWidgetByClass(self,qtype,action):
        if action == "hidden":
            slicer.util.mainWindow().findChild(qtype).setVisible(False)
        else:
            slicer.util.mainWindow().findChild(qtype).setVisible(True)

    def hideWidget(self,wname):
        slicer.util.findChildren(name=wname)[0].setVisible(False)


class Login(qt.QDialog):
    def __init__(self):
        qt.QDialog.__init__(self)
        self.setWindowTitle('Login')
        self.resize(300, 150)
        grid = qt.QGridLayout()
        grid.setSpacing(5)

        #nameLayout = qt.QHBoxLayout(self)
        self.nameLabel = qt.QLabel(self)
        self.nameLabel.setText("Username:")
        self.leName = qt.QLineEdit(self)
        #nameLayout.addWidget(self.nameLabel)
        #nameLayout.addWidget(self.leName)


        #passLayout = qt.QHBoxLayout(self)
        self.passLabel = qt.QLabel(self)
        self.passLabel.setText("Password:")
        self.lePassword = qt.QLineEdit(self)
        self.lePassword.setEchoMode(qt.QLineEdit.Password)
        #passLayout.addWidget(self.passLabel)
        #passLayout.addWidget(self.lePassword)
        self.pbLogin = qt.QPushButton('Login', self)
        # self.pbCancel = qt.QPushButton('Cancel', self)
 
        self.pbLogin.clicked.connect(self.handleLogin)
        #self.pbCancel.clicked.connect(self.handleCancel)
        #layout = qt.QVBoxLayout(self)
        #layout.addLayout(nameLayout)
        #layout.addLayout(passLayout)
 
        #buttonLayout = qt.QHBoxLayout(self)
        #buttonLayout.addStretch(1)
        #buttonLayout.addWidget(self.pbLogin)
        #buttonLayout.addWidget(self.pbCancel)
 
        #layout.addLayout(buttonLayout)
        grid.addWidget(self.nameLabel, 1, 0)
        grid.addWidget(self.leName, 1, 1)

        grid.addWidget(self.passLabel, 2, 0)
        grid.addWidget(self.lePassword, 2, 1)

        grid.addWidget(self.pbLogin, 3, 1)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)
        self.setLayout(grid)
        #--------

        #self.textName = qt.QLineEdit(self)
        #self.textPass = qt.QLineEdit(self)
        #self.buttonLogin = qt.QPushButton('Login', self)
        #self.buttonLogin.clicked.connect(self.handleLogin)
        #layout = qt.QVBoxLayout(self)
        #layout.addWidget(self.textName)
        #layout.addWidget(self.textPass)
        #layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.leName.text == 'user' and self.lePassword.text == 'tester'):
            Login.role = "USER"
            self.accept()
        elif (self.leName.text == 'admin' and self.lePassword.text == 'admin'):
            Login.role = "ADMIN"
            self.accept()
        else:
            qt.QMessageBox.warning(
                self, 'Error', 'Bad user or password')
    def handleCancel(self):
        cusUtils = CusUtils()
        thread.start_new_thread(cusUtils.timer, (1,1)) 




