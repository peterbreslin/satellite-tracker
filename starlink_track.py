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



def predict_track(hrs):

    sats = load.tle_file(url)
    sat = random.randint(0, len(sats)) # pick random satellite
    
    ts = load.timescale()
    now = ts.now()
    dates = ts.utc(now.utc[0], now.utc[1], now.utc[2], now.utc[3], range(hrs)) 
    
    lats = []
    lons = []
    for t in dates:
        geocentric = sats[sat].at(t)  
        lat, lon = wgs84.latlon_of(geocentric) # Geodetic latitude and longitude
        lats.append(lat.degrees)
        lons.append(lon.degrees)
    
    plt.figure(figsize=[10,15])
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.plot(lons, lats, color='k', transform=ccrs.Geodetic())
    plt.show()



predict_track(50)