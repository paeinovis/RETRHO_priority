import astropy.coordinates as coordinates
from astroplan import Observer
from astropy import units as u
import pytz
import csv

DEF_LATITUDE = 29.4001          # (degrees)
DEF_LONGITUDE = -82.5862        # (degrees)
DEF_HEIGHT = 23                 # (meters)
DEF_TIMEZONE = pytz.timezone('US/Eastern')
DEF_NAME = 'Rosemary Hill Observatory'

# These must be manually updated if changes to the template are made !!!
NAME = "Primary Identifier**"
SEC_NAME = "Secondary Identifier \n(e.g., planet, common name, or reference object)"
RA = "RA**"
DEC = "Dec**"
TYPE_OF_OBJECT = "Type of Object**"
MAG_V = "V Magnitude**"	
MAG_B = "B Magnitude"
OBS_WIN_OPEN = "Obs. window opens*"	
OBS_WIN_CLOSE = "Obs. window closes*"	
PRIORITY = "Priority*"
QUAL = "Preferred Quality"
FIL_B = "B"
FIL_G = "g"
FIL_R = "r"
FIL_I = "i"
FIL_Z = "z"
FIL_H = "H-alpha"
FIL_O = "O III"
FIL_S = "S II"
BASELINE = "Baseline*"
PROCEDURES = "Observation procedures*"
JUSTIFICATION = "Scientific justification"
NOTES = "Notes?"

COLUMNS = [NAME, SEC_NAME, TYPE_OF_OBJECT, RA, DEC, MAG_V, MAG_B, 
           OBS_WIN_OPEN, OBS_WIN_CLOSE, PRIORITY, 
           FIL_B, FIL_G, FIL_R, FIL_I, FIL_Z, FIL_H, FIL_O, FIL_S, 
           BASELINE, PROCEDURES, JUSTIFICATION, NOTES]

PRETTY_COLUMNS = ["Name", "Secondary Name", "Type of Object", "\nRA", "Dec", "\nV Magnitude", "B Magnitude",
                  "\nObs. window opens", "Obs. window closes", "Priority",
                  "\nB Filter", "g Filter", "r Filter", "i Filter", "z Filter", "H-alpha Filter", "O III Filter", "S II Filter",
                  "\nBaseline", "\nObservation procedures", "\nScientific Justification", "\nNotes"]

SORT_NAMES_1 = ["Brightest", "Dimmest"]
SORT_NAMES_2 = ["Brightest", "Dimmest", "Highest Priority"]



