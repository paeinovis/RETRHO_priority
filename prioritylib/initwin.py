from lib import *
import prioritylib.plots as plots
import prioritylib.helpers as helpers
import prioritylib.printers as printers
import prioritylib.setters as setters
from prioritylib.global_ import *
import prioritylib.sorters as sorters

# Creates main window with all tabs
class MainWindow(QMainWindow):
    # Init main window
    def __init__(self):
        super().__init__()
        init_window(self)
        self.setWindowIcon(QIcon('retrhogo.png'))
    
    # Init secondary window(s) FIXME: presently not used - if this stays this way, delete
    def new_window(self):
        if self.w is None:
            self.w = PopupWindow()
        self.w.show()

# Creates secondary window(s) w/ label FIXME: presently not used - if this stays this way, delete
class PopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowIcon(QIcon('retrhogo.png'))

# class for scrollable label        (from Geeks for Geeks)
class ScrollLabel(QScrollArea):
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        layout = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
 
    def setText(self, text):
        self.label.setText(text)


# First init of main window - only called once
def init_window(self):
    self.setWindowTitle("Planning")

    # Define tabs
    self.tabs = QTabWidget()
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.tab3 = QWidget()
    self.tabs.addTab(self.tab1, "Stars from name")
    self.tabs.addTab(self.tab2, "Objects from file")
    self.tabs.addTab(self.tab3, "Custom values")

    # Overall window stuff
    container = QWidget()
    self.setCentralWidget(container)
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.tabs)
    container.setLayout(self.layout)
    self.w = None
    self.sheet = None

    width = 450
    height = 950
    self.resize(width, height)

    self.fov = 15*u.arcmin
    self.time_var = Time.now() 
    self.use_curr_time = True

    # Init
    init_tab_one(self)
    init_tab_two(self)
    init_tab_three(self)

    info = "Program time:\n\nName:\nIdentifier:\nUp now:\n\nCoordinates RA:\nCoordinates DEC:\nMagnitude V:\n\nRises:\nSets:\n\n\nMaximum altitude:\nMinimum altitude:\n\nAltitude:\nAzimuth:\n"
    self.tab1.label_info.setText(info)   

def init_tab_one(self):
    # Tab 1 objects:

    # Init tab 1 values:
    self.tab1.coords = SkyCoord("00:00:00.00 00:00:00.00", unit=(u.hour, u.deg), frame='icrs')
    self.tab1.current_target = FixedTarget(self.tab1.coords, name="Default Coordinates Plot")
    self.tab1.current_target_name = "Default"

    self.tab1.only_show_up = False

    # List of possible alignment stars - can be changed if desired. 
    # Currently organized by brightest mag V to dimmest
    temp_target_names = ['Arcturus', 'Vega', 'Capella', 'Procyon', 'Altair', 
                         'Aldebaran', 'Antares', 'Spica', 'Fomalhaut', 'Deneb', 
                         'Regulus', 'Dubhe', 'Mirfak', 'Polaris', 'Schedar',
                         'Kappa Oph', '* b03 Cyg', '* g Her', '* 49 Cas']

    self.tab1.target_names = []
    self.tab1.up_target_names = [] 
    self.tab1.targets = []
    self.tab1.mags = []

    # Widgets
    self.tab1.targets_dropdown = QComboBox()
    self.tab1.targets_dropdown.addItems(self.tab1.target_names)
    self.tab1.targets_dropdown.setEditable(True)
    self.tab1.targets_dropdown.setInsertPolicy(QComboBox.InsertAtTop)

    self.tab1.sort_dropdown = QComboBox()
    self.tab1.sort_dropdown.addItems(SORT_NAMES_1)

    self.tab1.label_info = QLabel()
    self.tab1.label_info.setGeometry(200, 200, 200, 30)
    self.tab1.label_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    self.tab1.targets_dropdown_button = QPushButton("Go")
    self.tab1.targets_dropdown_button.clicked.connect(lambda: printers.get_info_of_obj(self, self.tab1))

    self.tab1.sort_dropdown_button = QPushButton("Sort")
    self.tab1.sort_dropdown_button.clicked.connect(lambda: sorters.sort_targets_tab1(self))

    self.tab1.plot_button = QPushButton("Plot")
    self.tab1.plot_button.clicked.connect(lambda: plots.plot(self, self.tab1))

    self.tab1.update_button = QPushButton("Update Targets Up Status")
    self.tab1.update_button.clicked.connect(lambda: helpers.determine_up(self.tab1.targets, self.tab1.target_names, self, self.tab1))

    self.tab1.show_up_button = QPushButton("Only Show Up Targets")
    self.tab1.show_up_button.clicked.connect(lambda: helpers.change_only_show_up(self, self.tab1))

    self.tab1.plot_airmass_button = QPushButton("Plot airmass")
    self.tab1.plot_airmass_button.clicked.connect(lambda: plots.airmass_plot(self, self.tab1))

    # Entire tab layout
    self.tab1.layout = QVBoxLayout()
    self.tab1.layout.addWidget(self.tab1.targets_dropdown)
    self.tab1.layout.addWidget(self.tab1.targets_dropdown_button)
    self.tab1.layout.addWidget(self.tab1.sort_dropdown)
    self.tab1.layout.addWidget(self.tab1.sort_dropdown_button)
    self.tab1.layout.addWidget(self.tab1.label_info)
    self.tab1.layout.addWidget(self.tab1.plot_button)
    self.tab1.layout.addWidget(self.tab1.plot_airmass_button)
    self.tab1.layout.addWidget(self.tab1.update_button)
    self.tab1.layout.addWidget(self.tab1.show_up_button)
    self.tab1.setLayout(self.tab1.layout)

    init_tab1_target_names(self, temp_target_names)

def init_tab_two(self):
    # Tab 2 objects: 

    # Init tab 2 values:
    self.tab2.coords = SkyCoord("00:00:00.00 00:00:00.00", unit=(u.hour, u.deg), frame='icrs')
    self.tab2.current_target = FixedTarget(self.tab2.coords, name="Default Coordinates Plot")
    self.tab2.current_target_name = "Default"
    self.tab2.result_table = None   
    self.tab2.sheet_index = 1
    self.tab2.sheet_index_end = 1

    self.tab2.only_show_up = False

    self.tab2.target_names = [] 
    self.tab2.up_target_names = [] 
    self.tab2.targets = []
    self.tab2.targets_dropdown = QComboBox()
    self.tab2.targets_dropdown.addItems(self.tab2.target_names)

    # Widgets
    self.tab2.label_info = ScrollLabel(self)
    self.tab2.label_info.setGeometry(200, 200, 200, 30)
    self.tab2.label_info.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    self.tab2.targets_dropdown_button = QPushButton("Go")
    self.tab2.targets_dropdown_button.clicked.connect(lambda: printers.get_info_of_obj(self, self.tab2))

    self.tab2.csv_info_button = QPushButton("Display Submitted Target Info")
    self.tab2.csv_info_button.clicked.connect(lambda: printers.print_csv_target(self))

    self.tab2.sort_dropdown = QComboBox()
    self.tab2.sort_dropdown.addItems(SORT_NAMES_2)

    self.tab2.sort_dropdown_button = QPushButton("Sort")
    self.tab2.sort_dropdown_button.clicked.connect(lambda: sorters.sort_targets_tab2(self))

    self.tab2.plot_button = QPushButton("Plot")
    self.tab2.plot_button.clicked.connect(lambda: plots.plot_coords(self, self.tab2))

    self.tab2.plot_airmass_button = QPushButton("Plot airmass")
    self.tab2.plot_airmass_button.clicked.connect(lambda: plots.airmass_plot(self, self.tab2))

    self.tab2.update_button = QPushButton("Update Targets Up Status")
    self.tab2.update_button.clicked.connect(lambda: helpers.determine_up(self.tab2.targets, self.tab2.target_names, self, self.tab2))

    self.tab2.show_up_button = QPushButton("Only Show Up Targets Toggle")
    self.tab2.show_up_button.clicked.connect(lambda: helpers.change_only_show_up(self, self.tab2))

    self.tab2.file_upload_button = QPushButton("Upload TargetMasterSheet.csv file")
    self.tab2.file_upload_button.clicked.connect(lambda: open_file_dialog(self))

    # Entire tab layout
    self.tab2.layout = QVBoxLayout()
    self.tab2.layout.addWidget(self.tab2.file_upload_button)
    self.tab2.layout.addWidget(self.tab2.targets_dropdown)
    self.tab2.layout.addWidget(self.tab2.targets_dropdown_button)
    self.tab2.layout.addWidget(self.tab2.csv_info_button)
    self.tab2.layout.addWidget(self.tab2.sort_dropdown)
    self.tab2.layout.addWidget(self.tab2.sort_dropdown_button)
    self.tab2.layout.addWidget(self.tab2.label_info)
    self.tab2.layout.addWidget(self.tab2.plot_button)
    self.tab2.layout.addWidget(self.tab2.plot_airmass_button)
    self.tab2.layout.addWidget(self.tab2.update_button)
    self.tab2.layout.addWidget(self.tab2.show_up_button)

    self.tab2.setLayout(self.tab2.layout)

def init_tab_three(self):
    # Tab 3 objects:

    # Init tab 3 values:
    self.tab3.ra = "00:00:00.00"
    self.tab3.dec = "00:00:00.00"
    temp_coords = self.tab3.ra + " " + self.tab3.dec
    self.tab3.coords = SkyCoord(temp_coords, unit=(u.hour, u.deg), frame='icrs')
    self.tab3.current_target = FixedTarget(self.tab3.coords, name="Default Coordinates Plot")
    self.tab3.current_target_name = "Fixed Coordinates"

    # Widgets
    self.tab3.fov_input = QLineEdit()
    self.tab3.fov_input_button = QPushButton("Change FOV in arcminutes")

    self.tab3.label_info = QLabel()
    self.tab3.label_info.setGeometry(200, 200, 200, 30)
    self.tab3.label_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    self.tab3.fov_input_button.clicked.connect(lambda: setters.change_fov(self))

    self.tab3.ra_input = QLineEdit()
    self.tab3.ra_input_button = QPushButton("Change Right Ascension")
    self.tab3.ra_input_button.clicked.connect(lambda: setters.change_ra(self))

    self.tab3.dec_input = QLineEdit()
    self.tab3.dec_input_button = QPushButton("Change Declination")
    self.tab3.dec_input_button.clicked.connect(lambda: setters.change_dec(self))

    self.tab3.time_input = QLineEdit()
    self.tab3.time_input_button = QPushButton("Change time (YYYY-MM-DD HH:MM:SS)")
    self.tab3.time_input_button.clicked.connect(lambda: setters.change_time(self))

    self.tab3.now_button = QPushButton("Use current time")
    self.tab3.now_button.clicked.connect(lambda: setters.use_now_time(self))

    self.tab3.plot_button = QPushButton("Plot")
    self.tab3.plot_button.clicked.connect(lambda: plots.plot_coords(self, self.tab3))

    self.tab3.plot_airmass_button = QPushButton("Plot airmass")
    self.tab3.plot_airmass_button.clicked.connect(lambda: plots.airmass_plot(self, self.tab3))

    self.tab3.get_info_button = QPushButton("Print info")
    self.tab3.get_info_button.clicked.connect(lambda: printers.tab3_print(self, self.tab3))

    # Entire tab layout
    self.tab3.layout = QVBoxLayout()
    self.tab3.layout.addWidget(self.tab3.fov_input)
    self.tab3.layout.addWidget(self.tab3.fov_input_button)
    self.tab3.layout.addWidget(self.tab3.ra_input)
    self.tab3.layout.addWidget(self.tab3.ra_input_button)
    self.tab3.layout.addWidget(self.tab3.dec_input)
    self.tab3.layout.addWidget(self.tab3.dec_input_button)
    self.tab3.layout.addWidget(self.tab3.time_input)
    self.tab3.layout.addWidget(self.tab3.time_input_button)
    self.tab3.layout.addWidget(self.tab3.now_button)
    self.tab3.layout.addWidget(self.tab3.plot_button)
    self.tab3.layout.addWidget(self.tab3.plot_airmass_button)
    self.tab3.layout.addWidget(self.tab3.get_info_button)
    self.tab3.layout.addWidget(self.tab3.label_info)

    self.tab3.setLayout(self.tab3.layout)


# Open csv file 
def open_file_dialog(self):                       # Function from https://pythonspot.com/pyqt5-file-dialog/
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(self,"Choose target list file", "","CSV Files (*.csv)", options=options)
    if file_name:
        try: 
            self.sheet = pandas.read_csv(file_name)
            self.sheet = self.sheet.iloc[1:]                                               # Gets rid of format instructional row
            self.sheet = self.sheet[self.sheet[RA].str.contains("nan") == False]           # Gets rid of blank rows
            self.tab2.targets[:] = []
            self.tab2.target_names[:] = []
            msg = "Successfully parsed file."
        except (KeyError):
            msg = "Error parsing file. Please check template of submitted sheet."
            setters.set_default(self, self.tab2, msg)
            return
        self.tab2.sheet_index = 1
        self.tab2.sheet_index_end = len(self.sheet) + 1
        init_tab2_target_names(self)
    else:
        self.sheet = None
        setters.set_default(self, self.tab2, "Error parsing file.")


# (Re)init tab1 values
def init_tab1_target_names(self, temp_target_names):
    del self.tab1.target_names, self.tab1.up_target_names, self.tab1.targets, self.tab1.mags
    self.tab1.target_names = []
    self.tab1.up_target_names = [] 
    self.tab1.targets = []
    self.tab1.mags = []

    now = Time.now()
    for star in temp_target_names:
        try:
            star = helpers.clip_name(star)
            curr_target = FixedTarget(coordinates.SkyCoord.from_name(star), name=star)
            self.tab1.targets.append(curr_target)
            self.tab1.mags.append(Simbad.query_object(star)[["V"][0]])
        except(NameResolveError):
            continue
        try:
            if RHO.target_is_up(now, curr_target):
                self.tab1.target_names.append(star + " (Up)")       # So user can see if a given object is in the sky
                self.tab1.up_target_names.append(star)
            else:
                self.tab1.target_names.append(star)
        except (exceptions.LargeQueryWarning, ReadTimeout, TimeoutError, IERSWarning):
            setters.set_default(self, self.tab1, "Download timed out, please try again.")
            return

    self.tab1.current_target_name = self.tab1.target_names[0]
    self.tab1.current_target = self.tab1.targets[0]
    self.tab1.coords = self.tab1.current_target.coord
    helpers.determine_up(self.tab1.targets, self.tab1.target_names, self, self.tab1)


# (Re)init tab2 values
def init_tab2_target_names(self):
    if self.tab2.target_names:
        self.tab2.target_names[:] = [] 
        self.tab2.up_target_names[:] = [] 
        self.tab2.targets[:] = []

    # Declare var as default to Now
    time_var_to_jd = Time.now()
    
    # If not using current time, however, use set date time
    if not self.use_curr_time:
        time_var_to_jd = self.time_var

    # Convert either now time or set time to jd for comparison purposes
    time_var_to_jd = time_var_to_jd.to_value('jd', 'float')

    for i in range(self.tab2.sheet_index, self.tab2.sheet_index_end):
        try: 
            name = self.sheet.at[i, NAME]
            # Get obs window and determine if applicable to set time 
            obs_win_open = self.sheet.at[i, OBS_WIN_OPEN]
            obs_win_open = Time(helpers.convert_date(obs_win_open))
            obs_win_open_sec = obs_win_open.to_value('cxcsec', 'float')

            obs_win_close = self.sheet.at[i, OBS_WIN_CLOSE]
            obs_win_close = Time(helpers.convert_date(obs_win_close))
            obs_win_close_sec = obs_win_close.to_value('cxcsec' ,'float') + 43200

            # Compare window to see if obs window currently open
            if obs_win_open_sec < time_var_to_jd and obs_win_close_sec < time_var_to_jd:
                continue

            curr_target = FixedTarget(coordinates.SkyCoord.from_name(name), name=name)
            self.tab2.targets.append(curr_target)

            priority = " (" + str(self.sheet.at[i, PRIORITY]) + ")"
            name += priority
            self.tab2.target_names.append(name)
            msg = "Successfully parsed file."
        except (KeyError, ValueError, TypeError):
            msg = "Error parsing file. Please check template of submitted sheet."
            setters.set_default(self, self.tab2, msg)
            return False
        except (NameResolveError, NoResultsWarning):
            priority = " (" + str(self.sheet.at[i, PRIORITY]) + ")"
            name += priority
            self.tab2.target_names.append(name)
            name = self.sheet[NAME][i]
            curr_coords = self.sheet[RA][i] + " " + self.sheet.at[i, DEC]
            curr_coords = SkyCoord(curr_coords, unit=(u.hour, u.deg), frame='icrs')
            curr_target = FixedTarget(curr_coords, name=name)
            self.tab2.targets.append(curr_target)
    if helpers.determine_up(self.tab2.targets, self.tab2.target_names, self, self.tab2):
        self.tab2.label_info.setText(msg)
        self.tab2.targets_dropdown.clear()
        self.tab2.targets_dropdown.addItems(self.tab2.target_names)
        self.tab2.current_target_name = self.tab2.target_names[0]
        self.tab2.current_target = self.tab2.targets[0]
        self.tab2.coords = self.tab2.current_target.coord
        return True
    msg = "Error parsing file. Please check template of submitted sheet."
    setters.set_default(self, self.tab2, msg)