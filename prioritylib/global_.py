import astropy.coordinates as coordinates
from astroplan import Observer
from astropy import units as u

RHO = Observer(
    location=coordinates.EarthLocation(lat=29.4001, lon=-82.5862*u.deg, height=23*u.m),
    timezone='US/Eastern',
    name='Rosemary Hill Observatory'
)

EXTRA_ROWS = 2

# These must be manually updated if changes to the template are made !!!
NAME = "Primary Identifier**"
SEC_NAME = "Secondary Identifier \n(e.g., planet)"
RA = "RA**"
DEC = "Dec**"
MAG_V = "V Magnitude**"	
MAG_B = "B Magnitude"
OBS_WIN_OPEN = "Obs. window \n opens*"	
OBS_WIN_CLOSE = "Obs. window\n closes*"	
PRIORITY = "Priority*"
QUAL = "Preferred Quality"
FIL_B = "B"
FIL_G = "G"
FIL_R = "R"
FIL_I = "I"
FIL_Z = "Z"
FIL_H = "H-alpha"
FIL_O = "O III"
FIL_S = "S II"
BASELINE = "Baseline*"
PROCEDURES = "Observation procedures*"
JUSTIFICATION = "Scientific justification"
NOTES = "Notes?"

COLUMNS = [NAME, SEC_NAME, RA, DEC, MAG_V, MAG_B, 
           OBS_WIN_OPEN, OBS_WIN_CLOSE, PRIORITY, 
           FIL_B, FIL_G, FIL_R, FIL_I, FIL_Z, FIL_H, FIL_O, FIL_S, 
           BASELINE, PROCEDURES, JUSTIFICATION, NOTES]

PRETTY_COLUMNS = ["Name", "Secondary Name", "\nRA", "Dec", "\nV Magnitude", "B Magnitude",
                  "\nObs. window opens", "Obs. window closes", "Priority",
                  "\nB Filter", "G Filter", "R Filter", "I Filter", "Z Filter", "H-alpha Filter", "O III Filter", "S II Filter",
                  "\nBaseline", "\nObservation procedures", "\nScientific Justification", "\nNotes"]

SORT_NAMES_1 = ["Brightest", "Dimmest"]
SORT_NAMES_2 = ["Brightest", "Dimmest", "Priority"]