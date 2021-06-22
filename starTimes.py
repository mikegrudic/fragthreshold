#!/usr/bin/env python
# coding: utf-8

# In[5]:


import h5py
from glob import glob
import numpy as np
from os.path import isdir
import load_from_snapshot
from os import system, mkdir, chdir

sims_dir = "/scratch1/08056/hlane17/fragset2/mach8_alpha8_mu4_sol1_Res101/"

# initialize lists to store all the stuff we will want in the final data file

for j in range(1, 15):
    Mass_star = []
    Time_list = []
    print(j)
    location = sims_dir + "mach8_alpha8_mu4_sol1_Res101"+ "_" + str(j) + "/output/"
    chdir(location)
    for i in range(102):
        ext='00'+str(i);
        if (i>=10): ext='0'+str(i)                                     #This resolves naming issues
        if (i>=100): ext=str(i)
        current_snap = "snapshot_" + str(ext) + ".hdf5" # get the last snapshot
    
    
        print("snap_" + str(i))
        f = h5py.File(current_snap, "r")  #opens file
        try:
            mstar = np.sum(f["PartType5"]["Masses"])
        except:
            mstar = 0
        Mass_star.append(mstar)
        time = load_from_snapshot.load_from_snapshot("Time",0,location,i)
        Time_list.append(time)
        f.close()
    chdir("../../")    
    np.savetxt("starTime" + str(j) + ".dat", np.c_[Time_list, Mass_star], 
               header = "#(0) infall mach (1) alpha (2) mu (3) solenoidal fractino (4) Ngas (5) seed (6) SFE (7) Nstars (8) > 10% mass frac (9) max mass frac (10) M2_frac (11) first star time"
    )
    

# In[ ]:




