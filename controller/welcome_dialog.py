from PyQt5.Qt import *
from PyQt5 import QtCore
import controller.forms.welcome
import model.ssh_engine
import os
import sys
import pexpect

class LoginThread(QThread):
    _signalMsg = pyqtSignal(str)
    _signalAccept = pyqtSignal() 

    def __init__(self, parent=None):
        super(LoginThread, self).__init__()
 
    def __del__(self):
        self.wait()
 
    def run(self):
        self._signalMsg.emit("Initiating connection...")        
        for ssh in model.ssh_engine.create_ssh():
            if ssh == None:
                self._signalMsg.emit("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#cc0000;\">Connection error!</span></p></body></html>")
                self._signalMsg.emit("Please check if SAGE device is connected to your computer.\nWhen plugged in, it will start connection automatically.")
                connectflag = True
                while connectflag:
                    for ssh in model.ssh_engine.create_ssh():
                        if ssh != None:
                            connectflag = False
                self._signalMsg.emit("SAGE device detected...")
                self._signalMsg.emit("Connected!")
                self._signalAccept.emit()
            else:
                self._signalMsg.emit("Connected!")
                self._signalAccept.emit()


class SageWelcome(QDialog):
    def __init__(self, app, args):
        QDialog.__init__(self)
        self.form = controller.forms.welcome.Ui_Welcome()
        self.form.setupUi(self)

        self.app = app
        self.args = args

        self.form.Cancel.clicked.connect(app.quit)
        self.form.LogBrowser.setText("")

        self.startLogin()

    def startLogin(self):
        self.thread = LoginThread()
        self.thread._signalMsg.connect(self.form.LogBrowser.append)
        self.thread._signalAccept.connect(self.accept)
        self.thread.start()

    def accept(self):
        self.close()
        import controller.SageMain_mainwindow
        self.mw = controller.SageMain_mainwindow.SageMainController(self.app, self.args)
        self.mw.show()
		
