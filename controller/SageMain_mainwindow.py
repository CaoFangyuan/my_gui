from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import controller.forms
import model.ssh_engine
import controller.TSConfig_mainwindow
import controller.selectpath_mainwindow
import controller.FPAConfig_mainwindow
import controller.log_mainwindow
from controller import *
import os
import sys
import pexpect
import json
import re
import operator
import time



class SageMainController(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        #QMainWindow.setObjectName("Sage")
        self.form = controller.forms.sagemain.Ui_MainWindow()
        self.form.setupUi(self)
        #Make menu visible
        self.form.menuBar.setNativeMenuBar(False)
        #Incident of "Mode" combox changes
        self.form.Mode.currentIndexChanged['QString'].connect(self.ChangeToSecond)
        #Incident of Clicking "YES" button
        self.form.YES.clicked.connect(self.changeToTS)
        self.form.Import.clicked.connect(self.selectPath)
        self.form.Delete.clicked.connect(self.selectWarning)
        #self.form.Delete.clicked.connect(self.deleteData)
        self.form.Refresh.clicked.connect(self.refreshData)
        model.ssh_engine.exesensordirector()
        model.ssh_engine.RasToGui(model.ssh_engine.SAGE_HOME + 'src/modules/dpm/common/TrialInfo.json', model.ssh_engine.SAGE + 'model/')
        filename = model.ssh_engine.SAGE+'model/TrialInfo.json'
        systeminfo = model.ssh_engine.SAGE+'model/SystemInfo.json'
        
        # Set system infomation 
        with open(systeminfo,'r') as f_2:
            data=json.load(f_2)
        #self.refreshSystemInfo(data)
        #self.refreshThread = RefreshThread()
        #self.refreshThread._signal.connect(self.refreshSystemInfo)
        #self.refreshThread.start()
        
        # Define the data model 
        with open(filename) as f_1:
            self.trial = json.load(f_1)

        header = ['名称', '时间', '大小']
        self.model = MyTableModel(self.trial, header)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        # Set data model to Qtableview
        self.form.tableView.setModel(self.proxy)
        self.form.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.form.tableView.setSelectionMode(QTableView.ExtendedSelection)
        #self.form.tableView.resizeColumnsToContents()
        self.form.tableView.setColumnWidth(0,200)
        self.form.tableView.setColumnWidth(1,200)
        self.form.tableView.setColumnWidth(2,200)
        self.horizontalHeader = self.form.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.starMenu)
                
        #Action when click actionDownload_ErrorLog and actionUpdate_Firmware
        #self.form.actionDownload_Log.triggered.connect(self.change2Log)
        #self.form.actionUpdate_Firmware.triggered.connect(self.change2FirmwareUpdate)    
        #self.form.actionExperiment_setup.triggered.connect(self.change2SystemSetUp)
        #self.form.actionHardware_button_Discription.triggered.connect(self.change2ButtonDiscription)    
        #self.form.actionLED_State_Discription.triggered.connect(self.change2LEDDiscription)
        #self.form.actionVersion.triggered.connect(self.change2Version)    
       

    #Select "TS"(defalt) to change to TS config page   
    def changeToTS(self):
        para={'Mode':self.form.Mode.currentText()}
        filename='para.json'
        with open(filename,'w') as f:
            json.dump(para,f)
        TSConfig = controller.TSConfig_mainwindow.TSConfig_Controller() 
        TSConfig.run_TSConfig()
        
	#Change to sencond level page	
    def ChangeToSecond(self):
		#Change to TS config page
        def change_TS(self):
            
            TSConfig = controller.TSConfig_mainwindow.TSConfig_Controller() 
            TSConfig.run_TSConfig()
        #Change to FPA config page    
        def change_FPA(self):
            FPAConfig = controller.FPAConfig_mainwindow.fpacpntroller() 
            FPAConfig.run_fpa()
        # Read the current index of "Mode" combox
        if self.form.Mode.currentText()=="躯干摇晃角":
            self.form.YES.clicked.disconnect()
            self.form.YES.clicked.connect(change_TS)
            
        elif self.form.Mode.currentText()=="足偏角":
            self.form.YES.clicked.disconnect()
            self.form.YES.clicked.connect(change_FPA)
        para={'Mode':self.form.Mode.currentText()}
        filename='para.json'
        with open(filename,'w') as f:
            json.dump(para,f)

    def deleteData(self):

        selectRow_ID= list(reversed([QPersistentModelIndex(index) for index in self.form.tableView.selectionModel().selectedRows()]))
        Trialname=[]
        for ID in selectRow_ID:
            name1=self.model.data(self.model.index(ID.row(),0))
            Trialname.append(name1)
            self.model.removeRow(ID.row()) 
        print(Trialname)
        DeleteTrial=" ".join(str(i) for i in Trialname)
        #print(a)
        model.ssh_engine.DelDirectory(DeleteTrial)

    def refreshData(self):
        model.ssh_engine.exesensordirector()
        model.ssh_engine.RasToGui(model.ssh_engine.SAGE_HOME + 'src/modules/dpm/common/TrialInfo.json', model.ssh_engine.SAGE + 'model/')
        filename = model.ssh_engine.SAGE+'model/TrialInfo.json'
        with open(filename) as f_1:
            self.trial = json.load(f_1)  
        header = ['名称', '时间', '大小']  
        self.model = MyTableModel(self.trial, header)


        # Set data model to Qtableview
        self.form.tableView.setModel(self.model)

    '''def refreshSystemInfo(self, data):

        for i  in range(8):
            (getattr(self.form,'sensor{}id'.format(i+1)).setText(data["Sensor"][i]["ID"]))
            (getattr(self.form,'sensor{}Battery'.format(i+1)).setValue(int(data["Sensor"][i]["Battery"])))
            (getattr(self.form,'sensor{}connection'.format(i+1)).setText(data["Sensor"][i]["State"]))
            if data["Sensor"][i]["State"]=="unconnected":
                (getattr(self.form,'sensor{}connection'.format(i+1)).setStyleSheet("color:red"))
        for i in range(4):
            (getattr(self.form,'Feedback{}id'.format(i+1)).setText(data["Feedback"][i]["ID"]))
            (getattr(self.form,'Feedback{}Battery'.format(i+1)).setValue(int(data["Feedback"][i]["Battery"])))
            (getattr(self.form,'Feedback{}connection'.format(i+1)).setText(data["Feedback"][i]["State"]))
            if data["Feedback"][i]["State"]=="unconnected": 
                (getattr(self.form,'Feedback{}connection'.format(i+1)).setStyleSheet("color:red"))   
        self.form.Capacity.setText(data["PI"])
        self.form.HubBattery.setValue(int(data["Battery"]))
        self.form.Hubconnection.setText(data["State"])'''
        

    def change2Log(self):
        change2Log=controller.log_mainwindow.Log()
        change2Log.run_log()
      
    def selectPath(self):
        selectpath=controller.selectpath_mainwindow.selectpath()
        selectpath.run_selectpath()
    
    def change2FirmwareUpdate(self):
        class Form(QWidget):
            def __init__(self, parent=None):
                super(Form, self).__init__(parent)

            def load(self, url):
                import webbrowser
                webbrowser.open(url)
        screen = Form()
        url = "http://wearablesystems.wikidot.com/"
        screen.load(url)
    def change2SystemSetUp(self):
        class Form(QWidget):
            def __init__(self, parent=None):
                super(Form, self).__init__(parent)

            def load(self, url):
                import webbrowser
                webbrowser.open(url)
        screen = Form()
        url = "http://wearablesystems.wikidot.com/"
        screen.load(url)
        
        
    def change2ButtonDiscription(self):
        class Form(QWidget):
            def __init__(self, parent=None):
                super(Form, self).__init__(parent)

            def load(self, url):
                import webbrowser
                webbrowser.open(url)
        screen = Form()
        url = "http://wearablesystems.wikidot.com/"
        screen.load(url)
        
    def change2LEDDiscription(self):
        class Form(QWidget):
            def __init__(self, parent=None):
                super(Form, self).__init__(parent)

            def load(self, url):
                import webbrowser
                webbrowser.open(url)
        screen = Form()
        url = "http://wearablesystems.wikidot.com/"
        screen.load(url)
    def change2Version(self):
        class Form(QWidget):
            def __init__(self, parent=None):
                super(Form, self).__init__(parent)

            def load(self, url):
                import webbrowser
                webbrowser.open(url)
        screen = Form()
        url = "http://wearablesystems.wikidot.com/"
        screen.load(url)


    def starMenu(self, Index):
        self.columnIndex = Index

        self.menu  = QMenu(self)

        actionSortAscend  = QAction("ascend" , self)
        actionSortDescend = QAction("descend", self)
        actionSortAscend.triggered.connect(self.sortAscend)
        actionSortDescend.triggered.connect(self.sortDescend)
        self.menu.addAction(actionSortAscend)
        self.menu.addAction(actionSortDescend)

        self.menu.addSeparator()
        
        if self.columnIndex==0:
            actionfilterAll = QAction("all", self)
            actionFilterFPA = QAction("FPA", self)
            actionFilterTS  = QAction("TS" , self)
            actionfilterAll.triggered.connect(self.filterAll)
            actionFilterFPA.triggered.connect(self.filterFPA)
            actionFilterTS.triggered.connect(self.filterTS)
            self.menu.addAction(actionfilterAll)
            self.menu.addAction(actionFilterFPA)
            self.menu.addAction(actionFilterTS)            

        headerPos = self.form.tableView.mapToGlobal(self.horizontalHeader.pos())
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.columnIndex)

        self.menu.exec_(QPoint(posX, posY))

    def sortAscend(self):

        self.model.sort(self.columnIndex, Qt.AscendingOrder)

    def sortDescend(self):
        self.model.sort(self.columnIndex, Qt.DescendingOrder)

    def filterAll(self):
        self.model.filter("")

    def filterFPA(self):
        self.model.filter("FPA")

    def filterTS(self):
        self.model.filter("TS")
        
    def selectWarning(self):
        button=QMessageBox.information(self,"Waring","This operation will detele the selected data files on Raspberry, still want to continue?",
                                    QMessageBox.Yes|QMessageBox.No)
        if button==QMessageBox.Yes:
            selectRow_ID = list(reversed([QPersistentModelIndex(index) for index in self.form.tableView.selectionModel().selectedRows()]))
            Trialname = []
            for ID in selectRow_ID:
                name1=self.model.data(self.model.index(ID.row(),0))
                Trialname.append(name1)
                self.model.removeRow(ID.row()) 
            print(Trialname)
            DeleteTrial = " ".join(str(i) for i in Trialname)
            #print(a)
            model.ssh_engine.DelDirectory(DeleteTrial)
        else:
            return

class MyTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = []

        row_num = len(datain)
        for row in range(row_num):
            self.arraydata.append([datain[row]['name'],datain[row]['time'],datain[row]['size']])
        self.origindata = list(self.arraydata)
        #If trial is in the order of 'name' 'time' 'size'. The code will be simplified as below.
        #for row in range(row_num):
        #   self.arraydata.append(list(datain[row].values()))
        #    print(self.arraydata)
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return 3
 
    def data(self, index, role=Qt.DisplayRole): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return self.arraydata[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number or by given Regular Expression
        """
        self.layoutAboutToBeChanged.emit()
        #In the former way, Fangyuan pointed out that 'FPA2' was in front of 'FPA10'.
        #That is why I rewrite the sort function.
        if Ncol == 0:
            self.arraydata.sort(key = lambda x : tuple([re.split('(\d+)', x[0])[0], int(re.split('(\d+)', x[0])[1])]))
        else:
            self.arraydata.sort(key = operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.layoutChanged.emit()

    def filter(self, string):
        self.layoutAboutToBeChanged.emit()
        self.arraydata = list(filter(lambda x : string in x[0], self.origindata))
        self.layoutChanged.emit()
        
    def removeRow(self, index):
        self.layoutAboutToBeChanged.emit()
        self.origindata.remove(self.arraydata[index])
        del self.arraydata[index]
        self.layoutChanged.emit()

class RefreshThread(QThread):
    _signal = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super(RefreshThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            time.sleep(1)
            systeminfo = model.ssh_engine.SAGE+'model/SystemInfo.json'
            with open(systeminfo,'r') as f_2:
                data = json.load(f_2)
            self._signal.emit(data)




