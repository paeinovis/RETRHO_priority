from lib import *
from prioritylib.global_ import *

def eastern(time):
    est = time.to_datetime(timezone=RHO.timezone)
    return est.strftime('%H:%M:%S')

# Determines which objects are above horizon
def determine_up(targets, obj_names, self, tab):
    if not targets:
        tab.label_info.setText("Could not complete action.")
        return
    
    now = Time.now()                                # Update time
    new_list = []                                   # List of objects with up info
    index = 0

    for obj in targets:
        obj_name = obj_names[index]
        if "(Up)" in obj_name:                        # Cuts off the (Up) part of the name if the star is indeed up
            obj_name = obj_name[0:-5]
        if RHO.target_is_up(now, obj):
            new_list.append(obj_name + " (Up)")       # So user can see if a given object is in the sky
        else:
            new_list.append(obj_name)
        index += 1
    tab.label_info.setText("Target \"Up\" Status successfully updated.")
    tab.target_names = new_list
    tab.current_target_name = tab.target_names[0]
    tab.targets_dropdown.clear()       
    tab.targets_dropdown.addItems(tab.target_names)
    tab.targets_dropdown.setCurrentText(tab.current_target_name)
    update(self, tab)

# Update dropdown menu stuff if needed
def update(self, tab):
    name = tab.targets_dropdown.currentText()
    if name == '':
        tab.label_info.setText("Could not complete action. Ensure a target is uploaded and selected.")
        return False
    
    if name in tab.target_names:
        index_of_name = tab.target_names.index(name)
    if "(Up)" in name:              # Cuts off the (Up) part of the name if the star is indeed up, so SIMBAD can query
        name = name[0:-5]
    tab.current_target_name = name

    if tab is self.tab2:
        tab.current_target = tab.targets[index_of_name]
        tab.coords = SkyCoord(ra=tab.current_target.ra, dec=tab.current_target.dec)
        tab.targets_dropdown.clear()       
        tab.targets_dropdown.addItems(tab.target_names)
        now = Time.now()                                # Update time
        if RHO.target_is_up(now, tab.current_target):
            name = name + " (Up)"      
        tab.targets_dropdown.setCurrentText(name)
        return True
    
    try: 
        result_table = Simbad.query_object(tab.current_target_name)[["main_id", "ra", "dec", "V"]]
        tab.result_table = result_table
        tab.coords = SkyCoord(ra=result_table["ra"], dec=tab.result_table["dec"])
        if name not in tab.target_names:
            tab.current_target = FixedTarget(tab.coords, name=name)
            tab.targets.append(tab.current_target)
            now = Time.now()                                # Update time
            if RHO.target_is_up(now, tab.current_target):
                name = name + " (Up)"      
            tab.target_names.insert(0, name)
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError, AttributeError):
        pass

    tab.targets_dropdown.clear()       
    tab.targets_dropdown.addItems(tab.target_names)
    tab.targets_dropdown.setCurrentText(name)
    return True