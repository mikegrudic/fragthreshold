#!/usr/bin/env python
# coding: utf-8

# In[1]:

#Only to be executed in the $SCRATCH space
from os import system, mkdir, chdir
from glob import glob
from os.path import isdir
import numpy as np

G = 4300.7 # gravitational constant in m/s - msun - pc units
cs = 200 # isothermal sound speed in m/s (= pressure/density, appropriate for ISM at ~10K)
sigma = 1e3 # surface density M/(pi R^2) in msun pc^-2 (this is arbitrary, just to set the dimensions of our problem - 1000 roughly corresponds to observed cores)

infall_machs = 1.41, #np.logspace(0.5,3,6,base=2) # the list of infall mach #'s we want - ranges from 1 to 8, evenly spaced in log space (each is a certain % larger than the last, in a geometric progression)
alphas = 0.25, 0.5, 1, 2, 4, 8 #list of turbulent virial parameters we want - 0 is no initial turbulence
mus = 4, 2, 1, 0.5 #np.inf, 4, 2, 1, 0.5, 0.25  # list of mass-to-flux ratios (greek letter mu) that we want - infinity is no magnetic field, ~0 is very strong magnetic field
seeds = 1,2,3,4,5,6,7,8,9,10,11,12,13,14 # different initial turbulent seed fields - so that we try a few different random samplings of the initial turbulence to make sure results are not a fluke
sol_fracs = 0, 0.5, 1  # 0, 1 # fraction of turbulent field in solenoidal modes 

for infall_mach in infall_machs:
    for alpha in alphas:
        for mu in mus:
            for seed in seeds:                
                for sol_frac in sol_fracs:
                    if sol_frac != 0.5 and mu != 4: continue
                    Ngas = max(250 * infall_mach**4, 100000) # number of gas cells in the core proper - we might as well always have at least 10k, but in Guszejnov 2020 we showed you want to make sure it's at least ~100 Mach^4 as well for things to really be converged
                    run_name = "mach%g_alpha%g_mu%g_sol%g_Res%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), sol_frac, round(Ngas**(1./3))) # this will be the unique identifier for the run - will want to create a new directory with this name
                        if not path.exists(run_name + "/slurm*.out"):
                            chdir(run_name)
                            submit_command = "sbatch " + run_name + ".sh"
                            print(submit_command)

                            chdir("../") # go back to the top level directory
                        else:
                            print("skipped " + run_name)


# In[ ]:




