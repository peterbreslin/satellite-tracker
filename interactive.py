import random
import cartopy.crs as ccrs
from skyfield.api import load
from skyfield.api import wgs84
import matplotlib.pyplot as plt 

url = 'https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=starlink&FORMAT=tle'



def skyfield_geodesic_latlon(static=True):

    sats = load.tle_file(url)
    if  static:
        print('Loaded', len(sats), 'Starlink satellites')
    
    t = load.timescale().now()
    lats = []
    lons = []
    for sat in sats:
        geocentric = sat.at(t)  
        lat, lon = wgs84.latlon_of(geocentric) # Geodetic latitude and longitude
        lats.append(lat.degrees)
        lons.append(lon.degrees)
    
    return lons, lats
    
    
    
def starlink_positions(animation=False, runtime=10):

    fig = plt.figure(figsize=[10,15])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax.stock_img()
    plt.ion()    
    
    lons, lats = skyfield_geodesic_latlon()
    ax.scatter(lons, lats, color='k', marker='.', s=1, transform=ccrs.Geodetic())
    
    if animation:
        from IPython.display import display, clear_output
        for i in range(runtime):
            ax.cla()
            ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
            ax.stock_img()
            lons, lats = skyfield_geodesic_latlon(static=False)
            ax.scatter(lons, lats, color='k', marker='.', s=1, transform=ccrs.Geodetic())
            display(fig)
            clear_output(wait=True)
        
    plt.show()
    
    
    
def predict_track(mins=90, n=1):

    plt.figure(figsize=[10,15])
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    
    sats = load.tle_file(url)
    ts = load.timescale()
    now = ts.now()
    dates = ts.utc(now.utc[0], now.utc[1], now.utc[2], now.utc[3], range(mins)) 
    
    for i in range(n):
        sat = random.randint(0, len(sats))
        sats.remove(sats[sat])
        lats = []
        lons = []
        for time in dates:
            geocentric = sats[sat].at(time)  
            lat, lon = wgs84.latlon_of(geocentric) # Geodetic latitude and longitude
            lats.append(lat.degrees)
            lons.append(lon.degrees)

        plt.plot(lons, lats, c='k', zorder=0, transform=ccrs.Geodetic(), lw=1)
        plt.scatter(lons[0], lats[0], c='C{}'.format(i), s=20, zorder=1, label=sats[sat].name)
        ax.legend(bbox_to_anchor=(1.0, 1.0))
        
    plt.show()
    
    
    
choice = int(input('Enter 1 to plot Starlink locations \nEnter 2 to plot them with time \nEnter 3 to plot a random track(s)\nAnswer: '))

if choice==1:
    starlink_positions()
    
elif choice==2:
    n = int(input('For how long? (seconds): '))
    starlink_positions(animation=True, runtime=n)
    
elif choice==3:
    
    while True:
        n = int(input('For how many satellites? '))
        
        if (n > 500) | (n == 0):
            print("That many won't look too great.. try again! ")
        else:
            break
        
    timerange = int(input("How many minutes would you like to predict(s) the track for? "))
    predict_track(mins=timerange, n=n)
    

    



















