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
        ln.SetViewArrangement(80)

    # Get the first ChartView node

        cvns = slicer.util.getNodes(pattern='vtkMRMLChartViewNode*')
        #slicer.util.loadVolume('/Users/lichuan/Desktop/subjects/FA.nrrd')
        #volumeNode = slicer.util.getNode(pattern='FA')

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
        # dn = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        # a = dn.GetArray()
        # a.SetNumberOfTuples(600)
        # x = range(0, 600)
        # for i in range(len(x)):
        #   a.SetComponent(i, 0, x[i]/50.0)
        #   a.SetComponent(i, 1, math.sin(x[i]/50.0))
        #   a.SetComponent(i, 2, 0)

        # dn2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
        # a = dn2.GetArray()
        # a.SetNumberOfTuples(600)
        # x = range(0, 600)
        # for i in range(len(x)):
        #   a.SetComponent(i, 0, x[i]/50.0)
        #   a.SetComponent(i, 1, math.cos(x[i]/50.0))
        #   a.SetComponent(i, 2, 0)

        # # Create the ChartNode, 
        # cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

        # # Add data to the Chart
        # cn.AddArray('A double array', dn.GetID())
        # cn.AddArray('Another double array', dn2.GetID())

        # # Configure properties of the Chart
        # cn.SetProperty('default', 'title', 'A simple chart with 2 curves')
        # cn.SetProperty('default', 'xAxisLabel', 'Something in x')
        # cn.SetProperty('default', 'yAxisLabel', 'Something in y')
        # cn.SetProperty('default', 'type', 'Bar')
        # cn.SetProperty('Another double array', 'type', 'Line')
        # cn.SetProperty('A double array', 'color', '#fe7d20')
        # # Set the chart to display
        # cvn.SetChartNodeID(cn.GetID())
        #---------------------------------------
    # logic = ChartingLogic()

        # out = volumeNode.GetImageData()
        # print out
        # new function for the first chart ----------------------------------------------------
        cvn1 = cvns.get('ChartView1')
        cvn2 = cvns.get('ChartView2')
        cn1 = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
        cn1.SetProperty('default','cusWrapData',self.generateChartString('group','p1','g1'))
        cvn1.SetChartNodeID(cn1.GetID())

        cn2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
        cn2.SetProperty('default','cusWrapData',self.generateChartString('zscore','p1','g1'))
        cvn2.SetChartNodeID(cn2.GetID())



        
       
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

    def generateChartString(self,charttype,pid,gid):
        if charttype == "group":
            print "group"
            #each group only one instance is enough
            groupChartDao = GroupChartDao(gid)
            result = "var data = ["
            result = result + self.generateDataString(groupChartDao.getPatientChartData(pid)) + "," + self.generateDataString(groupChartDao.getGroupChartData())+"];"
            print "chart string:" + result
            result = result + "var xAxisTicks = " + str(groupChartDao.getAreaList()) + ";"
            print "chart string:" + result
            optionStr = ''' var options = { highlighter: {
                useAxesFormatters:false,
                formatString:'%.3g,%.3g'

            },
            cursor: {
                show: true,
                zoom: true,
            },
            title:'Cortex Thickness Group Analysis Chart',
            series:[
                {
                    pointLabels: {
                        show: true
                    },
                    renderer: $.jqplot.BarRenderer,
                    label: 'Volumes',
            '''+self.generateColorString()+'''
                    rendererOptions: {
                        varyBarColor: true,
                        barWidth: 15,
                        barPadding: -15,
                        barMargin: 0,
                        highlightMouseOver: false
                    }
                }, 
                {
                    rendererOptions: {
                    }
                }
            ],
            axesDefaults: {
                pad: 0
            },
            axes: {

                xaxis: {
                    label: 'Area Name',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks:xAxisTicks,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer
                },
                yaxis: {
                    label: 'Thickness(mm)',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    rendererOptions: {
                        forceTickAt0: true
                    }
                }
            },
            grid: {
                drawGridlines: true
            },
            legend: {
                show: true,
                labels:['Patient Data','Group Data']
            }
            }; '''
            print "option string:" + optionStr
            result += optionStr
            return result

        elif charttype == "zscore":
            print "zscore"
            zscoreChartDao = ZscoreChartDao(gid)
            result = "var data = ["
            result = result + self.generateDataString(zscoreChartDao.getZscore())+"];"
            print "chart string:" + result
            result = result + "var xAxisTicks = " + str(zscoreChartDao.getAreaList()) + ";"
            print "chart string:" + result
            optionStr = ''' var options = { highlighter: {
                show: true, 
                showLabel: true, 
                tooltipAxes: 'y'
            },
            cursor: {
                show: true,
                zoom: true,
            },
            title:'Cortex Thickness Zscore Analysis Chart',
            series:[
                {
                    rendererOptions: {
                    }
                }
            ],
            axesDefaults: {
                pad: 0
            },
            axes: {

                xaxis: {
                    label: 'Area Name',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks:xAxisTicks,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer
                },
                yaxis: {
                    label: 'Zscore',
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    rendererOptions: {
                        forceTickAt0: true
                    }
                }
            },
            grid: {
                drawGridlines: true
            },
            legend: {
                show: true,
                labels:['Zscore']
            }
            }; '''
            print "option string:" + optionStr
            result += optionStr
            return result

        else:
            print 'error'
            return ""  

    def generateDataString(self,data):
        result = "["
        a = ","
        print "data:"+str(data)
        result = result + a.join(data) + "]"
        return result

    def generateColorString(self):
        # sample: seriesColors: ['#dd8265', '#b17a65', '#6fb8d2', '#d8654f','#6fb8d2'],
        return ""


#create this class for save the file data in mem, use redis?
class GroupChartDao:
    def __init__ (self,gid):
        self.gid = gid
        print 'init group chart dao'
    def getGroupChartData(self):
        self.gdata = ['154.24','122.23','255.23','123.11','456.12','322.12']
        return self.gdata 
    def getPatientChartData(self,pid):
        pdata = ['167.42','245.24','345.23','100.23','450.12','232.44']
        return pdata
    def getAreaList(self):
        self.arealist = ['area1','area2','area3','area4','area5','area6']
        return self.arealist


class ZscoreChartDao:
    def __init__ (self,gid):
        self.gid = gid
        print 'init zscore chart dao'
    def getZscore(self):
        self.gdata = ['-1.24','-2.23','1.23','2.11','1.12','2.12']
        return self.gdata 
    # def getPatientChartData(self,pid):
    #     pdata = ['23.42','12.24','12.23','99.23','44.12','33.44']
    #     return pdata
    def getAreaList(self):
        self.arealist = ['area1','area2','area3','area4','area5','area6']
        return self.arealist
