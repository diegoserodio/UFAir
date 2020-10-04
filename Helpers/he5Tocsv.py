import numpy as np
import sys
import h5py
import csv
from datetime import datetime
from pyhdf.SD import SD, SDC

filepath = './../Data/AIRS.2020.01.11.L3.RetStd_IR001.v7.0.3.0.G20120100333.hdf'

#Loads the .he5 file
file = h5py.File(filepath,'r')

#Extracting timestamp, latitude, longitude and desired data
data = file.get('HDFEOS').get('SWATHS').get('ColumnAmountNO2').get('Data Fields').get('ColumnAmountNO2')
geolocation = file.get('HDFEOS').get('SWATHS').get('ColumnAmountNO2').get('Geolocation Fields')
latitude = np.array(geolocation.get('Latitude'))
longitude = np.array(geolocation.get('Longitude'))
timestamp = np.array(geolocation.get('Time'))

#Generating .csv file
headers = ["Time", "Latitude", "Longitude", "NO2"]
with open('ColumnAmountNO2_04_01.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for i in range(60):
        for j in range(len(data[i])):
            date = datetime.fromtimestamp(timestamp[i])
            date = str(date).replace("1997", "2020")
            writer.writerow([date, latitude[i][j], longitude[i][j], data[i][j]])
