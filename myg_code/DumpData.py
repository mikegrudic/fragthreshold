# does a pass through all the simulations and dumps the quantities of interest to a plaintext data file

import h5py
from glob import glob
import numpy as np
from os.path import isdir


sims_dir = "/work/08056/hlane17/frontera/fragthreshold/"

# initialize lists to store all the stuff we will want in the final data file
SFEs = [] # star formation efficiency: mstar / (mstar + mgas)
tenpercent_frac = [] # fraction of stellar mass in stars > 10% the total stellar mass
Mmax_frac = [] # mass fraction of the most massive thing
infall_machs = []
alphas = []
sol_fracs = []
seeds = []
mus = []
Ngas = []


for dir in glob(sims_dir+"mach*alpha*/output"): # this will work without having to update the list of parameters in the script - just looks for all directories that match the pattern and have an output directory inside
    # get the run parameters from the directory name
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

    if mstar.sum() > 0: Mmax_frac.append(mstar.max() / mstar.sum()) 
    else: Mmax_frac.append(np.nan) # handle the empty case where max 

np.savetxt("SimulationData.dat", np.c_[infall_machs, alphas, mus, sol_fracs, Ngas, seeds, SFEs, tenpercent_frac, Mmax_frac], 
           header = "#(0) infall mach (1) alpha (2) mu (3) solenoidal fractino (4) Ngas (5) seed (6) SFE (7) > 10% mass frac (8) max mass frac"
)

