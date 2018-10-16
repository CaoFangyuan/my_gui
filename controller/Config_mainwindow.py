from PyQt5.Qt import *
import controller.forms.config
import model.ssh_engine
import os
import sys
import pexpect



class config_success(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.form = controller.forms.config.Ui_config()
        self.form.setupUi(self)
   
   
    # Show select path dialog      
    def run_config(self):
        self.exec()
    

    
        
