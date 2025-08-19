import csv
from datetime import datetime 
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u


def get_input():
    date_str = input("Enter Date (YYYY-MM-DD): ")
    time_str = input("Enter Time (HH:MM:SS): ")
    latitude = float(input("Enter Latitude in Degrees: "))
    longitude = float(input("Enter Longitude in Degrees: "))
    elevation = float(input("Enter Elevation in Meters: ")) # Height above sea level
    altitude = float(input("Enter Altitude in Degrees: ")) # Angle from horizon
    azimuth = float(input("Enter Azimuth in Degrees: ")) # Direction along horizon (True North) 

    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    
    return dt, latitude, longitude, elevation, altitude, azimuth

def calculate_radec(dt, lat, lon, ele, alti, azi):
    
    observer_location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=ele*u.meter)
    observation_time = Time(dt, scale='utc')
    celestial_object = SkyCoord(alt=alti*u.deg, az=azi*u.deg, frame='altaz', obstime=observation_time, location=observer_location).icrs

    ra = celestial_object.ra.deg
    dec = celestial_object.dec.deg

    return ra, dec

def save_to_csv(data, filename='log.csv'):
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['Date (yyyy-mm-dd)', 'Time', 'Latitude (degrees)', 'Longitude(degrees)', 'Elevation (meters)', 'Altitude (degrees)', 'Azimuth(degrees)', 'RA (degrees)', 'Dec (degrees)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            writer.writerow(row)

def main():
    now = datetime.now()

    all_data = []
    print(f"Current Date and Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    while True:
        dt, latitude, longitude, elevation, altitude, azimuth = get_input()
        ra, dec = calculate_radec(dt, latitude, longitude, elevation, altitude, azimuth)

        all_data.append({
            'Date (yyyy-mm-dd)': dt.strftime('%Y-%m-%d'),
            'Time': dt.strftime('%H:%M:%S'),
            'Latitude (degrees)': latitude,
            'Longitude(degrees)': longitude,
            'Elevation (meters)': elevation,
            'Altitude (degrees)': altitude,
            'Azimuth(degrees)': azimuth,
            'RA (degrees)': ra,
            'Dec (degrees)': dec
        })

        cont = input("Add another? (y/n): ").lower()

        if(cont != "y"):
            break

    save_to_csv(all_data)
    print("CSV saved!")

if __name__ == "__main__":
    main()
