from lib import *
from prioritylib.global_ import *
import prioritylib.initwin as initwin
import prioritylib.printers as printers
import prioritylib.helpers as helpers

# Change FOV to user input
def change_fov(self):
    update = "FOV could NOT be updated.\nEnsure that the value entered is a positive floating point number." + "\n\nCurrent information" + printers.get_tab_three_info(self)
    try:
        new_fov = float(self.tab3.fov_input.text())
        if (new_fov > 0):
            self.fov = new_fov * u.arcmin
            update = "Successfully updated FOV to " + str(self.fov) + "." + "\n\nCurrent information" + printers.get_tab_three_info(self)
    except (ValueError, TypeError):
        pass
    self.tab3.label_info.setText(update)

# Change RA to user input
def change_ra(self):
    update = "RA could NOT be updated.\nEnsure that the value entered matches a valid format (e.g., HH:MM:SS)." + "\n\nCurrent information" + printers.get_tab_three_info(self)
    try:
        new_ra = self.tab3.ra_input.text()
        coord_str_1 = str(new_ra) 
        coord_str_2 = str(self.tab3.dec)
        new_coords = SkyCoord(coord_str_1, coord_str_2, unit=(u.hour, u.deg), frame='icrs')
        self.tab3.coords = new_coords
        self.tab3.ra = new_ra
        self.tab3.current_target = FixedTarget(self.tab3.coords, name="Custom Coordinates Plot")
        update = "Updated RA to " + str(self.tab3.ra) + ".\nCoordinates are now " + self.tab3.coords.to_string(style="hmsdms", sep=":", precision=1) + "." + "\n\nCurrent information" + printers.get_tab_three_info(self)
    except (ValueError, TypeError):
        pass
    self.tab3.label_info.setText(update)

# Change Dec to user input
def change_dec(self):
    update = "Dec could NOT be updated.\nEnsure that the value entered matches a valid format (e.g., Deg:MM:SS)." + "\n\nCurrent information" + printers.get_tab_three_info(self)
    try:
        new_dec = self.tab3.dec_input.text()
        coord_str_1 = str(self.tab3.ra) 
        coord_str_2 = str(new_dec)
        new_coords = SkyCoord(coord_str_1, coord_str_2, unit=(u.hour, u.deg), frame='icrs')
        self.tab3.coords = new_coords
        self.tab3.dec = new_dec
        self.tab3.current_target = FixedTarget(self.tab3.coords, name="Custom Coordinates Plot")
        update = "Updated Dec to " + str(self.tab3.dec) + ".\nCoordinates are now " + self.tab3.coords.to_string(style="hmsdms", sep=":", precision=1) + "." + "\n\nCurrent information" + printers.get_tab_three_info(self)
    except (ValueError, TypeError):
        pass
    self.tab3.label_info.setText(update)

# Change time to user input, resulting in a static datetime
def change_time(self):
    update = "Time could NOT be updated.\nEnsure that the value entered matches a valid format \n(e.g., 2024-12-20 02:12:02)." + "\n\nCurrent information" + printers.get_obs_info(self)
    try:
        new_time = self.tab4.time_input.text()
        new_time = parse(new_time)
        new_time = self.obs_timezone.localize(new_time)
        self.time_var = new_time
        self.use_curr_time = False
        # If tab2 has sheet uploaded, re-check obs windows   
        if self.sheet is not None:
            reset_tab2(self)
        time_arr = helpers.convert_time_to_string(self, self.time_var)
        update = "Updated time to " + time_arr[0] + " " + time_arr[1] + "." + "\n\nCurrent information" + printers.get_obs_info(self)
    except (ValueError, TypeError):
        pass
    except (ErfaWarning):           # Apparently there is time shenanigans about using certain dates. So.
        update = "Time could NOT be updated; the date was too far in the future/past."
    self.tab4.label_info.setText(update)

# Reset bool to using (approx.) Now wherever applicable instead of a static datetime
def use_now_time(self):
    self.use_curr_time = True
    temp_time = dt.datetime.now(self.obs_timezone)
    self.time_var = temp_time
    # If tab2 has sheet uploaded, re-check obs windows   
    if self.sheet is not None:
        reset_tab2(self)
    self.tab4.label_info.setText("Program will now use current time.\nIf applicable, submission targets have been reset." + "\n\nCurrent information" + printers.get_obs_info(self))

# Change longitude of observer
def change_lon(self):
    update = "Longitude could NOT be updated.\nEnsure that the value entered matches a valid format \n(e.g., 29.004)." + "\n\nCurrent information" + printers.get_obs_info(self)
    try:
        new_lon = self.tab4.obs_lon_input.text()
        lon_float = float(new_lon)
        new_obs = Observer(
            location=coordinates.EarthLocation(lat=self.obs_lat * u.deg, lon=lon_float * u.deg, height=self.obs_height * u.m),
            timezone=self.obs_timezone,
            name=self.obs_name
        )
        self.obs = new_obs
        self.obs_lon = lon_float
        update = "Updated longitude to " + str(self.obs_lon) + "." + "\n\nCurrent information" + printers.get_obs_info(self) + "\n\nCurrent information" + printers.get_obs_info(self)
    except(ValueError, TypeError):
        pass
    self.tab4.label_info.setText(update)

    # If tab2 has sheet uploaded, re-check obs windows   
    if self.sheet is not None:
        reset_tab2(self)

# Change latitude of observer
def change_lat(self):
    update = "Latitude could NOT be updated.\nEnsure that the value entered matches a valid format \n(e.g., -82.58)." + "\n\nCurrent information" + printers.get_obs_info(self)
    try:
        new_lat = self.tab4.obs_lat_input.text()
        lat_float = float(new_lat)
        new_obs = Observer(
            location=coordinates.EarthLocation(lat=lat_float * u.deg, lon=self.obs_lon * u.deg, height=self.obs_height * u.m),
            timezone=self.obs_timezone,
            name=self.obs_name
        )
        self.obs = new_obs
        self.obs_lat = lat_float
        # ^ this is AFTER attempt to define observer so the value is ensured correct
        update = "Updated latitude to " + str(self.obs_lat) + "." + "\n\nCurrent information" + printers.get_obs_info(self)
    except(ValueError, TypeError):
        pass
    self.tab4.label_info.setText(update)

    # If tab2 has sheet uploaded, re-check obs windows   
    if self.sheet is not None:
        reset_tab2(self)

# Change timezone of observer and update time accordingly
def change_timezone(self):
    update = "Time zone could NOT be updated.\nEnsure that the value entered matches a valid format according to tz database time zones \n(e.g., 'US/Eastern')." + "\n\nCurrent information" + printers.get_obs_info(self)
    try:
        new_tz = self.tab4.obs_timezone_dropdown.currentText()
        new_tz = new_tz.split("- ")[1]
        new_tz = new_tz.split(" (")[0]      # Get timezone Name by itself (excludes acronym and UTC value)
        if (new_tz == "Coordinated Universal Time"):
            new_tz = "UTC"
        new_obs = Observer(
            location=coordinates.EarthLocation(lat=self.obs_lat * u.deg, lon=self.obs_lon * u.deg, height=self.obs_height * u.m),
            timezone=new_tz,
            name=self.obs_name
        )
        self.obs = new_obs
        new_tz = pytz.timezone(new_tz)
        self.obs_timezone = new_tz

        # Refresh Now time     
        if self.use_curr_time:
            self.time_var = dt.datetime.now(self.obs_timezone)
        else:
            # If not using Now, translate entered time to new timezone
            new_time = self.time_var.astimezone(self.obs_timezone)
            self.time_var = new_time

        time_arr = helpers.convert_time_to_string(self, self.time_var)
        update = "Updated timezone to " + str(self.obs_timezone) + " and time to " + time_arr[0] + " " + time_arr[1] + "." + "\n\nCurrent information" + printers.get_obs_info(self)
    except(ValueError, TypeError, UnknownTimeZoneError):
        pass
    self.tab4.label_info.setText(update)

    # If tab2 has sheet uploaded, re-check obs windows   
    if self.sheet is not None:
        reset_tab2(self)

# Change name of observer - I don't believe this has any functional repercussions
def change_name(self):
    update = "Name could NOT be updated.\nEnsure that a value was entered." + "\n\nCurrent information" + printers.get_obs_info(self)
    try:
        new_name = self.tab4.obs_name_input.text()
        new_obs = Observer(
            location=coordinates.EarthLocation(lat=self.obs_lat * u.deg, lon=self.obs_lon * u.deg, height=self.obs_height * u.m),
            timezone=self.obs_timezone,
            name=new_name
        )
        self.obs = new_obs
        self.obs_name = new_name
        update = "Updated name to " + str(self.obs_name) + "." + "\n\nCurrent information" + printers.get_obs_info(self)
    except(ValueError, TypeError):
        pass
    self.tab4.label_info.setText(update)

# Change altitude of observer
def change_height(self):
    update = "Height could NOT be updated.\nEnsure that the value entered matches a valid format \n(e.g., 23)." + "\n\nCurrent information" + printers.get_obs_info(self)
    try:
        new_height = self.tab4.obs_height_input.text()
        height_float = float(new_height)
        new_obs = Observer(
            location=coordinates.EarthLocation(lat=self.obs_lat * u.deg, lon=self.obs_lon * u.deg, height=height_float * u.m),
            timezone=self.obs_timezone,
            name=self.obs_name
        )
        self.obs = new_obs
        self.obs_height = height_float
        update = "Updated height to " + str(self.obs_height) + "." + "\n\nCurrent information" + printers.get_obs_info(self)
    except(ValueError, TypeError):
        pass
    self.tab4.label_info.setText(update)

# Called when USER resets observer 
def reset_observer_with_message(self):
    reset_observer(self)
    print_info = "Observer values have been set to default (Rosemary Hill Observatory)." + "\n\nCurrent information" + printers.get_obs_info(self)
    self.tab4.label_info.setText(print_info)

# Called when program initially sets observer (at beginning of runtime)
def reset_observer(self):
    self.obs_lat = float(DEF_LATITUDE)
    self.obs_lon = float(DEF_LONGITUDE)
    self.obs_height = float(DEF_HEIGHT)
    self.obs_timezone = pytz.timezone(str(DEF_TIMEZONE))
    self.obs_name = str(DEF_NAME)

    self.obs = Observer(
        location=coordinates.EarthLocation(lat=DEF_LATITUDE * u.deg, lon=DEF_LONGITUDE * u.deg, height=DEF_HEIGHT * u.m),
        timezone=DEF_TIMEZONE,
        name=DEF_NAME
    )

# Failure condition, set to defaults
def set_default(self, tab, msg):           
    tab.label_info.setText("")
    time.sleep(1)
    tab.label_info.setText(msg)
    tab.coords = SkyCoord("00:00:00.00 00:00:00.00", unit=(u.hour, u.deg), frame='icrs')
    tab.current_target = FixedTarget(tab.coords, name="Default Coordinates Plot")
    tab.current_target_name = "Default"
    tab.result_table = None   

def reset_tab2(self):
    # Update target list etc etc
    if initwin.init_tab2_target_names(self):
        self.tab2.label_info.setText("Submission targets reset.")

        self.tab2.targets_dropdown.clear()                      # Reset dropdown menu

        if not self.tab2.only_show_up:                          # If all targets are being shown, add all to dropdown
            self.tab2.targets_dropdown.addItems(self.tab2.target_names)             
            self.tab2.current_target_name = self.tab2.target_names[0]
        else:                                                   # If only Up targets are being shown, add only up targets to dropdown
            self.tab2.targets_dropdown.addItems(self.tab2.up_target_names)
            self.tab2.current_target_name = self.tab2.up_target_names[0]

def set_observatory(self):
    update = "Observatory could not be updated." + "\n\nCurrent information" + printers.get_obs_info(self)
    new_obs_name = self.tab4.obs_list_dropdown.currentText()
    try:      
        index_of_name = self.observatories_names.index(new_obs_name) 
        self.obs = self.observatories[index_of_name]
        self.obs_lat = float(self.obs.latitude / u.deg)
        self.obs_lon = float(self.obs.longitude / u.deg)
        self.obs_height = float(self.obs.elevation / u.m)
        self.obs_timezone = pytz.timezone(str(self.obs.timezone))
        self.obs_name = self.obs.name
        update = "Updated observatory to " + str(self.obs_name) + "." + "\n\nCurrent information" + printers.get_obs_info(self)
    except(ValueError, KeyError):
        pass
    self.tab4.label_info.setText(update)
