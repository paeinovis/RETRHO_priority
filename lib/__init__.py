import astropy
import astroquery
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from astropy.time import Time
from astroplan.plots import plot_airmass, plot_finder_image, plot_sky
from astroquery.simbad import Simbad
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QPushButton, QWidget, QAction, QVBoxLayout, QLabel, QTabWidget, QInputDialog, QLineEdit, QFileDialog, QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import astropy.coordinates as coordinates
import time

# Warnings imports
from astroquery.simbad.core import NoResultsWarning
from astropy.coordinates.name_resolve import NameResolveError
from erfa import ErfaWarning
import warnings
warnings.filterwarnings("ignore", message="Numerical value without unit or explicit format passed to TimeDelta, assuming days")
warnings.filterwarnings("error")
warnings.filterwarnings("ignore", message="The plot_date function was deprecated in Matplotlib 3.9 and will be removed in 3.11. Use plot instead.")
from astroplan import FixedTarget, Observer, TargetAlwaysUpWarning, TargetNeverUpWarning
from pyvo.dal.exceptions import DALFormatError, DALAccessError, DALServiceError, DALQueryError
from astropy.utils import iers
# iers.conf.IERS_A_URL = 'ftp://cddis.gsfc.nasa.gov/pub/products/iers/finals2000A.all'
# iers.conf.IERS_A_URL_MIRROR = 'https://datacenter.iers.org/data/9/finals2000A.all'
# from astroplan import download_IERS_A
# download_IERS_A()

import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication

import qdarktheme
