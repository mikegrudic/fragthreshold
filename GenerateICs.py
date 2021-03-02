# Generates all initial conditions and simulation directories for the STARFORGE fragmentation threshold project

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

for infall_mach in infall_machs:
    for alpha in alphas:
        for mu in mus:
            for seed in seeds:                
                print(infall_mach, alpha, mu, seed)
                R = cs**2 * infall_mach**2 / (np.pi * G * sigma) # cloud radius
                M = np.pi * sigma * R**2 # cloud mass
                Emag = (mu/0.4)**-2. # fraction of binding energy as magnetic energy

                Ngas = max(100 * infall_mach**4, 10000) # number of gas cells in the core proper - we might as well always have at least 10k, but in Guszejnov 2020 we showed you want to make sure it's at least ~100 Mach^4 as well for things to really be converged
            
                run_name = "mach%g_alpha%g_mu%g_Res%d_%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), seed, round(Ngas**(1./3))) # this will be the unique identifier for the run - will want to create a new directory with this name
                if not isdir(run_name): mkdir(run_name) # if the directory for the run does not exist, create it
                chdir(run_name)
                makecloud_command = "MakeCloud.py --M=%g --R=%g --N=%d --warmgas --bturb=%g --alpha_turb=%g"%(M,R,Ngas,Emag,alpha)
                system(makecloud_command)
                system("cp ../gizmo/GIZMO .") # copy GIZMO binary to current directory
                
                params_file_name = glob("params*.txt")[0] # to get the exact parameter filename, search for things matching the pattern and take the first result

                submit_script_text = open("../template_submit.sh","r").read().replace("JOBNAME", run_name).replace("PARAMSFILE",params_file_name) # generate the text to write to the submit script
                open(run_name + ".sh", "w").write(submit_script_text) # write the submit script
                
                chdir("../") # go back to the top level directory
                


                
