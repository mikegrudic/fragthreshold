#!/usr/bin/env python
# coding: utf-8

# In[59]:


import numpy as np
import h5py
from matplotlib import pyplot as plt
import pickle
from os import system, mkdir, chdir
from glob import glob
from os.path import isdir
import numpy as np




#This program is intended to be run in the directory that contains a collection of simulations.
chdir("/home/hlane/project1Sims")
G = 4300.7 # gravitational constant in m/s - msun - pc units
cs = 200 # isothermal sound speed in m/s (= pressure/density, appropriate for ISM at ~10K)
sigma = 1e3 # surface density M/(pi R^2) in msun pc^-2 (this is arbitrary, just to set the dimensions of our problem - 1000 roughly corresponds to observed cores)

infall_machs = np.logspace(0,3,7,base=2) # the list of infall mach #'s we want - ranges from 1 to 8, evenly spaced in log space (each is a certain % larger than the last, in a geometric progression)
alphas = 0, 0.5, 1, 2, 4, 8 #list of turbulent virial parameters we want - 0 is no initial turbulence
mus = 4, #np.inf, 4, 2, 1, 0.5, 0.25  # list of mass-to-flux ratios (greek letter mu) that we want - infinity is no magnetic field, ~0 is very strong magnetic field
seeds = 42, #42, 2, 3 # different initial turbulent seed fields - so that we try a few different random samplings of the initial turbulence to make sure results are not a fluke
sol_fracs = 0.5,  # 0, 1 # fraction of turbulent field in solenoidal modes 
if not isdir("allPickle"): mkdir("allPickle") # if the directory for the run does not exist, create it
dict = {}
MachDict = {}
tenPercentFractionDict = {}


for infall_mach in infall_machs:
    print(infall_mach)
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
                    cpt = sum([len(files) for r, d, files in os.walk("/home/hlane/project1Sims/" + run_name +"output")])
                    system("pwd")
                    print(cpt)
                    for i in range(cpt-6,cpt-5): 
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

