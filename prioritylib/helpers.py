from lib import *
from prioritylib.global_ import *
import prioritylib.setters as setters
# Convert Time object to EST (where RHO is located)
def eastern(self, time, rise_set_bool):
    if rise_set_bool or self.use_curr_time:
        est = time.to_datetime(timezone=RHO.timezone)
        return est.strftime('%H:%M:%S')
    return time.strftime("%H:%M:%S")

# Determines which objects are above horizon
def determine_up(targets, obj_names, self, tab):
    if not targets:
        setters.set_default(self, tab, "Could not complete action.")
        return
    
    if self.use_curr_time:
        self.time_var = Time.now()                    # Update time If Needed
    new_list = []                                     # List of objects with up info
    index = 0

    tab.up_target_names = []

    for obj in targets:
        obj_name = obj_names[index]
        if "(Up)" in obj_name:                        # Cuts off the (Up) part of the name if the star is indeed up
            obj_name = obj_name[0:-5]
        if RHO.target_is_up(self.time_var, obj):
            new_list.append(obj_name + " (Up)")       # So user can see if a given object is in the sky. I maybe should've done this in a smarter manner but it's too late now!!!!
            tab.up_target_names.append(obj_name + " (Up)")
        else:
            new_list.append(obj_name)
        index += 1
    tab.label_info.setText("Target \"Up\" Status successfully updated.")
    tab.target_names = new_list
    
    tab.targets_dropdown.clear()                      # Reset dropdown menu

    if not tab.only_show_up:                          # If all targets are being shown, print these
        tab.targets_dropdown.addItems(tab.target_names)             
        tab.current_target_name = tab.target_names[0]
    else:                                             # If only Up targets are being shown, print these
        tab.targets_dropdown.addItems(tab.up_target_names)
        tab.current_target_name = tab.up_target_names[0]

    tab.targets_dropdown.setCurrentText(tab.current_target_name)        # Re-set current dropdown text
    if update(self, tab):
        return True

# Kind of a vague but important function for checking, not so necessarily an update now
def update(self, tab):
    if self.use_curr_time:
        self.time_var = Time.now()                                # Update time If needed

    name = tab.targets_dropdown.currentText()
    if name == '' or tab.target_names is None:                    # Don't do anything if there's no target chosen or list uploaded
        return False
    
    up_name = name
    if "(Up)" in name:              # Cuts off the (Up) part of the name if the star is indeed up, so SIMBAD can query
        name = name[0:-5]

    index_of_name = 0
    if up_name in tab.target_names:                        # Doesn't have to check both lists since the given name will be in the target_names list or something is broken
        index_of_name = tab.target_names.index(up_name)
        tab.current_target = tab.targets[index_of_name]
    tab.current_target_name = name

    if tab is self.tab2:                                   # Change current values for tab2 without doing tab1 things  
        tab.coords = tab.current_target.coord
        tab.targets_dropdown.clear()       
        if not tab.only_show_up:
            tab.targets_dropdown.addItems(tab.target_names)
        else:
            tab.targets_dropdown.addItems(tab.up_target_names)
        
        if RHO.target_is_up(self.time_var, tab.current_target):
            tab.targets_dropdown.setCurrentText(up_name)
            tab.target_names[index_of_name] = up_name
        else:
            tab.targets_dropdown.setCurrentText(name)
            tab.target_names[index_of_name] = name
        return True
    
    try:                                                   # Aforementioned tab1 things
        result_table = Simbad.query_object(tab.current_target_name)[["main_id", "ra", "dec", "V"]]
        tab.result_table = result_table
        tab.coords = SkyCoord(ra=result_table["ra"], dec=tab.result_table["dec"])
        if up_name not in tab.target_names:
            tab.current_target = FixedTarget(tab.coords, name=name)
            tab.targets.insert(0, tab.current_target)
            tab.target_names.insert(0, name)
            if RHO.target_is_up(self.time_var, tab.current_target):
                name = name + " (Up)"
                tab.up_target_names.insert(0, name)     
                up_name = name
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError, AttributeError):
        return False        

    tab.targets_dropdown.clear()       
    if not tab.only_show_up:
        tab.targets_dropdown.addItems(tab.target_names)
    else:
        tab.targets_dropdown.addItems(tab.up_target_names)
    
    if RHO.target_is_up(self.time_var, tab.current_target):
        tab.targets_dropdown.setCurrentText(up_name)
        tab.target_names[index_of_name] = up_name
    else:
        tab.targets_dropdown.setCurrentText(name)
        tab.target_names[index_of_name] = name
    return True

# Toggle for whether or not unrisen objects appear
def change_only_show_up(self, tab):
    set_label = ""
    if not tab.only_show_up:
        tab.only_show_up = True
        tab.show_up_button.setText("Show All Targets")
        set_label = "Now showing only up targets."
    else:
        tab.only_show_up = False
        tab.show_up_button.setText("Only Show Up Targets")
        set_label = "Now showing all targets."
    determine_up(tab.targets, tab.target_names, self, tab)
    tab.label_info.setText(set_label)