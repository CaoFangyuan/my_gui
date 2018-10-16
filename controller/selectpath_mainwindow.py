from PyQt5.Qt import *
import controller.forms.dialog
import model.ssh_engine
import os
import sys
import pexpect



class selectpath(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.form = controller.forms.dialog.Ui_selectpath()
        self.form.setupUi(self)
        self.form.change.clicked.connect(self.changePath)
        self.form.select.clicked.connect(self.accept)
        self.form.cancel.clicked.connect(self.reject)
        # Save previous selected path
        self.settings = QSettings("Wearable", "Sage System")
        selected_path = self.settings.value("selected_path", self.form.path.text())
        self.path = selected_path
        self.form.path.setText(selected_path)
   
    # Show select path dialog      
    def run_selectpath(self):
        self.exec()
    
    def changePath(self):
        open = QFileDialog()
        self.path = open.getExistingDirectory()  
        self.form.path.setText(self.path)
        self.settings.setValue("selected_path", self.path)

    #def readPath(self):
       #print(self.form.path.text())
    
        
		
		



     
    
 
