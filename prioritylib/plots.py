from lib import *
import prioritylib.helpers as helpers
from prioritylib.global_ import *

# Plot finder image based on coordinates
def plot_coords(self, tab):
    if tab is self.tab3:
        title = "Finder image from coordinates (FOV = " + str(self.fov) + ")"
        title_2 = "Plot From Coordinates"
    elif tab is self.tab2:
        name = tab.targets_dropdown.currentText()
        if name == '':
            tab.label_info.setText("Could not complete action. Ensure a target is uploaded and selected.")
            return False
        helpers.update(self, tab)
        title = "Finder image for " + tab.current_target_name + " (FOV = " + str(self.fov) + ")"
        title_2 = tab.current_target_name + " Plot"
    now = Time.now()
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    ax, hdu = plot_finder_image(tab.coords, fov_radius=self.fov);
    wcs = WCS(hdu.header)
    ax.set_title(title)
    figure.add_subplot(ax, projection=wcs)
    canvas.setWindowTitle(title_2)
    canvas.show();

# Plot finder image    
def plot(self, tab):
    if tab.target_names is not None:
        if not helpers.update(self, tab):
            return
            
    try: 
        result_table = Simbad.query_object(tab.current_target_name)[["main_id", "ra", "dec", "V"]]
    except (NoResultsWarning, NameResolveError, DALFormatError, DALAccessError, DALServiceError, DALQueryError):
        tab.label_info.setText("Object not found. Check spelling and try again.")
        return
    
    now = Time.now()
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    ax, hdu = plot_finder_image(tab.current_target, fov_radius=self.fov);
    wcs = WCS(hdu.header)
    title = "Finder image for " + tab.current_target_name + " (FOV = " + str(self.fov) + ")"
    ax.set_title(title)
    figure.add_subplot(ax, projection=wcs)
    title = tab.current_target_name + " Plot"
    canvas.setWindowTitle(title)
    canvas.show();


# Plot airmass
def airmass_plot(tab):        
    now = Time.now()
    figure = plt.figure(figsize=(8, 6))
    ax = plot_airmass(tab.current_target, 
                        observer=RHO, 
                        time=now.to_datetime(timezone=RHO.timezone), 
                        use_local_tz=True,
                        brightness_shading=True)
    title = "Airmass plot for " + tab.current_target_name
    ax.set_title(title)
    figure.add_subplot(ax)
    title = tab.current_target_name + " Airmass Plot"
    canvas = FigureCanvas(figure)
    canvas.setWindowTitle(title)
    canvas.show();
