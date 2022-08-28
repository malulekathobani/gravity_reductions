""" Name    : Thobani
    Surname : Maluleka
    Empl Id : MLLTHO015
    Course  : APG4005F
    Date    : Fri Aug 26 02:08:22 2022
"""

"""The python script to compute gravity station terrain correction"""
import Functions as fn
import pandas as pd
from math import sin, cos, acos, radians
from scipy.integrate import dblquad

n=len(fn.data.gravity_data())
lst=list(range(n+1))  
lst.remove(0)  
trc=dict(zip(lst , [0] * n))

dataset=fn.data.fishnet_grid_data()

def geodesic_dist(lat, long, latr, longr):
    R=6.371E6    
    _A = acos( ( sin(lat) * sin(latr) ) + ( cos(lat) * cos(latr) * cos(longr - long)) )
    return 2 * R * sin(_A / 2)

def trc_correction(lat, long, Zp, latr, longr, Zqr):
    R=6371008.7714 #mean earth radius
    lat, long, latr, longr = radians(lat), radians(long), radians(latr), radians(longr)
    
    _A = acos( ( sin(lat) * sin(latr) ) + ( cos(lat) * cos(latr) * cos(longr - long)) )
    geodesic_distance = 2 * R * sin(_A / 2)
    
    contt=(0.017820381 * (6.371E6)**2)/2
    mth=( ((Zp - Zqr)**2) / geodesic_distance**3) * (cos(lat))
    area = dblquad(lambda x, y: mth, lat, latr, lambda x: long, lambda x: longr)
    return contt * area[0]

for i in dataset.itertuples():
    lank=i.rank
    idd=i.gravity_station_ID
    lat=i.gravity_station_latitude
    long=i.gravity_station_longitude
    Zp=i.gravity_station_srtm

    latr=i.grid_point_latitude
    longr=i.grid_point_longitude
    Zqr=i.grid_point_srtm
    
    if lank>1 and lank<=25:
        trc[idd]+=trc_correction(lat, long, Zp, latr, longr, Zqr)
        
    else:
        ""
        
nn=trc.items()
corrections={"gsID":[], "TC":[]}
for i in nn:
    corrections["gsID"].append(i[0])
    corrections["TC"].append(i[1])
       
terraincorrections=pd.DataFrame(corrections)

