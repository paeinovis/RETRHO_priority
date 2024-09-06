from lib import *
from prioritylib.global_ import *

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
        update = "Uupdated Dec to " + str(self.tab3.dec) + ".\nCoordinates are now " + self.tab3.coords.to_string(style="hmsdms", sep=":", precision=1) + "."
    except (ValueError):
        pass
    self.tab3.label_info.setText(update)
