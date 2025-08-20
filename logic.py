import csv
import os
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u

def calculate_radec(dt, lat, lon, ele, alti, azi):
    
    observer_location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=ele*u.meter)
    observation_time = Time(dt, scale='utc')
    celestial_object = SkyCoord(alt=alti*u.deg, az=azi*u.deg, frame='altaz', obstime=observation_time, location=observer_location).icrs

    ra = celestial_object.ra.deg
    dec = celestial_object.dec.deg

    return ra, dec

def save_to_csv(data, filename):
    header = ["Date", "Time", "Latitude (deg)", "Longitude (deg)", "Elevation (m)", 
              "Altitude (deg)", "Azimuth (deg)", "RA (deg)", "DEC (deg)"]

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(data)