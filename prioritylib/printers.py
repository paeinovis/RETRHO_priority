from lib import *
import prioritylib.helpers as helpers
import prioritylib.setters as setters
from prioritylib.global_ import *

# Get info of object and print to label
def get_info_of_obj(self, tab):
    if not helpers.update(self, tab):
        if tab is self.tab2:
            print_csv_target(self)
        else:                           # If fail And NOT something that can default to CSV, set defaults.
            setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return

    try: 
        result_table = Simbad.query_object(tab.current_target_name)[["main_id", "ra", "dec", "V"]]
        tab.result_table = result_table
        tab.coords = SkyCoord(ra=result_table["ra"], dec=result_table["dec"])
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError, AttributeError):
        if tab is self.tab2:
            print_csv_target(self)
        else:
            setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return

    # SIMBAD shenanigans to get some relevant info and convert it to hmsdms bc SIMBAD doesn't do that natively anymore???
    info = [tab.result_table["main_id"][0], tab.coords.to_string('hmsdms'), tab.result_table["V"][0]]

    # Cutting off the long decimal points for readibility w/o rounding - we don't need to be That precise
    if "." in str(info[1]) and " " in str(info[1]):
        coords_str = str(info[1]).split(".")
        coords_2 = coords_str[1].split(" ")
        coords_ra = coords_str[0][2:] + "." + coords_2[0][:2] + "s"
        coords_dec = coords_2[1][:] + "." + coords_str[2][:2] + "s"
    # In the unlikely event they're not separated in the way I'm expecting .
    else:                        
        coords_ra = tab.result_table["ra"]
        coords_dec = tab.result_table["dec"]

    # Idk what to say abt this, sometimes the true/false comes like [True] and other times it comes like True. I don't get it .
    up_now = str(RHO.target_is_up(self.time_var, tab.current_target))
    if "[" in up_now:
        up_now = up_now.split("[")[1]
        up_now = up_now.split("]")[0]

    alt_az = tab.coords.transform_to(AltAz(obstime=self.time_var, location=RHO.location))
    str_alt = str(alt_az.alt)[1:-8] 
    if "s" not in str_alt:
        str_alt += "s"
    str_az = str(alt_az.az)[1:-8]
    if "s" not in str_az:
        str_az += "s"
    
    # Gather relevant info
    str_info = ""
    str_info += "Program time: " + str(self.time_var)[0:10] + " " + str(helpers.eastern(self, self.time_var, False)) +"\n\n"
    str_info += "Name: " + tab.current_target_name + "\n"
    str_info += "Identifier: " + info[0] + "\n"
    str_info += "Up now: " + up_now + "\n\n"
    str_info += "Coordinates RA: " + coords_ra + "\n"
    str_info += "Coordinates DEC: " + coords_dec + "\n"      
    try:
        str_info += "Magnitude V: " + str(round(float(info[2]), 5)) + "\n\n"
    except (UserWarning):
        str_info += "Magnitude V: Not available\n\n"
    try: 
        rise_set = [helpers.eastern(self, RHO.target_rise_time(time=self.time_var, target=tab.current_target), True), helpers.eastern(self, RHO.target_set_time(time=self.time_var, target=tab.current_target), True)]
        str_info += "Rises: " + rise_set[0] + " EST" + "\n"
        str_info += "Sets: " + rise_set[1] + " EST" + "\n"
        if up_now == "True":
            diff_rise = abs(self.time_var - RHO.target_rise_time(time=self.time_var, target=tab.current_target))
            diff_set = abs(self.time_var - RHO.target_set_time(time=self.time_var, target=tab.current_target))
            if diff_rise > diff_set:
                str_info += "Currently setting\n\n" 
            else:
                str_info += "Currently rising\n\n"
        else:
            str_info += "Currently below horizon\n\n"
    except (TargetAlwaysUpWarning, TargetNeverUpWarning, AttributeError):
        str_info += "Rises: Does not rise\n"
        str_info += "Sets: Does not set\n"
        str_info += "Circumpolar\n\n"
    str_info += "Altitude: " + str_alt + "\n"
    str_info += "Azimuth: " + str_az
    
    # Set label as the string info
    tab.label_info.setText(str_info)

# Used for tab2 CSV-submitted objects (when SIMBAD can't find them or people want CSV info specifically)
def print_csv_target(self):
    helpers.update(self, self.tab2)         
    str_info = "Could not complete action. Ensure a target is uploaded and selected."
    if self.tab2.current_target_name != "Default":
        name = self.tab2.current_target_name
        name_up = self.tab2.current_target_name + " (Up)"
        if name in self.tab2.target_names:
            index_of_name = self.tab2.target_names.index(name) + EXTRA_ROWS      # Ignore the first few rows
        elif name_up in self.tab2.target_names:
            index_of_name = self.tab2.target_names.index(name_up) + EXTRA_ROWS
        else:
            setters.set_default(self, self.tab2, str_info)
            return

        str_info = ""
        
        index = 0                                       # Grab Relevant CSV columns and values
        for column in COLUMNS: 
            # This is here for aesthetic purposes in print - makes more sense to have the rise/set time, up status, etc Before observing info
            # Makes sense chronologically for the code Below 
            if PRETTY_COLUMNS[index] == "\nB Filter":
                str_info += "\nProgram time: " + str(self.time_var)[0:10] + " " + str(helpers.eastern(self, self.time_var, False)) +"\n"
                up_now = str(RHO.target_is_up(self.time_var, self.tab2.current_target))
                if "[" in up_now:
                    up_now = up_now.split("[")[1]
                    up_now = up_now.split("]")[0]
                str_info += "Up now: " + up_now + "\n"

                alt_az = self.tab2.coords.transform_to(AltAz(obstime=self.time_var, location=RHO.location))
                str_alt = str(alt_az.alt)[0:-7] 
                if "s" not in str_alt:
                    str_alt += "s"
                str_az = str(alt_az.az)[0:-7]
                if "s" not in str_az:
                    str_az += "s"

                try: 
                    rise_set = [helpers.eastern(self, RHO.target_rise_time(time=self.time_var, target=self.tab2.current_target), True), helpers.eastern(self, RHO.target_set_time(time=self.time_var, target=self.tab2.current_target), True)]
                    str_info += "\nRises: " + rise_set[0] + " EST" + "\n"
                    str_info += "Sets: " + rise_set[1] + " EST" + "\n"
                    if up_now == "True":
                        diff_rise = abs(self.time_var - RHO.target_rise_time(time=self.time_var, target=self.tab2.current_target))
                        diff_set = abs(self.time_var - RHO.target_set_time(time=self.time_var, target=self.tab2.current_target))
                        if diff_rise > diff_set:
                            str_info += "Currently setting\n\n" 
                        else:
                            str_info += "Currently rising\n\n"
                    else:
                        str_info += "Currently below horizon\n\n"
                except (TargetAlwaysUpWarning, TargetNeverUpWarning, AttributeError):
                    str_info += "\nRises: Does not rise\n"
                    str_info += "Sets: Does not set\n"
                    str_info += "Circumpolar\n\n"
                str_info += "Altitude: " + str_alt + "\n"
                str_info += "Azimuth: " + str_az + "\n"
            
            # Prints info from CSV per column 
            str_info += PRETTY_COLUMNS[index] + ": "      # Unfortunately, the Names of the columns are not easy to read. So PRETTY_COLUMNS are the stringified versions
            value = str(self.sheet[column][index_of_name])
            if value == "nan":
                value = "Not given"
            str_info += value + "\n"
            index += 1

    self.tab2.label_info.setText(str_info)

