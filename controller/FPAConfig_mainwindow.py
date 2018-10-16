from PyQt5.Qt import *
import controller.forms.fpa
import model.ssh_engine
import os
import sys
import pexpect

class fpacpntroller(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.form = controller.forms.fpa.Ui_FPA()
        self.form.setupUi(self)
        
    # Show select path dialog      
    def run_fpa(self):
        self.exec()
