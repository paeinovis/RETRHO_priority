from lib import *
import prioritylib.helpers as helpers
import prioritylib.setters as setters
from prioritylib.global_ import *

# Plot finder image based on coordinates
def plot_coords(self, tab):
    if tab is self.tab3:
        title = "Finder image from coordinates (FOV = " + str(self.fov) + ")"
        title_2 = "Plot From Coordinates"
    elif tab is self.tab2:
        if not helpers.update(self, tab):           
            setters.set_default(self, tab, "Could not complete action. Ensure a target is uploaded and selected.")
            return  
        title = "Finder image for " + helpers.clip_name(tab.current_target_name) + " (FOV = " + str(self.fov) + ")"
        title_2 = helpers.clip_name(tab.current_target_name) + " Finder Plot"
    try:
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        ax, hdu = plot_finder_image(tab.coords, fov_radius=self.fov);
        wcs = WCS(hdu.header)
        ax.set_title(title)
        figure.add_subplot(ax, projection=wcs)
        canvas.setWindowTitle(title_2)
        canvas.setWindowIcon(QIcon('retrhogo.png'))
        canvas.show();
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError):
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return
    except (exceptions.LargeQueryWarning, ReadTimeout, TimeoutError, IERSWarning):
        setters.set_default(self, tab, "Download timed out, please try again.")
        return

# Plot finder image based on name    
def plot(self, tab):
    if not helpers.update(self, tab):          
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return  
                
    try: 
        result_table = Simbad.query_object(helpers.clip_name(tab.current_target_name))[["main_id", "ra", "dec", "V"]]
    
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        ax, hdu = plot_finder_image(tab.current_target, fov_radius=self.fov);
        wcs = WCS(hdu.header)
        title = "Finder image for " + helpers.clip_name(tab.current_target_name) + " (FOV = " + str(self.fov) + ")"
        ax.set_title(title)
        figure.add_subplot(ax, projection=wcs)
        title = helpers.clip_name(tab.current_target_name) + " Finder Plot"
        canvas.setWindowTitle(title)
        canvas.setWindowIcon(QIcon('retrhogo.png'))
        canvas.show()
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError):
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return
    except (exceptions.LargeQueryWarning, ReadTimeout, TimeoutError, IERSWarning):
        setters.set_default(self, tab, "Download timed out, please try again.")
        return

# Plot airmass based on target
def airmass_plot(self, tab):        
    if tab is self.tab3:
        title = "Airmass plot from coordinates"
        title_2 = "Airmass plot From Coordinates"
    elif not helpers.update(self, tab):          
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return  
    else:
        title = "Airmass plot for " + helpers.clip_name(tab.current_target_name)
        title_2 = helpers.clip_name(tab.current_target_name) + " Airmass Plot"

    if self.use_curr_time:
        self.time_var = dt.datetime.now(self.obs_timezone)                                # Update time If needed

    try: 
        figure = plt.figure(figsize=(8, 6))
        ax = plot_airmass(tab.current_target, 
                            observer=OBS, 
                            time=self.time_var, 
                            use_local_tz=True,
                            brightness_shading=True)
        ax.set_title(title)
        ax.grid(visible=True)   
        figure.add_subplot(ax)
        
        canvas = FigureCanvas(figure)
        canvas.setWindowTitle(title_2)
        canvas.setWindowIcon(QIcon('retrhogo.png'))
        canvas.show();
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError):
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return
    except (exceptions.LargeQueryWarning, ReadTimeout, TimeoutError, IERSWarning):
        setters.set_default(self, tab, "Download timed out, please try again.")
        return
    

# This is adapted from astropy documentation here: https://docs.astropy.org/en/latest/coordinates/example_gallery_plot_obs_planning.html
def az_time_plot(self, tab):
    if tab is self.tab3:
        title = "Altitude plot from coordinates"
        title_2 = "Altitude Plot from Coordinates"
        title_3 = "From coordinates"
    elif not helpers.update(self, tab):          
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return  
    else:
        title = "Altitude plot for " + helpers.clip_name(tab.current_target_name)
        title_2 = helpers.clip_name(tab.current_target_name) + " Altitude Plot"
        title_3 = helpers.clip_name(tab.current_target_name)

    if self.use_curr_time:
        self.time_var = dt.datetime.now(self.obs_timezone)                                # Update time If needed
    
    try: 
        delta_time = np.linspace(-12, 12, 1000) * u.hour
        times = Time(self.time_var) + delta_time
        frame = AltAz(obstime=times, location=OBS.location)
        altazs = tab.coords.transform_to(frame)

        figure, ax = plt.subplots(1, 1)
        canvas = FigureCanvas(figure)
        ax.set_title(title)

        mappable = ax.scatter(
            delta_time,
            altazs.alt,
            c=altazs.az.value,
            label=title_3,
            edgecolor='none',
            lw=0,
            s=8,
            cmap="gist_rainbow"
        )

        ax.set_xlim(-12, 12)
        ax.set_xticks((np.arange(13) * 2 - 12))
        ax.set_ylim(0, 90)

        ax.set_ylabel("Altitude [deg]")
        ax.set_xlabel("Hours from program time")
        ax.grid(visible=True)
        figure.colorbar(mappable).set_label("Azimuth [deg]")

        canvas.setWindowTitle(title_2)
        canvas.setWindowIcon(QIcon('retrhogo.png'))
        canvas.show();
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError):
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return
    except (exceptions.LargeQueryWarning, ReadTimeout, TimeoutError, IERSWarning):
        setters.set_default(self, tab, "Request timed out, please try again.")
        return
    except:
        e = sys.exc_info()[0]
        print(e)
