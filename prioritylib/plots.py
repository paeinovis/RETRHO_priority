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
        title = "Finder image for " + tab.current_target_name + " (FOV = " + str(self.fov) + ")"
        title_2 = tab.current_target_name + " Finder Plot"
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    ax, hdu = plot_finder_image(tab.coords, fov_radius=self.fov);
    wcs = WCS(hdu.header)
    ax.set_title(title)
    figure.add_subplot(ax, projection=wcs)
    canvas.setWindowTitle(title_2)
    canvas.show();

# Plot finder image based on name    
def plot(self, tab):
    if not helpers.update(self, tab):          
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return  
                
    try: 
        result_table = Simbad.query_object(tab.current_target_name)[["main_id", "ra", "dec", "V"]]
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError):
        setters.set_default(self, tab, "Object not found. Check spelling or upload file and try again.")
        return
    
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    ax, hdu = plot_finder_image(tab.current_target, fov_radius=self.fov);
    wcs = WCS(hdu.header)
    title = "Finder image for " + tab.current_target_name + " (FOV = " + str(self.fov) + ")"
    ax.set_title(title)
    figure.add_subplot(ax, projection=wcs)
    title = tab.current_target_name + " Finder Plot"
    canvas.setWindowTitle(title)
    canvas.show()

# Plot airmass based on target
def airmass_plot(self, tab):        
    if tab is self.tab3:
        title = "Airmass plot from coordinates"
        title_2 = "Plot From Coordinates"
    elif not helpers.update(self, tab):          
        setters.set_default(self, tab)
        return  
    else:
        title = "Airmass plot for " + tab.current_target_name + " (FOV = " + str(self.fov) + ")"
        title_2 = tab.current_target_name + " Airmass Plot"

    if self.use_curr_time:
        self.time_var = Time.now()                                # Update time If needed

    figure = plt.figure(figsize=(8, 6))
    ax = plot_airmass(tab.current_target, 
                        observer=RHO, 
                        time=self.time_var.to_datetime(timezone=RHO.timezone), 
                        use_local_tz=True,
                        brightness_shading=True)
    ax.set_title(title)
    figure.add_subplot(ax)
    canvas = FigureCanvas(figure)
    canvas.setWindowTitle(title_2)
    canvas.show();
