
import sys
from PyQt5.Qt import *
import controller.forms

class SageControllerApp(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self._argv = argv
# Show the first level page
def run():
    app = SageControllerApp(sys.argv)
    QCoreApplication.setApplicationName("Sage")
    import controller.welcome_dialog
    wc = controller.welcome_dialog.SageWelcome(app, sys.argv)
    wc.show()
    sys.exit(app.exec_())
  

