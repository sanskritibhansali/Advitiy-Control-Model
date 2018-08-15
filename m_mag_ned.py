import numpy as np
import datetime
from pyigrf12 import runigrf12
import constants_1U as con1U

lla = np.genfromtxt('LLA.csv', delimiter=",")
N = lla.shape[0]
m_mag_ned = np.zeros((N,5))
z1 = 0
z2 = 1
for i in range(N):    
    print(i)
    lat = lla[i, 1]       
    lon = lla[i, 2]
    height = lla[i, 3] * 0.001
    elapsed_t = lla[i, 0]
    e_t = datetime.timedelta(seconds = elapsed_t)
    dt = con1U.EPOCH + e_t      #can make a func for this
    #day1 = getattr(dt, 'day')
    #parameters = [day1, z1, z2, height, lat, lon]
    B = runigrf12(dt, z1, z2, height, lat, lon)
    m_mag_ned[i,0]=lla[i, 0]
    m_mag_ned[i,1:5]=B
np.savetxt('mag_output_ned.csv',m_mag_ned, delimiter=",") 
print ("NED frame magnetic field in nano-tesla")
