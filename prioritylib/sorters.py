from lib import *
from prioritylib.global_ import *
import prioritylib.initwin as initwin
import prioritylib.setters as setters
import prioritylib.helpers as helpers

# Sorting here is more complicated since the values aren't immediately ready . I don't know why I felt the need to implement sorts in both tabs but here we are.
def sort_targets_tab1(self):
    sort = self.tab1.sort_dropdown.currentText()
    if sort == '':                    # Don't do anything if there's no target chosen or list uploaded
        setters.set_default(self, self.tab1, "Could not complete action. Ensure a sort method is chosen.")
        return
    
    # Default sort lowest to highest - brightest to dimmest
    self.tab1.mags, self.tab1.target_names = zip(*sorted(zip(self.tab1.mags, self.tab1.target_names)))

    if sort == "Brightest":
        # Already complete
        pass
    elif sort == "Dimmest":
        # Flip both lists
        self.tab1.mags = self.tab1.mags[::-1]
        self.tab1.target_names = self.tab1.target_names[::-1]
    else:
        setters.set_default(self, self.tab1, "Could not complete action.")
        return
    
    initwin.init_tab1_target_names(self, self.tab1.target_names)
    helpers.determine_up(self.tab1.targets, self.tab1.target_names, self, self.tab1)
    self.tab1.label_info.setText("Sort complete.")

# Sort sheet values with a switch case depending on what is selected
# FIXME: should eventually add ways to do current-date stuff and Obs Window
def sort_targets_tab2(self):
    sort = self.tab2.sort_dropdown.currentText()
    if sort == '':                    # Don't do anything if there's no target chosen or list uploaded
        setters.set_default(self, self.tab2, "Could not complete action. Ensure a sort method is chosen.")
        return
    match sort:
        case "Brightest":
            self.sheet.sort_values([MAG_V], inplace=True, ignore_index=True)
        case "Dimmest":
            self.sheet.sort_values(MAG_V, ascending=False, inplace=True, ignore_index=True)
        case "Highest Priority":
            self.sheet.sort_values(PRIORITY, inplace=True, ignore_index=True)
        # I'd add Lowest priority, but I don't see why that would be useful?
    # Update target list etc etc
    if initwin.init_tab2_target_names(self, 0, len(self.sheet)):
        self.tab2.label_info.setText("Sort complete.")