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
            result = result + self.generateDataString(groupChartDao.getPatientChartData(pid)) + "," + self.generateDataString(groupChartDao.getGroupChartHighData())+","+self.generateDataString(groupChartDao.getGroupChartLowData())+"];"
            print "chart string:" + result
            result = result + "var xAxisTicks = " + str(groupChartDao.getAreaList()) + ";"
            print "chart string:" + result
            optionStr = ''' var options = { 
            highlighter: {
                show:true,
                useAxesFormatters:false,
                tooltipContentEditor:function (str,seriesIndex,pointIndex,plot) {
                    var label = plot.axes.xaxis._ticks[pointIndex*2+1].label;
                    if(seriesIndex == 1){
                        return "Group High-"+label+":"+plot.data[seriesIndex][pointIndex]
                    }
                    else if(seriesIndex == 2){
                        return "Group Low-"+label+":"+plot.data[seriesIndex][pointIndex]

                    }
                    else{
                        return "Patient-"+label+":"+plot.data[seriesIndex][pointIndex]

                    }                    
                }

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
                        smooth: true
                    }
                },
                {
                    rendererOptions: {
                        smooth: true
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
                labels:['Patient Data','Group Data High','Group Data Low']
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
            optionStr = ''' var options = { 
            highlighter: {
                show:true,
                useAxesFormatters:false,
                tooltipContentEditor:function (str,seriesIndex,pointIndex,plot) {
                    var label = plot.axes.xaxis._ticks[pointIndex*2+1].label;
                    
                        return "Zscore data-"+label+":"+plot.data[seriesIndex][pointIndex]
                                     
                }
            },
            cursor: {
                show: true,
                zoom: true,
            },
            title:'Cortex Thickness Zscore Analysis Chart',
            series:[
                {
                    rendererOptions: {
                        smooth: true
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
#获取组分析数据的最高值，数据的组成是字符串的数组
    def getGroupChartHighData(self):
        self.ghdata = ['184.24','322.23','355.23','123.11','426.12','182.12']
        return self.ghdata 
#获取组分析数据的最低值，数据的组成是字符串的数组
    def getGroupChartLowData(self):
        self.gldata = ['154.24','122.23','255.23','113.11','356.12','122.12']
        return self.gldata 
#获取病人数据值
    def getPatientChartData(self,pid):
        pdata = ['167.42','245.24','345.23','100.23','450.12','232.44']
        return pdata
#脑区对应的名称
    def getAreaList(self):
        self.arealist = ['area1','area2','area3','area4','area5','area6']
        return self.arealist


class ZscoreChartDao:
    def __init__ (self,gid):
        self.gid = gid
        print 'init zscore chart dao'
#获得zscore数值
    def getZscore(self):
        self.gdata = ['-1.24','-2.23','1.23','2.11','1.12','2.12']
        return self.gdata 
#脑区对应的名称
    def getAreaList(self):
        self.arealist = ['area1','area2','area3','area4','area5','area6']
        return self.arealist
