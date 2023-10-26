import sys
import random
import argparse
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import cartopy.crs as ccrs
from skyfield.api import load
from skyfield.api import wgs84
import matplotlib.pyplot as plt


class StarlinkTracker:
    """ 
    Simple Starlink tracker and trajectory estimator.
        - The -t argument specifies the number of minutes for which to predict the track for.
        - Press the 'a' key to regenerate a new, random Starlink trajectory. 
        - Press the 'esc' key to exit.
    """

    def __init__(self, arg):
        self.minutes = arg
        self.url = 'https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=starlink&FORMAT=tle'
        self.sats = load.tle_file(self.url)
        self.ts = load.timescale()
        self.sat_idx = self.pick_starlink()
        self.coords = self.generate_track()


    def pick_starlink(self):
        """
        Returns an index for a random Starlink.
        """
        return random.randint(0, len(self.sats)) 


    def predict_track(self):
        """
        Predicts the trajectory of a random Starlink for a given number of hours.
        Returns the geodetic coordinates.
        """
        now = self.ts.now()
        dates = self.ts.utc(now.utc[0], now.utc[1], now.utc[2], now.utc[3], range(self.minutes)) 
        
        lats = []
        lons = []
        for t in dates:
            geocentric = self.sats[self.sat_idx].at(t)  
            lat, lon = wgs84.latlon_of(geocentric) # Geodetic latitude and longitude
            lats.append(lat.degrees)
            lons.append(lon.degrees)
        return lons, lats


    def generate_track(self):
        """
        Calls predict_track() function.
        """
        return self.predict_track()


    def plot_track(self, coords):
        """
        Plots the Starlink track on a 2D image of the globe.
        """
        plt.figure(figsize=[10,5])
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        starlink = self.sats[self.sat_idx].name
        ax.plot(coords[0], coords[1], zorder=1, c='k', transform=ccrs.Geodetic(), label=starlink)
        plt.scatter(coords[0][0], coords[1][0], zorder=2, c='g', label='Current position')
        plt.scatter(coords[0][-1], coords[1][-1], zorder=2, c='r', label=f'Position after {self.minutes} minutes')
        plt.legend()
        plt.gcf().canvas.mpl_connect('key_press_event', self.on_key) #binding key event to the plot
        plt.show()


    def on_key(self, event):
        if event.key == 'escape':
            sys.exit()
        elif event.key == 'a':
            # Regenerate the track and update the plot
            self.sat_idx = self.pick_starlink()
            self.coords = self.generate_track()
            plt.close()
            self.plot_track(self.coords)


def main():
    parser = argparse.ArgumentParser(description="Starlink Tracker")
    parser.add_argument("-t", "--minutes", type=int, default=60, help="Number of minutes for trajectory estimation")
    args = parser.parse_args()

    app = QApplication([])
    tracker = StarlinkTracker(args.minutes)
    tracker.plot_track(tracker.coords)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()