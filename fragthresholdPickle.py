#!/usr/bin/env python
# coding: utf-8

# In[59]:


import numpy as np
import load_from_snapshot
import h5py
from matplotlib import pyplot as plt
import pickle
from os import system, mkdir, chdir
from glob import glob
from os.path import isdir
import numpy as np


# In[62]:


#This program is intended to be run in the directory that contains a collection of simulations.
for infall_mach in infall_machs:
    for alpha in alphas:
        for mu in mus:
            for seed in seeds:                
                for sol_frac in sol_fracs:
                    Ngas = max(100 * infall_mach**4, 10000)
                    run_name = "mach%g_alpha%g_mu%g_sol%g_Res%d_%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), sol_frac, round(Ngas**(1./3)), seed) # this will be the unique identifier for the run - will want to create a new directory with this name
                    chdir(run_name)
                    F = h5py.File("output/snapshot_000.hdf5", "r")
                    ids = np.array(F["PartType0"]["ParticleIDs"])
                    gas_we_care_about = (ids<=Ngas)
                    ids = ids[gas_we_care_about]
                    
                    mgasInit = np.sum(np.array(F["PartType0"]["Masses"])[ids]) #MassGas in snapshot 1
    
                    dict[run_name] = {}
                    MachDict[run_name] = {}
                    tenPercentFractionDict[run_name] = {}
                    MachList = []
                    num = ls -1 | wc -l
                    for i in range(num-6,num-5): 
                        system("pwd")
                        tenPercentFraction = []
                        tenPercentList = []
                        MachDict[run_name][i] = MachList
                        tenPercentFractionDict[run_name][i] = tenPercentList

                        ext='00'+str(i);
                        if (i>=10): ext='0'+str(i) #This resolves naming issues
                        if (i>=100): ext=str(i)
                        f = h5py.File("output/snapshot_" + ext + ".hdf5", "r")  #opens file
                        try:
                            mStar = np.array(f["PartType5"]["Masses"])     #reads file
                        except: 
                            mStar = np.array([0])                #If there are no stars, the mass is zero.

                        for u in mStar:
                            if (10*u > mgasInit):
                                tenPercentList.append(u)
                            else:
                                noValue = 0
                                tenPercentList.append(noValue)
                        tenPercentFraction.append(len(tenPercentList)/len(mStar))
                        MachList.append(infall_mach)

                    dict[run_name] = [tenPercentFractionDict, MachDict]
                    chdir("../") # go back to the top level directory
                    chdir("allPickle") #switch to pickle directory
                    F = open(run_name + '.pickle','wb')
                    pickle.dump(dict[run_name], F)
                    F.close()
                    chdir("../") #go back to the top level directory


# In[ ]:





# In[ ]:




