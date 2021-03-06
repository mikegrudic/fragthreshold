#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import h5py
from matplotlib import pyplot as plt
import pickle
import os
from os import system, mkdir, chdir
from glob import glob
from os.path import isdir
import numpy as np


# In[12]:


#location = "/home/hlane/project1Sims/"
location = "/scratch1/08056/hlane17/frontera/fragthreshold/"
#This program is intended to be run in the directory that contains a collection of simulations.
chdir(location)
G = 4300.7 # gravitational constant in m/s - msun - pc units
cs = 200 # isothermal sound speed in m/s (= pressure/density, appropriate for ISM at ~10K)
sigma = 1e3 # surface density M/(pi R^2) in msun pc^-2 (this is arbitrary, just to set the dimensions of our problem - 1000 roughly corresponds to observed cores)

infall_machs = np.logspace(0,3,7,base=2) # the list of infall mach #'s we want - ranges from 1 to 8, evenly spaced in log space (each is a certain % larger than the last, in a geometric progression)
alphas = 0.25, 0.5, 1, 2, 4, 8 #list of turbulent virial parameters we want - 0 is no initial turbulence
mus = 4, 2, 1, 0.5 #np.inf, 4, 2, 1, 0.5, 0.25  # list of mass-to-flux ratios (greek letter mu) that we want - infinity is no magnetic field, ~0 is very strong magnetic field
seeds = 42, #42, 2, 3 # different initial turbulent seed fields - so that we try a few different random samplings of the initial turbulence to make sure results are not a fluke
sol_fracs = 0.5,  # 0, 1 # fraction of turbulent field in solenoidal modes 
if not isdir("allPickle"): mkdir("allPickle") # if the directory for the run does not exist, create it
dict = {}
AlphaDict = {}
tenPercentMass = {}
mStarTotalDict = {}

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
                    
                    mCloudInit = np.sum(np.array(F["PartType0"]["Masses"])[ids]) #MassGas in snapshot 1
    
                    dict = {}
                    tenPercentMass[run_name] = {}
                    mStarTotalDict[run_name] = {}
                    tenPercentList = []
                    massStars = []
                    d=location + run_name + "/output"
                    numFiles = 0
                    for path in os.listdir(d):
                        if os.path.isfile(os.path.join(d, path)):
                            numFiles += 1
                    system("pwd")
                    print(numFiles)
                    numTot = numFiles-5
                    for i in range(numTot,numTot+1): 
                        tenPercentList = []
                        starList = []
                        
                        ext='00'+str(i);
                        if (i>=10): ext='0'+str(i) #This resolves naming issues
                        if (i>=100): ext=str(i)
                        f = h5py.File("output/snapshot_" + ext + ".hdf5", "r")  #opens file
                        try:
                            mStar = np.array(f["PartType5"]["Masses"])     #reads file
                            starList.append(mStar)
                        except:
                            mStar = []
                            
                            #mStar = np.array([0])               #If there are no stars, the mass is zero.
                            #starList.append(mStar)
                        for u in mStar:
                            if (10*u > np.sum(starList)):
                                tenPercentList.append(u)
                        mStarTotalDict[run_name][i] = starList
                        
                        tenPercentMass[run_name][i] = tenPercentList
                        
                    print("Creating pickle dictionaries")
                    dict[run_name] = [tenPercentMass, mStarTotalDict, numTot, mCloudInit]
                    chdir("../") # go back to the top level directory
                    chdir("allPickle") #switch to pickle directory
                    print("Switched to allPickle")
                    F = open(run_name + '.pickle','wb')
                    pickle.dump(dict[run_name], F)
                    print("Dumped Pickle")
                    F.close()
                    chdir("../") #go back to the top level directory


# In[ ]:




