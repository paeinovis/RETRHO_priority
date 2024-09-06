from lib import *
import prioritylib.initwin as initwin

Simbad.add_votable_fields("U", "V", "B")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        initwin.init_window(self)
     
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()






# Authors: Pae Swanson, Triana Almeyda, Cassidy Camera, Hannah Luft

# References used (mostly for pyqt tbh):
# https://www.pythonguis.com/docs/qcombobox/
# https://www.geeksforgeeks.org/pyqt5-setting-current-text-in-combobox/
# https://www.geeksforgeeks.org/pyqt5-how-to-add-action-to-a-button/
# https://www.pythonguis.com/docs/qpushbutton/
# https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html
# https://www.geeksforgeeks.org/how-to-embed-matplotlib-graph-in-pyqt5/
# https://docs.astropy.org/en/stable/visualization/wcsaxes/
# https://stackoverflow.com/questions/72568050/plotting-a-chart-inside-a-pyqt-gui
# https://pythonspot.com/pyqt5-tabs/
# https://pythonspot.com/pyqt5-file-dialog/

