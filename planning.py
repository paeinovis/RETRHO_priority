from lib import *
import prioritylib.initwin as initwin

Simbad.add_votable_fields("U", "V", "B")

app = QApplication(sys.argv)
w = initwin.MainWindow()
w.show()
app.exec_()





# Authors: Pae Swanson, Triana Almeyda, Cassidy Camera, Hannah Luft