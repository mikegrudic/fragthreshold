#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import h5py
from glob import glob
import numpy as np
from os.path import isdir
import load_from_snapshot

sims_dir = "/scratch1/08056/hlane17/fragset2/"

# initialize lists to store all the stuff we will want in the final data file
SFEs = [] # star formation efficiency: mstar / (mstar + mgas)
tenpercent_frac = [] # fraction of stellar mass in stars > 10% the total stellar mass
Mmax_frac = [] # mass fraction of the most massive thing
M2_frac = [] # mass fraction of second-most massive thing
infall_machs = []
alphas = []
sol_fracs = []
seeds = []
mus = []
Ngas = []
Nstars = []
firstStarTime = []

for dir in glob(sims_dir+"mach*alpha*/mach*alpha*/output"):    # get the run parameters from the directory name
    infall_machs.append(float(dir.split("mach")[1].split("_")[0])) # infall mach 
    alphas.append(float(dir.split("alpha")[1].split("_")[0])) # virial parameter
    mus.append(float(dir.split("mu")[1].split("_")[0])) # mass-to-flux ratio mu
    sol_fracs.append(float(dir.split("sol")[1].split("_")[0])) # solenoidal fraction 
    seeds.append(float(dir.split("_")[-1].split("/")[0])) # random seed
    Ngas.append(float(dir.split("Res")[1].split("_")[0])**3) # number of gas cells initially
    
    last_snap = sorted(glob(dir+"/snapshot*.hdf5"))[-1] # get the last snapshot
    
    F = h5py.File(last_snap, 'r') # open the snapshot
    if not "PartType5" in F.keys():  # get the stellar masses - if there are no PartType5 for some reason then we just create an empty array
        mstar = np.array([])
    else:
        mstar = np.array(F["PartType5"]["Masses"])
    
    mgas = np.array(F["PartType0"]["Masses"])
    
    SFEs.append(mstar.sum()/(mstar.sum() + mgas.sum()))
    tenpercent_frac.append(np.sum(mstar[mstar > 0.1*mstar.sum()]))
    Nstars.append(len(mstar))

    if not "PartType5" in F.keys():  # get the stellar masses - if there are no PartType5 for some reason then we just create an empty array
        time = np.nan
        firstSTarTime.append(time)
        print("no star")
    else:
        for i in range(101):
            ext='00'+str(i);
            if (i>=10): ext='0'+str(i)                                     #This resolves naming issues
            if (i>=100): ext=str(i)
            current_snap = sorted(glob(dir+"/snapshot*.hdf5"))[i] # get the last snapshot
            print("snap_" + str(i))
            f = h5py.File(current_snap, "r")  #opens file
            try:
                mstar2 = np.array(f["PartType5"]["Masses"])
            except:
                mstar2 = 0
            if(mstar2.sum() > 0):
                time = load_from_snapshot.load_from_snapshot("Time",0,dir,i)
                firstStarTime.append(time)
                print (mstar.sum())
                print("Star found, breaking")
                break
            else:
                pass
            f.close()
            F.close()
        
    if mstar.sum() > 0: Mmax_frac.append(mstar.max() / mstar.sum()) 
    else: Mmax_frac.append(np.nan) # handle the empty case where max 
    if len(mstar) > 1: M2_frac.append(np.sort(mstar)[-2] / mstar.sum()) # mass fraction of second-most massive star
    else: M2_frac.append(np.nan)

np.savetxt("SimulationDataTime.dat", np.c_[infall_machs, alphas, mus, sol_fracs, Ngas, seeds, SFEs, Nstars, tenpercent_frac, Mmax_frac, M2_frac, firstStarTime], 
           header = "#(0) infall mach (1) alpha (2) mu (3) solenoidal fractino (4) Ngas (5) seed (6) SFE (7) Nstars (8) > 10% mass frac (9) max mass frac (10) M2_frac (11) first star time"
)

