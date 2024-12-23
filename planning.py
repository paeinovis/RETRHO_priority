from lib import *
import prioritylib.initwin as initwin

app = QApplication(sys.argv)

try:
    Simbad.add_votable_fields("U", "V", "B")
except (DALAccessError, DALServiceError, DALFormatError):
    popup = initwin.PopupWindow()
    initwin.DAL_error(popup)
    popup.show()
    app.exec_()
except (E10):
    popup = initwin.PopupWindow()
    initwin.pyvo_error(popup)
    popup.show()
    app.exec_()


w = initwin.MainWindow()
w.show()
app.exec_()


# Authors: Pae Swanson
# Contributors: Meir Schochet, Cassidy Camera, Hannah Luft