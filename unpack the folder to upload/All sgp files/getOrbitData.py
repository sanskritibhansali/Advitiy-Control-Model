import numpy as np
import constants_1U as C1U
import sgp 
import TLE2OrbitElements as TOE


def filename(TT,MS,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg,sgp_output):
    os.chdir('data_files/')
    fname_load = "sgp_i_TT%g_MS%g_MMo%g_Ecc%g_Incl%g_MAnamoly%g_ArgP%g_Raan%g.csv"%(TT,MS,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg)	#load from this file
    
    try:
    	a_file = open(fname_load, 'rb')
    	my_input = a_file
    	a_file.close
    	loaded = True
    	print 'File found: ' + fname_load
    except IOError as e:	#if file doesnot exist already it sets flag and calculates it so you don't have to manually check
    	loaded = False
    	print('No existing file could be opened.')
    
    if loaded == False:
    	my_input = sgp_output
     	np.savetxt(fname_load,my_input, delimiter=",")
    '''
    	print "calculated new file using function"
    
     #fname_save = "sgp_Twice_i_tf%g_dt%g_RA%g_in%g_per%g.csv"%(tf,dt,RAAN,Inclinatoin,ArgPer) #save in this file
    fname_save = "sgp_Twice_i_TT%g_MS%g_MMo%g_Ecc%g_Incl%g_MAnamoly%g_ArgP%g_Raan%g.csv"%(TT,MS,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg)  #save in this file

    my_input = np.genfromtxt(fname_load, delimiter=",")
    #do something and get new variable
    result = 2*my_input
    
    np.savetxt(fname_save,result, delimiter=",")
    print 'saved results ' + fname_save
   '''

def getOrbitData_TLE():
    line1 = C1U.LINE1
    line2 = C1U.LINE2
    MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg,DMeanMotion,DDMeanMotion,BStar = TOE.TLE2OE(line1,line2)
    
    dT = C1U.dT ## dT is in seconds. total 100 minutes here. 10 is for 1/timestep
    TT = C1U.TT ## total time in minutes (used in filename)
    MS = C1U.MODEL_STEP
    sgp_output = np.zeros([N,7])
    sgp_output = np.zeros([ len(dT),7], dtype = 'float')
    sgp_output[:,0],sgp_output[:,1:4],sgp_output[:,4:7] = sgp.sgp_fn(dT,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg,DMeanMotion,DDMeanMotion,BStar)
    
    filename(TT,MS,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg,sgp_output)

    #np.savetxt("sgp_output_c.csv", sgp_output, delimiter=",") #Saves sgp_output to csv file

def getOrbitData_OrbitELement():
    MeanMo = C1U.MeanMo 
    Eccen = C1U.Eccen 
    Incl_deg  = C1U.Incl_deg
    MeanAnamoly_deg = C1U.MeanAnamoly_deg
    ArgP =C1U.ArgP 
    RAAN_deg = C1U.RAAN_deg
    DMeanMotion = C1U.DMeanMotion
    DDMeanMotion = C1U.DDMeanMotion
    BStar = C1U.BStar
    
    dT = C1U.dT ## dT is in seconds. total 100 minutes here. 10 is for 1/timestep
    TT = C1U.TT ## total time in minutes (used in filename)
    MS = C1U.MODEL_STEP
    sgp_output = np.zeros([N,7])
    sgp_output = np.zeros([ len(dT),8], dtype = 'float') #7 to 8 for eccentricity calculation
    sgp_output[:,0],sgp_output[:,1:4],sgp_output[:,4:7] = sgp.sgp_fn(dT,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg,DMeanMotion,DDMeanMotion,BStar)
    
    filename(TT,MS,MeanMo,Eccen,Incl_deg,MeanAnamoly_deg,ArgP,RAAN_deg,sgp_output)

    #np.savetxt("sgp_output_b.csv", sgp_output, delimiter=",") #Saves sgp_output to csv file

### Call getOrbitData_TLE or getOrbitData_OrbitELement
# Uncomment whichever is required
#getOrbitData_TLE()
getOrbitData_OrbitELement()