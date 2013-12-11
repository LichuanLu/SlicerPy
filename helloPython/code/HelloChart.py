#!/usr/bin/python
# -*- coding: utf-8 -*-
from __main__ import vtk, qt, ctk, slicer
import Charting
import math



#
# HelloSharpen
#

class HelloChart:

    def __init__(self, parent):
        parent.title = 'HelloChart'
        parent.categories = ['test']
        parent.dependencies = []
        parent.contributors = ['Jean-Christophe Fillion-Robin (Kitware)'
                               , 'Steve Pieper (Isomics)',
                               'Sonia Pujol (BWH)']  # replace with "Firstname Lastname (Org)"
        parent.helpText = \
            """
    Example of scripted loadable extension for the HelloSharpen tutorial.
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
# qHelloPythonWidget
#

class HelloChartWidget:

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
        self.reloadButton.name = 'HelloChart Reload'
        self.layout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)

    # chart code
    # Change the layout to one that has a chart.  This created the ChartView

        ln = slicer.util.getNode(pattern='vtkMRMLLayoutNode*')
        ln.SetViewArrangement(24)

    # Get the first ChartView node

        cvn = slicer.util.getNode(pattern='vtkMRMLChartViewNode*')
        slicer.util.loadVolume('/Users/lichuan/Desktop/subjects/FA.nrrd')
        volumeNode = slicer.util.getNode(pattern='FA')

        # # Create another data array
        # dn3 = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        # a = dn3.GetArray()
        # a.SetNumberOfTuples(12)
        # x = range(0, 12)
        # for i in range(len(x)):
        #   a.SetComponent(i, 0, x[i]/4.0)
        #   a.SetComponent(i, 1, math.sin(x[i]/4.0))
        #   a.SetComponent(i, 2, 0)

        # # Create another ChartNode
        # cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

        # # Add data to the chart
        # cn.AddArray('Periodic', dn3.GetID())

        # # Configure properties of the Chart
        # cn.SetProperty('default', 'title', 'A bar chart')
        # cn.SetProperty('default', 'xAxisLabel', 'time')
        # cn.SetProperty('default', 'yAxisLabel', 'velocity')
        # cn.SetProperty('default', 'type', 'Bar');

        # # Set the chart to display
        # cvn.SetChartNodeID(cn.GetID())



        #--------------


        # dn6 = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        # a = dn6.GetArray()

        # a.SetNumberOfTuples(40)
        # for i in range(a.GetNumberOfTuples()):
        #   a.SetComponent(i, 0, 1)
        #   a.SetComponent(i, 1, (2.0*random.random() - 0.5) + 20.0)

        # # Create another data array
        # dn7 = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        # a = dn7.GetArray()

        # a.SetNumberOfTuples(25)
        # for i in range(20):
        #   a.SetComponent(i, 0, 2)
        #   a.SetComponent(i, 1, 2.0*(2.0*random.random()-1.0) + 27.0)
        # for i in range(5):
        #   a.SetComponent(20+i, 0, 2)
        #   a.SetComponent(20+i, 1, 10.0*(2.0*random.random()-1.0) + 27.0)

        # # Create another data array
        # dn8 = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        # a = dn8.GetArray()

        # a.SetNumberOfTuples(25)
        # for i in range(20):
        #   a.SetComponent(i, 0, 3)
        #   a.SetComponent(i, 1, 3.0*(2.0*random.random()-1.0) + 24.0)
        # for i in range(5):
        #   a.SetComponent(20+i, 0, 2)
        #   a.SetComponent(20+i, 1, 10.0*(2.0*random.random()-1.0) + 24.0)
        
        # # Create another ChartNode
        # cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

        # # Add data to the chart
        # cn.AddArray('Controls', dn6.GetID())
        # cn.AddArray('Group A', dn7.GetID())
        # cn.AddArray('Group B', dn8.GetID())

        # # Configure properties of the Chart
        # cn.SetProperty('default', 'title', 'A box chart')
        # cn.SetProperty('default', 'xAxisLabel', 'population')
        # cn.SetProperty('default', 'xAxisType', 'categorical')
        # cn.SetProperty('default', 'yAxisLabel', 'size (ml)')
        # cn.SetProperty('default', 'type', 'Box');

        # # Set the chart to display
        # cvn.SetChartNodeID(cn.GetID())
        #-----------------
         # Create arrays of data
        dn = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        a = dn.GetArray()
        a.SetNumberOfTuples(600)
        x = range(0, 600)
        for i in range(len(x)):
          a.SetComponent(i, 0, x[i]/50.0)
          a.SetComponent(i, 1, math.sin(x[i]/50.0))
          a.SetComponent(i, 2, 0)

        dn2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        a = dn2.GetArray()
        a.SetNumberOfTuples(600)
        x = range(0, 600)
        for i in range(len(x)):
          a.SetComponent(i, 0, x[i]/50.0)
          a.SetComponent(i, 1, math.cos(x[i]/50.0))
          a.SetComponent(i, 2, 0)

        # Create the ChartNode, 
        cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

        # Add data to the Chart
        cn.AddArray('A double array', dn.GetID())
        cn.AddArray('Another double array', dn2.GetID())

        # Configure properties of the Chart
        cn.SetProperty('default', 'title', 'A simple chart with 2 curves')
        cn.SetProperty('default', 'xAxisLabel', 'Something in x')
        cn.SetProperty('default', 'yAxisLabel', 'Something in y')
        cn.SetProperty('default', 'type', 'Bar')
        cn.SetProperty('Another double array', 'type', 'Line')
        cn.SetProperty('A double array', 'color', '#fe7d20')
        # Set the chart to display
        cvn.SetChartNodeID(cn.GetID())

    # logic = ChartingLogic()

        out = volumeNode.GetImageData()
        print out

    def onReload(self, moduleName='HelloChart'):
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
