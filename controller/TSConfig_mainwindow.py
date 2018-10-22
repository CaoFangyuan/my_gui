from PyQt5.Qt import *
from PyQt5.QtCore import *
import controller.forms.ts_config
import controller.Config_mainwindow
import model.ssh_engine
import os
import sys
import pexpect
import json



class TSConfig_Controller(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.form = controller.forms.ts_config.Ui_TS_Config()
        self.form.setupUi(self)
        #Incident of Clicking "config" button
        self.form.Configure.clicked.connect(self.writeAndSentTXT)
        #Incident of "Feedback_Direc" combox changes 
        self.form.Feedback_Direc.currentIndexChanged['QString'].connect(self.SetPara)
        #Incident of "PD_Control" checkbox changes
        self.form.PD_Control.setTristate(False)
        self.form.PD_Control.stateChanged.connect(self.PD_State)
        #Initial state for "PD_Control" checkbox
        if self.form.PD_Control.checkState()==0:

            self.form.D_Parameter.setVisible(False)	
            self.form.label.setVisible(False)
            self.form.label_2.setVisible(False)
         
        self.form.Left.setVisible(False)
        self.form.Right.setVisible(False)
        self.form.Front.setVisible(True)
        self.form.Back.setVisible(True)
        self.form.label_11.setVisible(False)
        self.form.label_12.setVisible(False)
        self.form.label_10.setVisible(True)
        self.form.label_13.setVisible(True)
        #Set double validator for lineedits
        #The boundary might not be appropriate

        regExp = QRegExp("^([0-9]|[1-8][0-9])(\.[0-9]+)?$")
        self.form.Left.setValidator(QRegExpValidator(regExp, self))
        self.form.Right.setValidator(QRegExpValidator(regExp, self))
        self.form.Front.setValidator(QRegExpValidator(regExp, self))
        self.form.Back.setValidator(QRegExpValidator(regExp, self))

        #Load previous setting
        self.settings = QSettings("Wearable", "Sage System")
        right = self.settings.value("right", self.form.Right.text())
        left  = self.settings.value("left" , self.form.Left.text())
        front = self.settings.value("front", self.form.Front.text())
        back  = self.settings.value("back" , self.form.Back.text())
        d_parameter    = self.settings.value("d_parameter"    , self.form.D_Parameter.text())
        pd_control     = self.settings.value("pd_control"     , self.form.PD_Control.isChecked(),type=bool)
        feedback_dirct = self.settings.value("feedback_dirct" , self.form.Feedback_Direc.currentIndex(),type=int)
        self.form.Right.setText(right)
        self.form.Left.setText(left)
        self.form.Front.setText(front)
        self.form.Back.setText(back)
        self.form.D_Parameter.setText(d_parameter)
        self.form.PD_Control.setCheckState(pd_control)
        self.form.Feedback_Direc.setCurrentIndex(feedback_dirct)

    # Show TS_Config page      
    def run_TSConfig(self):
        self.exec()
    
    def changeToSetUp(self):
        class Form(QWidget):
            def __init__(self, parent=None):
                super(Form, self).__init__(parent)

            def load(self, url):
                import webbrowser
                webbrowser.open(url)
        screen = Form()
        url = "http://wearablesystems.wikidot.com/"
        screen.load(url)
    
    def SetPara(self):
		
        if self.form.Feedback_Direc.currentText()=="前后":
            self.form.Left.setVisible(False)
            self.form.Right.setVisible(False)
            self.form.Front.setVisible(True)
            self.form.Back.setVisible(True)
            self.form.label_11.setVisible(False)
            self.form.label_12.setVisible(False)
            self.form.label_10.setVisible(True)
            self.form.label_13.setVisible(True)
           
        elif self.form.Feedback_Direc.currentText()=="左右":
            self.form.Left.setVisible(True)
            self.form.Right.setVisible(True)
            self.form.Front.setVisible(False)
            self.form.Back.setVisible(False)
            self.form.label_10.setVisible(False)
            self.form.label_13.setVisible(False)
            self.form.label_11.setVisible(True)
            self.form.label_12.setVisible(True)
        
        else:
            self.form.Front.setVisible(True)
            self.form.Back.setVisible(True)
            self.form.Left.setVisible(True)
            self.form.Right.setVisible(True)
            self.form.label_10.setVisible(True)
            self.form.label_13.setVisible(True)
            self.form.label_11.setVisible(True)
            self.form.label_12.setVisible(True)
            
    #Check state of "PD_Control" checkbox       
    def PD_State(self):
        
        if self.form.PD_Control.isChecked():
            self.form.PD_Control.setTristate(False)
            self.form.D_Parameter.setVisible(True)
            self.form.label.setVisible(True)
            self.form.label_2.setVisible(True)
            #print(self.form.PD_Control.checkState())
        else:
            self.form.D_Parameter.setVisible(False)
            self.form.label.setVisible(False)
            self.form.label_2.setVisible(False)	
            #print(self.form.PD_Control.checkState())
        
    #o write configure parameter to .py file and send to Raspberry Pi, execute program on Raspberry pi     
    def writeAndSentTXT(self):
		#write to json file
        filename='para.py'
        if self.form.Feedback_Direc.currentText()=="Anterior-Posterior (A/P)":
            with open(filename,'a') as f:
                f.write('Feedback_direc=0\n')
                f.write('Front='+self.form.Front.text()+'\n')   
                f.write('Back='+self.form.Back.text()+'\n')   
           
        elif self.form.Feedback_Direc.currentText()=="Medial-Lateral (M/L)":
            with open(filename,'a') as f:
                f.write('Feedback_direc=1\n')
                f.write('Left='+self.form.Left.text()+'\n')   
                f.write('Right='+self.form.Right.text()+'\n') 
        else:
            with open(filename,'a') as f:
                f.write('Feedback_direc=2\n')
                f.write('Front='+self.form.Front.text()+'\n')   
                f.write('Back='+self.form.Back.text()+'\n')
                f.write('Left='+self.form.Left.text()+'\n')   
                f.write('Right='+self.form.Right.text()+'\n')
        if self.form.PD_Control.isChecked():
            para={'PD':self.form.D_Parameter.text()}
            with open(filename,'a') as f:
                f.write('pd='+self.form.D_Parameter.text()+'\n')   
           
        else:
            with open(filename,'a') as f:
                f.write('pd=0\n')
        
        # Save current setting
        self.settings.setValue("right", self.form.Right.text())
        self.settings.setValue("left", self.form.Left.text())
        self.settings.setValue("front", self.form.Front.text())
        self.settings.setValue("back", self.form.Back.text())
        self.settings.setValue("d_parameter", self.form.D_Parameter.text())
        self.settings.setValue("pd_control", self.form.PD_Control.isChecked())
        self.settings.setValue("feedback_dirct",self.form.Feedback_Direc.currentIndex())
        # send config file to raspberry pi
        model.ssh_engine.GuiToRas("./para.py",model.ssh_engine.SAGE_HOME+'common/')
        Config_success=controller.Config_mainwindow.config_success() 
        Config_success.run_config()
        
		
		



     
    
 
