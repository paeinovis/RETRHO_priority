from lib import *
from prioritylib import *

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

    width = 450
    height = 500
    self.setMinimumSize(width, height) 

    # Init
    init_tab_one(self)
    init_tab_two(self)
    init_tab_three(self)
    self.fov = 15*u.arcmin
    self.time_var = Time.now() 
    self.use_curr_time = True

    info = "Name:\nIdentifier:\nUp now:\n\nCoordinates:\nMagnitude V:\n\nRises:\nSets:\n\nAltitude:\nAzimuth:"
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
    temp_target_names = ['Antares', 'Arcturus', 'Vega', 'Capella', 'Procyon',
                        'Altair', 'Aldebaran', 'Spica', 'Fomalhaut', 'Deneb', 
                        'Regulus', 'Dubhe', 'Mirfak', 'Polaris', 'Schedar',
                        'Kappa Oph', '* b03 Cyg' '* g Her', '* 49 Cas']
    self.tab1.target_names = []
    self.tab1.up_target_names = [] 
    self.tab1.targets = []

    now = Time.now()
    for star in temp_target_names:
        try:
            curr_target = FixedTarget(coordinates.SkyCoord.from_name(star), name=star)
            self.tab1.targets.append(curr_target)
        except(NameResolveError):
            continue
        if RHO.target_is_up(now, curr_target):
            self.tab1.target_names.append(star + " (Up)")       # So user can see if a given object is in the sky
            self.tab1.up_target_names.append(star)
        else:
            self.tab1.target_names.append(star)


    # Widgets
    self.tab1.targets_dropdown = QComboBox()
    self.tab1.targets_dropdown.addItems(self.tab1.target_names)
    self.tab1.targets_dropdown.setEditable(True)
    self.tab1.targets_dropdown.setInsertPolicy(QComboBox.InsertAtTop)

    self.tab1.label_info = QLabel()
    self.tab1.label_info.setGeometry(200, 200, 200, 30)

    self.tab1.targets_dropdown_button = QPushButton("Go")
    self.tab1.targets_dropdown_button.clicked.connect(lambda: printers.get_info_of_obj(self, self.tab1))

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
    self.tab1.layout.addWidget(self.tab1.label_info)
    self.tab1.layout.addWidget(self.tab1.plot_button)
    self.tab1.layout.addWidget(self.tab1.plot_airmass_button)
    self.tab1.layout.addWidget(self.tab1.update_button)
    self.tab1.layout.addWidget(self.tab1.show_up_button)
    self.tab1.setLayout(self.tab1.layout)

def init_tab_two(self):
    # Tab 2 objects: 

    # Init tab 2 values:
    self.tab2.coords = SkyCoord("00:00:00.00 00:00:00.00", unit=(u.hour, u.deg), frame='icrs')
    self.tab2.current_target = FixedTarget(self.tab2.coords, name="Default Coordinates Plot")
    self.tab2.current_target_name = "Default"
    self.tab2.result_table = None   

    self.tab2.only_show_up = False

    self.tab2.target_names = [] 
    self.tab2.up_target_names = [] 
    self.tab2.targets = []
    self.tab2.targets_dropdown = QComboBox()
    self.tab2.targets_dropdown.addItems(self.tab2.target_names)

    # Widgets
    self.tab2.label_info = QLabel()
    self.tab2.label_info.setGeometry(200, 200, 200, 30)

    self.tab2.targets_dropdown_button = QPushButton("Go")
    self.tab2.targets_dropdown_button.clicked.connect(lambda: printers.get_info_of_obj(self, self.tab2))

    self.tab2.csv_info_button = QPushButton("Print Submitted Target Info")
    self.tab2.csv_info_button.clicked.connect(lambda: printers.print_csv_target(self))

    self.tab2.plot_button = QPushButton("Plot")
    self.tab2.plot_button.clicked.connect(lambda: plots.plot_coords(self, self.tab2))

    self.tab2.plot_airmass_button = QPushButton("Plot airmass")
    self.tab2.plot_airmass_button.clicked.connect(lambda: plots.airmass_plot(self, self.tab2))

    self.tab2.update_button = QPushButton("Update Targets Up Status")
    self.tab2.update_button.clicked.connect(lambda: helpers.determine_up(self.tab2.targets, self.tab2.target_names, self, self.tab2))

    self.tab2.show_up_button = QPushButton("Only Show Up Targets Toggle")
    self.tab2.show_up_button.clicked.connect(lambda: helpers.change_only_show_up(self, self.tab2))

    self.tab2.file_upload_button = QPushButton("Upload file")
    self.tab2.file_upload_button.clicked.connect(lambda: open_file_dialog(self))

    # Entire tab layout
    self.tab2.layout = QVBoxLayout()
    self.tab2.layout.addWidget(self.tab2.file_upload_button)
    self.tab2.layout.addWidget(self.tab2.targets_dropdown)
    self.tab2.layout.addWidget(self.tab2.targets_dropdown_button)
    self.tab2.layout.addWidget(self.tab2.csv_info_button)
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
    self.tab3.layout.addWidget(self.tab3.label_info)

    self.tab3.setLayout(self.tab3.layout)

# Open csv file 
def open_file_dialog(self):                       # Function from https://pythonspot.com/pyqt5-file-dialog/
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(self,"Choose target list file", "","CSV Files (*.csv)", options=options)
    if file_name:
        self.sheet = pandas.read_csv(file_name)
        self.sheet = self.sheet[self.sheet[RA].str.contains("nan") == False]           # Gets rid of blank rows
        self.tab2.targets = []
        self.tab2.target_names = []
        msg = "Successfully parsed file."
        for i in range(2, len(self.sheet)):
            try: 
                name = self.sheet[NAME][i]
                curr_target = FixedTarget(coordinates.SkyCoord.from_name(name), name=name)
                self.tab2.targets.append(curr_target)
                self.tab2.target_names.append(name)
            except (NoResultsWarning, ValueError, TypeError):
                msg = "Error parsing file. Please check template of submitted sheet."
            except (NameResolveError):
                name = self.sheet[NAME][i] 
                curr_coords = self.sheet[RA][i] + " " + self.sheet[DEC][i]
                curr_coords = SkyCoord(curr_coords, unit=(u.hour, u.deg), frame='icrs')
                curr_target = FixedTarget(curr_coords, name=name)
                self.tab2.targets.append(curr_target)
                self.tab2.target_names.append(name)
        helpers.determine_up(self.tab2.targets, self.tab2.target_names, self, self.tab2)
        self.tab2.label_info.setText(msg)
        self.tab2.targets_dropdown.clear()       
        self.tab2.targets_dropdown.addItems(self.tab2.target_names)
    else:
        self.sheet = None
        setters.set_default(self, self.tab2, "Error parsing file.")

