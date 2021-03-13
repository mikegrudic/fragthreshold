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


# In[19]:


#location = "/home/hlane/project1Sims/"
location = "/work/08056/hlane17/frontera/fragthreshold"
#This program is intended to be run in the directory that contains a collection of simulations.
chdir(location)
G = 4300.7 # gravitational constant in m/s - msun - pc units
cs = 200 # isothermal sound speed in m/s (= pressure/density, appropriate for ISM at ~10K)
sigma = 1e3 # surface density M/(pi R^2) in msun pc^-2 (this is arbitrary, just to set the dimensions of our problem - 1000 roughly corresponds to observed cores)

infall_machs = 1.41, 1#np.logspace(0,3,7,base=2) # the list of infall mach #'s we want - ranges from 1 to 8, evenly spaced in log space (each is a certain % larger than the last, in a geometric progression)
alphas = 0, 0.5, 1, 2, 4, 8 #list of turbulent virial parameters we want - 0 is no initial turbulence
mus = 4, #np.inf, 4, 2, 1, 0.5, 0.25  # list of mass-to-flux ratios (greek letter mu) that we want - infinity is no magnetic field, ~0 is very strong magnetic field
seeds = 42, #42, 2, 3 # different initial turbulent seed fields - so that we try a few different random samplings of the initial turbulence to make sure results are not a fluke
sol_fracs = 0.5,  # 0, 1 # fraction of turbulent field in solenoidal modes 
if not isdir("allPickle"): mkdir("allPickle") # if the directory for the run does not exist, create it
dict = {}
MachDict = {}
tenPercentFractionDict = {}


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
                    tenPercentList = []
                    mStarList = []
                    d=location + run_name + "/output"
                    numFiles = 0
                    for path in os.listdir(d):
                        if os.path.isfile(os.path.join(d, path)):
                            numFiles += 1
                    system("pwd")
                    print(numFiles)
                    numTot = numFiles-5
                    for i in range(numTot,numTot+1): 
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
                            mStarList.append(mStar)
                        except: 
                            mStar = 0               #If there are no stars, the mass is zero.
                            mStarList.append(mStar)
                            print(mStarList)
                        for u in mStarList:
                            if (10*u > mgasInit):
                                tenPercentList.append(u)
                            else:
                                noValue = 0
                                tenPercentList.append(noValue)
                        tenPercentFraction.append(len(tenPercentList)/len(mStarList))
                        MachList.append(infall_mach)

                    dict[run_name] = [tenPercentFractionDict, MachDict, numTot]
                    chdir("../") # go back to the top level directory
                    chdir("allPickle") #switch to pickle directory
                    F = open(run_name + '.pickle','wb')
                    pickle.dump(dict[run_name], F)
                    F.close()
                    chdir("../") #go back to the top level directory


# In[ ]:


#import os package to use file related methods
import os
#initialization of file count.
Number_Of_Files=0
#path name variablle .
run_name = "mach1.41_alpha0.5_mu4_sol0.5_Res22_42"
d="/home/hlane/project1Sims/" + run_name + "/output"
#os.walk () method is used for travel throught the fle .
for files in os.walk(path):
    for files in path:
        Number_Of_Files=Number_Of_Files+1
print("Total files  = ",Number_Of_Files)


# In[ ]:


import os
numFiles = 0
d="/work/08056/hlane17/frontera/fragthreshold" + run_name + "/output"
for path in os.listdir(d):
    if os.path.isfile(os.path.join(d, path)):
        numFiles += 1
print(count)


# In[7]:


chdir("/home/hlane/project1Sims/allPickle")

infall_machs = np.logspace(0,3,7,base=2) # the list of infall mach #'s we want - ranges from 1 to 8, evenly spaced in log space (each is a certain % larger than the last, in a geometric progression)
alphas = 0, 0.5, 1, 2, 4, 8 #list of turbulent virial parameters we want - 0 is no initial turbulence
mus = 4, #np.inf, 4, 2, 1, 0.5, 0.25  # list of mass-to-flux ratios (greek letter mu) that we want - infinity is no magnetic field, ~0 is very strong magnetic field
seeds = 42, #42, 2, 3 # different initial turbulent seed fields - so that we try a few different random samplings of the initial turbulence to make sure results are not a fluke
sol_fracs = 0.5,  # 0, 1 # fraction of turbulent field in solenoidal modes 

for infall_mach in infall_machs:
    for alpha in alphas:
        for mu in mus:
            for seed in seeds:                
                for sol_frac in sol_fracs:
                    Ngas = max(100 * infall_mach**4, 10000)
                    run_name = "mach%g_alpha%g_mu%g_sol%g_Res%d_%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), sol_frac, round(Ngas**(1./3)), seed) # this will be the unique identifier for the run - will want to create a new directory with this name
                    F=open(run_name + '.pickle', "rb")
                    temp = pickle.load(F)
                    tenPercentFractionDict = temp[0]
                    MachDict = temp[1]
                    numTot = temp[2]

                    for i in range(numTot,numTot+1):
                        plt.scatter(MachDict[run_name][i],tenPercentFractionDict[run_name][i])
                    F.close()
plt.xlabel("Infall Mach Number " + r"($ℳ_{\rm infall}\rm$)")
plt.ylabel("Fraction of mass in large fragments (" + r"$M_{\rm Sink}\, \rm > 0.1M_{\rm cloud}$)")
plt.show()


# In[ ]:




