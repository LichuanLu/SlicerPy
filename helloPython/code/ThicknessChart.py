#!/usr/bin/python
# -*- coding: utf-8 -*-
from __main__ import vtk, qt, ctk, slicer
from DicomDAO import BaseDAO
from BrainASUtils import PathDao

import Charting
import math
import linecache
import re



#
# ThicknessChart
#

class ThicknessChart:

    def __init__(self, parent):
        parent.title = 'ThicknessChart'
        parent.categories = ['BrainAS']
        parent.dependencies = []
        parent.contributors = ['Lichuan Lu'
                               , 'Xiang Li (Isomics)']  # replace with "Firstname Lastname (Org)"
        parent.helpText = \
            """
    help text of ThicknessChart module
    """
        parent.acknowledgementText = \
            """
    acknowledgementText of ThicknessChart module"""  # replace with organization, grant and thanks.
        parent.icon = qt.QIcon(':Icons/Medium/SlicerAddScalarOverlay.png')

        self.parent = parent


#
# qThicknessChartWidget
#

class ThicknessChartWidget:

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

        

    # chart code
    # Change the layout to one that has a chart.  This created the ChartView

        ln = slicer.util.getNode(pattern='vtkMRMLLayoutNode*')
        ln.SetViewArrangement(80)

    # Get the first ChartView node

        # cvns = slicer.util.getNodes(pattern='vtkMRMLChartViewNode*')
        # cvn1 = cvns.get('ChartView1')
        # cvn2 = cvns.get('ChartView2')
        # cn1 = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
        # cn1.SetProperty('default','cusWrapData',self.generateChartString('group','p1','g1'))
        # cvn1.SetChartNodeID(cn1.GetID())

        # cn2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
        # cn2.SetProperty('default','cusWrapData',self.generateChartString('zscore','p1','g1'))
        # cvn2.SetChartNodeID(cn2.GetID())

        self.reloadButton = qt.QPushButton('Reload')
        self.reloadButton.toolTip = 'Reload this module.'
        self.reloadButton.name = 'ChartTest Reload'
        self.layout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)

        #self.generateChartString('group','p1','g1')


        self.grid = qt.QGridLayout()
        self.grid.setSpacing(3)

        self.ageLabel = qt.QLabel(self)
        self.ageLabel.setText("Age From:")
        self.ageLow = qt.QLineEdit(self)
        self.ageLow.setText('0')
        self.ageLabel2 = qt.QLabel(self)
        self.ageLabel2.setText("To")
        self.ageHigh = qt.QLineEdit(self)
        self.ageHigh.setText('200')

        self.sexLabel = qt.QLabel(self)
        self.sexLabel.setText("Sex:")
        self.sexCombo = qt.QComboBox()
        self.sexCombo.addItem("All")
        self.sexCombo.addItem("Male")
        self.sexCombo.addItem("Female")
        #self.sexCombo.connect('activated(str)',self.onSexActivated)
        #self.sexCombo.activated[str].connect(self.onSexActivated)        
        self.countLabel = qt.QLabel(self)
        self.countLabel.setText('Count:')
        self.countEdit = qt.QLineEdit(self)
        self.countEdit.setText('10')

        self.searchButton = qt.QPushButton('Search')
        self.searchButton.toolTip = 'Search Normal Group'
        self.searchButton.connect('clicked()',self.onSearchClicked)

        self.grid.addWidget(self.ageLabel, 1, 0)
        self.grid.addWidget(self.ageLow, 1, 1)
        self.grid.addWidget(self.ageLabel2,1,2)
        self.grid.addWidget(self.ageHigh,1,3)


        self.grid.addWidget(self.sexLabel, 2, 0)
        self.grid.addWidget(self.sexCombo, 2,1)

        self.grid.addWidget(self.countLabel,3,0)
        self.grid.addWidget(self.countEdit,3,1)

        self.grid.addWidget(self.searchButton, 3, 3)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)
        self.layout.addLayout(self.grid)

        self.font = qt.QFont()
        self.font.setBold(True)
        self.font.setPixelSize(15)
        self.listTitle = qt.QLabel("Normal Record List:")
        self.listTitle.setFont(self.font)
        self.layout.addWidget(self.listTitle)

        self.normalRecordList = qt.QTreeWidget()

    # descending order as default

        self.normalRecordList.setSortingEnabled(1)
        self.normalRecordList.setHeaderLabels(['PUID','Name','Age','Sex'])
        self.normalRecordListRefresh()

        self.layout.addWidget(self.normalRecordList)

       
        self.listTitle2 = qt.QLabel("Patient Record List:")
        self.listTitle2.setFont(self.font)
        self.layout.addWidget(self.listTitle2)

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

    # add two button for left brain and right brain and one label for the result

        self.chartHandleLabel = qt.QLabel("")
        self.chartHandleLabel.setStyleSheet('color: red')
        self.layout.addWidget(self.chartHandleLabel)

        self.buttonLayout = qt.QHBoxLayout()

        self.leftBrainBtn = qt.QPushButton('Left Brain Analyze')
        self.leftBrainBtn.toolTip = 'Left Brain Analyze'
        self.leftBrainBtn.name = 'Left-Brain-Analyze-Button'
        self.buttonLayout.addWidget(self.leftBrainBtn)
        self.leftBrainBtn.connect('clicked()', self.leftBrainBtnClicked)

        self.rightBrainBtn = qt.QPushButton('Right Brain Analyze')
        self.rightBrainBtn.toolTip = 'Right Brain Analyze'
        self.rightBrainBtn.name = 'Right-Brain-Analyze-Button'
        self.buttonLayout.addWidget(self.rightBrainBtn)
        self.rightBrainBtn.connect('clicked()', self.rightBrainBtnClicked)

        self.layout.addLayout(self.buttonLayout)

    def leftBrainBtnClicked(self):
        print "leftBrainBtnClicked"
        self.chartHandleLabel.setText("")
        selectedItem = self.qt_scan_result_list.currentItem()
        try:
            pid = int(selectedItem.text(0))
            print str(selectedItem.text(0))
            print str(selectedItem.text(1))
        except:
            print "Warning: Please select one record from the Patient record list"
            self.chartHandleLabel.setText("Warning: Please select one record from the Patient record list!")
            traceback.print_exc()
            return
        try:
            self.brainChartAnalyze("Left",pid)
        except:
            self.chartHandleLabel.setText("Error:brainChartAnalyze left")
            traceback.print_exc()
        self.chartHandleLabel.setText("Success:Analyze Left Brain")

    def rightBrainBtnClicked(self):
        print "rightBrainBtnClicked"
        self.chartHandleLabel.setText("")
        selectedItem = self.qt_scan_result_list.currentItem()
        try:
            pid = int(selectedItem.text(0))
            print str(selectedItem.text(0))
            print str(selectedItem.text(1))
        except:
            print "Warning: Please select one record from the Patient record list"
            self.chartHandleLabel.setText("Warning: Please select one record from the Patient record list!")
            traceback.print_exc()
            return
        try:
            self.brainChartAnalyze("Right",pid) 
        except:
            self.chartHandleLabel.setText("Error:brainChartAnalyze right")
            traceback.print_exc()
        self.chartHandleLabel.setText("Success:Analyze Right Brain")


    def brainChartAnalyze(self,brainType,pid):
        print brainType+","+str(pid)
        gid = []


        root = self.normalRecordList.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item_id = item.text(0) # text at first (0) column
            print str(item_id)
            gid.append(int(item_id))


        gdata = GroupData(gid)   


        cvns = slicer.util.getNodes(pattern='vtkMRMLChartViewNode*')
        self.cvn1 = cvns.get('ChartView1')
        self.cvn2 = cvns.get('ChartView2')
        cn1 = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
        cn1.SetProperty('default','cusWrapData',self.generateChartString('group',pid,gdata,brainType))
        self.cvn1.SetChartNodeID(cn1.GetID())

        cn2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
        cn2.SetProperty('default','cusWrapData',self.generateChartString('zscore',pid,gdata,brainType))
        self.cvn2.SetChartNodeID(cn2.GetID())

    #TODO run the chart function
    def onTreeItemDoubleClicked(self,index):
        print "onTreeItemDoubleClicked"

    def normalRecordListRefresh(self):
        self.normalRecordList.clear()
        print self.ageLow.text+","+self.ageHigh.text+","+self.sexCombo.currentText+','+self.countEdit.text
        patient_dao = PatientDao()
        if(self.ageLow.text == ""):
            ageLowNum = 0
        else:
            ageLowNum = int(self.ageLow.text)
        if(self.ageHigh.text == ""):
            ageHighNum = 200
        else:
            ageHighNum = int(self.ageHigh.text)
        if(self.countEdit.text == ""):
            countNum = 10
        else:
            countNum = int(self.countEdit.text)

        scan_results = patient_dao.getNormalList(ageLowNum,ageHighNum,self.sexCombo.currentText,countNum)
        if(scan_results != ""):
            item_list = []
            for result in scan_results:
                #print str(result[0]) + ',' + result[1]+','+result[2]+','+result[3]
                item = qt.QTreeWidgetItem([result[0], result[1],result[2],result[3]])
                item_list.append(item)

            # item.content = result

            self.normalRecordList.insertTopLevelItems(0, item_list)

    def onSearchClicked(self):
        print "search click"
        self.normalRecordListRefresh()
    
    # def onSexActivated(self,text):
    #     print "sex:"+text
       
    def onReload(self, moduleName='ThicknessChart'):
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


    def generateColorList(self,highList,lowList,dataList):
        overHighColor = '#FF0000'
        overLowColor = '#0000FF'
        normalColor = '#C5B47F'
        colorList = []
        for index,item in enumerate(dataList):
            if(float(item) > float(highList[index])):
                colorList.append(overHighColor)
            elif (float(item) < float(lowList[index])):
                colorList.append(overLowColor)
            else:
                colorList.append(normalColor)
        if len(colorList) > 0:
            resString = 'seriesColors:'+ str(colorList)+','
        else:
            resString = ""
        print "color string:"+resString
        return resString


    def generateChartString(self,charttype,pid,gdata,brainType):
        cu = BaseDAO.ctkDicomConnect.cursor()
        pfileData = ""
        print "brainType:"+brainType
        try:
            cu.execute('SELECT Foldername FROM Patients_extend where Patient_UID = ?',(pid,))
            res = cu.fetchone()
            print "generateChartString res pid:"+str(res)+","+str(pid)
            if res:
                if brainType == "Left":
                    path = PathDao.freesurferPath+res[0]+"/data/patient/stats/lh.aparc.a2009s.stats"
                    print "patient path:"+path
                    pfileData = ReadFile(path)
                elif brainType == "Right":
                    path = PathDao.freesurferPath+res[0]+"/data/patient/stats/rh.aparc.a2009s.stats"
                    print "patient path:"+path
                    pfileData = ReadFile(path)

        except:
            print 'generateChartString error'
            traceback.print_exc()
            return
        finally:
            cu.close()
        print "generateChartString pfileData:"+str(len(pfileData.thickAvgList))
        # gdata = GroupData(gid)   
        if charttype == "group":
            print "group"
            #each group only one instance is enough
            groupChartDao = GroupChartDao(gdata)
            groupChartDao.setPatientChartData(pfileData.thickAvgList)
            groupChartDao.setAreaList(pfileData.areaList)
            localPatientChartData = groupChartDao.getPatientChartData(pid)
            localGroupChartHighData = groupChartDao.getGroupChartHighData(brainType)
            localGroupChartLowData = groupChartDao.getGroupChartLowData(brainType)

            result = "var data = ["
            result = result + self.generateDataString(localPatientChartData) + "," + self.generateDataString(localGroupChartHighData)+","+self.generateDataString(localGroupChartLowData)+"];"
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
            '''+self.generateColorList(localGroupChartHighData,localGroupChartLowData,localPatientChartData)+'''
            series:[
                {
                    pointLabels: {
                        show: true
                    },
                    renderer: $.jqplot.BarRenderer,
                    label: 'Volumes',
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
                        color:'#4BB2C5',
                        smooth: true
                    }
                },
                {
                    rendererOptions: {
                        color:'#EAA228',
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
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions:{ 
                        angle: -90
                      }
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
            zscoreChartDao = ZscoreChartDao(gdata)
            zscoreChartDao.setAreaList(pfileData.areaList)
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
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions:{ 
                        angle: -90
                      }
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


class GroupData:
    def __init__ (self,gid):
        self.gid = gid
        self.leftFiles = []
        self.rightFiles = []
        print 'init group chart dao'
        if (len(self.gid) > 0):
            cu = BaseDAO.ctkDicomConnect.cursor()
            try:
                sql="SELECT Foldername FROM Patients_extend where Patient_UID in ({seq})".format(seq=','.join(['?']*len(gid)))
                print "GroupData sql:"+sql
                cu.execute(sql, gid)
                res = cu.fetchall()
                if len(res) > 0:
                    for gfolder in res:
                        self.leftFiles.append(ReadFile(PathDao.freesurferPath+gfolder[0]+"/data/patient/stats/lh.aparc.a2009s.stats"))
                        self.rightFiles.append(ReadFile(PathDao.freesurferPath+gfolder[0]+"/data/patient/stats/rh.aparc.a2009s.stats"))
            except:
                print 'get normal list error'
                #traceback.print_exc()
            finally:
                cu.close()
                print "GroupData:"+str(len(self.leftFiles))+","+str(len(self.rightFiles))

#create this class for save the file data in mem, use redis?
class GroupChartDao:
    def __init__ (self,gdata):
        self.gdata = gdata
#获取组分析数据的最高值，数据的组成是字符串的数组
    def getGroupChartHighData(self,brainType):
        try:
            if brainType == "Left":
                fileList = self.gdata.leftFiles
                length = len(fileList[0].thickAvgList)
            elif brainType == "Right":
                fileList = self.gdata.rightFiles
                length = len(fileList[0].thickAvgList)
            print "lenght:"+str(length)
            self.ghdata = []
            for i in range(length):
                temp = 0
                for datafile in fileList:
                    tempData = float(datafile.thickAvgList[i])
                    if tempData > temp:
                        temp = tempData
                self.ghdata.append(str(temp))
        except:
            print "getGroupChartHighData error"
            traceback.print_exc()
            self.ghdata = ['3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','3.358','4.23','5.23','4.11','3.12','4.12','4.33']
        print "self.ghdata:"+str(len(self.ghdata)) 
        return self.ghdata 
#获取组分析数据的最低值，数据的组成是字符串的数组
    def getGroupChartLowData(self,brainType):
        try:
            if brainType == "Left":
                fileList = self.gdata.leftFiles
                length = len(fileList[0].thickAvgList)
            elif brainType == "Right":
                fileList = self.gdata.rightFiles
                length = len(fileList[0].thickAvgList)
            print "lenght:"+str(length)
            self.gldata = []
            for i in range(length):
                temp = 10
                for datafile in fileList:
                    tempData = float(datafile.thickAvgList[i])
                    if tempData < temp:
                        temp = tempData
                self.gldata.append(str(temp))
        except:
            print "getGroupChartLowData error"
            traceback.print_exc()
            self.gldata = ['1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','1.358','0.358','1.255','1.11','0.12','2.12','0.23']
        print "self.gldata:"+str(len(self.gldata)) 
        return self.gldata 
#获取病人数据值
    def getPatientChartData(self,pid):
        return self.pdata
    def setPatientChartData(self,data):
        self.pdata = data
#脑区对应的名称
    def getAreaList(self):
        return self.arealist
    def setAreaList(self,data):
        self.arealist = data


class ZscoreChartDao:
    def __init__ (self,gdata):
        self.gdata = gdata
        print 'init zscore chart dao'
#获得zscore数值
    def getZscore(self):
        self.gdata = ['-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','-1.24','-2.23','1.23','2.11','1.12','2.12','0.03']
        print len(self.gdata)
        return self.gdata 
#脑区对应的名称
    def getAreaList(self):
        return self.arealist
    def setAreaList(self,data):
        self.arealist = data

#小心内存泄漏，没有clearcache
class ReadFile:
    def __init__ (self,filepath):
        print "filepath:"+filepath
        self.path = filepath
        self.file = linecache.getlines(filepath)[54:127]
        print self.file
        self.parseFile()
    def parseFile(self):
        try: 
            self.areaList = []
            self.thickAvgList = []
            for line in self.file:
                strs = re.split(r'\s+',line)
                self.areaList.append(strs[0])
                self.thickAvgList.append(strs[4])
            print len(self.thickAvgList)
            print len(self.areaList)
        except:
            print "parse file error"
            traceback.print_exc()
        finally:
            linecache.clearcache()


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
                cu.execute("SELECT Patient_UID,PatientsName,PatientsAGE,PatientsSex,Foldername FROM Patients_extend where Status = 2 and PatientsAge <= ? and PatientsAge >= ? and IsNormal=1 limit ?",(agehigh,agelow,count))
            elif sex == 'Male':
                cu.execute("SELECT Patient_UID,PatientsName,PatientsAGE,PatientsSex,Foldername FROM Patients_extend where Status = 2 and PatientsAge <= ? and PatientsAge >= ? and PatientsSex = 'M' and IsNormal=1 limit ?",(agehigh,agelow,count))
            elif sex == 'Female':
                cu.execute("SELECT Patient_UID,PatientsName,PatientsAGE,PatientsSex,Foldername FROM Patients_extend where Status = 2 and PatientsAge <= ? and PatientsAge >= ? and PatientsSex = 'F' and IsNormal=1 limit ?",(agehigh,agelow,count))

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

            return resList
        except:
            print 'get patients extend list error'
            traceback.print_exc()
        finally:
            cu.close()
       

    def getGroupText(self,code):
        if code == 0:
            return 'Patient'
        elif code == 1:
            return 'Normal'
        else:
            return ''

