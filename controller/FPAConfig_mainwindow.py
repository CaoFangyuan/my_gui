from PyQt5.Qt import *
import controller.forms.fpa
import controller.Config_mainwindow
import model.ssh_engine
import os
import sys
import pexpect
import json

class fpacpntroller(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.form = controller.forms.fpa.Ui_FPA()
        self.form.setupUi(self)
        #Incident of Clicking "config" button
        self.form.Configure.clicked.connect(self.writeAndSentTXT)
           
        self.settings = QSettings("Wearable", "Sage System")
        right = self.settings.value("right", self.form.Right.text())
        left  = self.settings.value("left" , self.form.Left.text())
        feedback_dirct = self.settings.value("feedback_dirct" , self.form.Feedback_Direc.currentIndex(),type=int)
        self.form.Right.setText(right)
        self.form.Left.setText(left)
        self.form.Feedback_Direc.setCurrentIndex(feedback_dirct)
        
    # Show select path dialog      
    def run_fpa(self):
        self.exec()
     

    #o write configure parameter to .py file and send to Raspberry Pi, execute program on Raspberry pi     
    def writeAndSentTXT(self):
		#write to json file
        filename='para.py'
        if self.form.Feedback_Direc.currentText()=="左脚":
            
            with open(filename,'w') as f:
                f.write('Feedback_direc=0\n')
                f.write('Left='+self.form.Left.text()+'\n')   
                f.write('Right='+self.form.Right.text()+'\n')
        elif self.form.Feedback_Direc.currentText()=="右脚":
            
            with open(filename,'w') as f:
                f.write('Feedback_direc=1\n')
                f.write('Left='+self.form.Left.text()+'\n')   
                f.write('Right='+self.form.Right.text()+'\n')
        
        # Save current setting
        self.settings.setValue("right", self.form.Right.text())
        self.settings.setValue("left", self.form.Left.text())
        self.settings.setValue("feedback_dirct",self.form.Feedback_Direc.currentIndex())
        # send config file to raspberry pi
        model.ssh_engine.GuiToRas("./para.py",model.ssh_engine.SAGE_HOME+'common/')
        Config_success=controller.Config_mainwindow.config_success() 
        Config_success.run_config()
