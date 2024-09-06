from lib import *
import prioritylib.helpers as helpers
from prioritylib.global_ import *

# Get info of object and print to label
def get_info_of_obj(self, tab):
    if tab.target_names is not None:
        if not helpers.update(self, tab):
            return
    try: 
        result_table = Simbad.query_object(tab.current_target_name)[["main_id", "ra", "dec", "V"]]
        tab.coords = SkyCoord(ra=result_table["ra"], dec=result_table["dec"])
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError, AttributeError):
        tab.label_info.setText("Object not found. Check spelling and try again.")
        if tab is self.tab2:
            print_csv_target(self)
        return
    
    tab.result_table = result_table
    now = Time.now()

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
        coords_ra = result_table["ra"]
        coords_dec = result_table["dec"]

    # Idk what to say abt this, sometimes the true/false comes like [True] and other times it comes like True. I don't get it .
    up_now = str(RHO.target_is_up(now, tab.current_target))
    if "[" in up_now:
        up_now = up_now.split("[")[1]
        up_now = up_now.split("]")[0]

    alt_az = tab.coords.transform_to(AltAz(obstime=now, location=RHO.location))
    str_alt = str(alt_az.alt)[1:-8] + "s"
    str_az = str(alt_az.az)[1:-8] + "s"
    
    # Gather relevant info
    str_info = ""
    str_info += "Name: " + tab.current_target_name + "\n"
    str_info += "Identifier: " + info[0] + "\n"
    str_info += "Up now: " + up_now + "\n\n"
    str_info += "Coordinates: " + coords_ra + ", " + coords_dec + "\n"      
    str_info += "Magnitude V: " + str(round(float(info[2]), 5)) + "\n\n"
    try: 
        rise_set = [helpers.eastern(RHO.target_rise_time(time=now, target=tab.current_target)), helpers.eastern(RHO.target_set_time(time=now, target=tab.current_target))]
        str_info += "Rises: " + rise_set[0] + " EST" + "\n"
        str_info += "Sets: " + rise_set[1] + " EST" + "\n\n"
    except (TargetAlwaysUpWarning, TargetNeverUpWarning, AttributeError):
        str_info += "Rises: Does not rise\n"
        str_info += "Sets: Does not set\n\n"
    str_info += "Altitude: " + str_alt + "\n"
    str_info += "Azimuth: " + str_az
    
    # Set label as the string info
    tab.label_info.setText(str_info)


def print_csv_target(self):
    update = "Could not complete action. Ensure a target is uploaded and selected."
    if self.tab2.current_target_name != "Default":
        name = self.tab2.current_target_name
        name_up = self.tab2.current_target_name + " (Up)"
        if name in self.tab2.target_names:
            index_of_name = self.tab2.target_names.index(name) + 2      # Plus 2 because ignoring first few rows
        elif name_up in self.tab2.target_names:
            index_of_name = self.tab2.target_names.index(name_up) + 2
        else:
            self.tab2.label_info.setText(update)
            return

        now = Time.now()
        up_now = str(RHO.target_is_up(now, self.tab2.current_target))
        if "[" in up_now:
            up_now = up_now.split("[")[1]
            up_now = up_now.split("]")[0]

        update = ""
        for column in COLUMNS:
            update += column + ": " 
            value = str(self.sheet[column][index_of_name])
            if value == "nan":
                value = "Not given"
            update += value + "\n"

        alt_az = self.tab2.coords.transform_to(AltAz(obstime=now, location=RHO.location))
        str_alt = str(alt_az.alt)[1:-8] + "s"
        str_az = str(alt_az.az)[1:-8] + "s"

        try: 
            rise_set = [helpers.eastern(RHO.target_rise_time(time=now, target=self.tab2.current_target)), helpers.eastern(RHO.target_set_time(time=now, target=self.tab2.current_target))]
            update += "Rises: " + rise_set[0] + " EST" + "\n"
            update += "Sets: " + rise_set[1] + " EST" + "\n\n"
        except (TargetAlwaysUpWarning, TargetNeverUpWarning, AttributeError):
            update += "Rises: Does not rise\n"
            update += "Sets: Does not set\n\n"

        update += "Altitude: " + str_alt + "\n"
        update += "Azimuth: " + str_az

    self.tab2.label_info.setText(update)