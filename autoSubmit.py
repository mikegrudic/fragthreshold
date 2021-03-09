#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import system, mkdir, chdir
from glob import glob
from os.path import isdir
import numpy as np

G = 4300.7 # gravitational constant in m/s - msun - pc units
cs = 200 # isothermal sound speed in m/s (= pressure/density, appropriate for ISM at ~10K)
sigma = 1e3 # surface density M/(pi R^2) in msun pc^-2 (this is arbitrary, just to set the dimensions of our problem - 1000 roughly corresponds to observed cores)

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
                    run_name = "mach%g_alpha%g_mu%g_sol%g_Res%d_%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), sol_frac, round(Ngas**(1./3)), seed) # this will be the unique identifier for the run - will want to create a new directory with this name
                    chdir(run_name)
                    submit_command = ""sbatch " + run_name + ".sh""
                    print(submit_command)

                    chdir("../") # go back to the top level directory


# In[ ]:




