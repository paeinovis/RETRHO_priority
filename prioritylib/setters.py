from lib import *
from prioritylib.global_ import *
import prioritylib.initwin as initwin

# Change FOV to user input
def change_fov(self):
    update = "FOV could NOT be updated.\nEnsure that the value entered is a positive floating point number."
    try:
        new_fov = float(self.tab3.fov_input.text())
        if (new_fov > 0):
            self.fov = new_fov * u.arcmin
            update = "Successfully updated FOV to " + str(self.fov) + "."
    except (ValueError):
        pass
    self.tab3.label_info.setText(update)

# Change RA to user input
def change_ra(self):
    update = "RA could NOT be updated.\nEnsure that the value entered matches a valid format (e.g., HH:MM:SS)."
    try:
        new_ra = self.tab3.ra_input.text()
        coord_str_1 = str(new_ra) 
        coord_str_2 = str(self.tab3.dec)
        new_coords = SkyCoord(coord_str_1, coord_str_2, unit=(u.hour, u.deg), frame='icrs')
        self.tab3.coords = new_coords
        self.tab3.ra = new_ra
        self.tab3.current_target = FixedTarget(self.tab3.coords, name="Custom Coordinates Plot")
        update = "Updated RA to " + str(self.tab3.ra) + ".\nCoordinates are now " + self.tab3.coords.to_string(style="hmsdms", sep=":", precision=1) + "."
    except (ValueError):
        pass
    self.tab3.label_info.setText(update)

# Change Dec to user input
def change_dec(self):
    update = "Dec could NOT be updated.\nEnsure that the value entered matches a valid format (e.g., Deg:MM:SS)."
    try:
        new_dec = self.tab3.dec_input.text()
        coord_str_1 = str(self.tab3.ra) 
        coord_str_2 = str(new_dec)
        new_coords = SkyCoord(coord_str_1, coord_str_2, unit=(u.hour, u.deg), frame='icrs')
        self.tab3.coords = new_coords
        self.tab3.dec = new_dec
        self.tab3.current_target = FixedTarget(self.tab3.coords, name="Custom Coordinates Plot")
        update = "Updated Dec to " + str(self.tab3.dec) + ".\nCoordinates are now " + self.tab3.coords.to_string(style="hmsdms", sep=":", precision=1) + "."
    except (ValueError):
        pass
    self.tab3.label_info.setText(update)

# Change time to user input, resulting in a static datetime
def change_time(self):
    update = "Time could NOT be updated.\nEnsure that the value entered matches a valid format \n(e.g., 2024-12-20 10:00:00)."
    try:
        new_time = self.tab3.time_input.text()
        new_time = Time(new_time)
        self.time_var = new_time
        self.use_curr_time = False
        # If tab2 has sheet uploaded, re-check obs windows   
        if self.sheet is not None:
            reset_tab2(self)
        update = "Updated time to " + str(self.time_var) + "."
    except (ValueError):
        pass
    except (ErfaWarning):           # Apparently there is time shenanigans about using certain dates. So.
        update = "Time could NOT be updated; the date was too far in the future/past."
    self.tab3.label_info.setText(update)

# Reset bool to using (approx.) Now wherever applicable instead of a static datetime
def use_now_time(self):
    self.use_curr_time = True
    self.time_var = Time.now() 
    # If tab2 has sheet uploaded, re-check obs windows   
    if self.sheet is not None:
        reset_tab2(self)
    self.tab3.label_info.setText("Program will now use current time.\nIf applicable, submission targets have been reset.")

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
