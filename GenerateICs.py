# Generates all initial conditions and simulation directories for the STARFORGE fragmentation threshold project

from os import system, mkdir, chdir
from glob import glob
from os.path import isdir
import numpy as np

G = 4300.7 # gravitational constant in m/s - msun - pc units
cs = 200 # isothermal sound speed in m/s (= pressure/density, appropriate for ISM at ~10K)
sigma = 1e3 # surface density M/(pi R^2) in msun pc^-2 (this is arbitrary, just to set the dimensions of our problem - 1000 roughly corresponds to observed cores)

infall_machs = np.logspace(0.5,3,6,base=2) # the list of infall mach #'s we want - ranges from 1 to 8, evenly spaced in log space (each is a certain % larger than the last, in a geometric progression)
alphas = 0.25, 0.5, 1, 2, 4, 8 #list of turbulent virial parameters we want - 0 is no initial turbulence
mus = 4, 2, 1, 0.5 #np.inf, 4, 2, 1, 0.5, 0.25  # list of mass-to-flux ratios (greek letter mu) that we want - infinity is no magnetic field, ~0 is very strong magnetic field
seeds = 1,2,3,4,5,6,7,8,9,10,11,12,13,14 # different initial turbulent seed fields - so that we try a few different random samplings of the initial turbulence to make sure results are not a fluke
sol_fracs = 0, 0.5, 1  # 0, 1 # fraction of turbulent field in solenoidal modes 

allowed_core_num = np.array([4,8,14,28,56])

for infall_mach in infall_machs:
    for alpha in alphas:
        for mu in mus:         
            for sol_frac in sol_fracs:
                if sol_frac != 0.5 and mu != 4: continue # only do other sol_fracs for mu=4, to reduce the parameter space

                R = cs**2 * infall_mach**2 / (np.pi * G * sigma) # cloud radius
                M = np.pi * sigma * R**2 # cloud mass
                Emag = (mu/0.4)**-2. # fraction of binding energy as magnetic energy

                Ngas = max(250 * infall_mach**4, 100000) # number of gas cells in the core proper - we might as well always have at least 10k, but in Guszejnov 2020 we showed you want to make sure it's at least ~100 Mach^4 as well for things to really be converged
                num_cores_per_run = int(max(4, 2**int(np.log2(Ngas / 100000))))
                num_cores_per_run = int(allowed_core_num[np.abs(allowed_core_num - num_cores_per_run).argmin()]) # find closest allowable number of cores

                num_nodes = len(seeds) * num_cores_per_run // 56
                print("num nodes=%d num_cores_per_run=%g"%(num_nodes,num_cores_per_run))
                if num_nodes == 2: queue = "small"
                else: queue = "normal"
                run_length = 48 #min(round((Ngas/1e4)**(5./3)), 48) # run length in hours
                job_name = "mach%g_alpha%g_mu%g_sol%g_Res%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), sol_frac, round(Ngas**(1./3)))
                submit_script_text = open("template_submit.sh","r").read().replace("QUEUE",queue).replace("NUMNODES",str(num_nodes)).replace("JOBNAME", job_name).replace("HOURS", str(run_length)) # generate the text to write to the submit script
                
                if not isdir(job_name): mkdir(job_name)
                chdir(job_name)
                submit_script = open(job_name + ".sh","w")
                submit_script.write(submit_script_text)

                for seed in seeds:       
                    print(infall_mach, alpha, mu, seed, sol_frac) 
                    
                    run_name = "mach%g_alpha%g_mu%g_sol%g_Res%d_%d"%(round(infall_mach,2), round(alpha,2), round(mu,2), sol_frac, round(Ngas**(1./3)), seed) # this will be the unique identifier for the run - will want to create a new directory with this name
                    if not isdir(run_name): 
                        mkdir(run_name) # if the directory for the run does not exist, create it
                        chdir(run_name)
                        makecloud_command = "MakeCloud.py --M=%g --R=%g --N=%d --warmgas --bturb=%g --alpha_turb=%g --turb_sol=%g --tmax=10 --nsnap=10 --turb_seed=%d"%(M,R,Ngas,Emag,alpha, sol_frac,seed)
                        print("Creating: " + run_name)
                        system(makecloud_command)
                        system("cp ../../gizmo/GIZMO .") # copy GIZMO binary to current directory
                        
                        params_file_name = glob("params*.txt")[0] # to get the exact parameter filename, search for things matching the pattern and take the first result
                        submit_script.write("cd " + run_name + "\n")
                        submit_script.write("ibrun -n %d -o %d "%(num_cores_per_run, (seed-1)*num_cores_per_run) + "./GIZMO " + params_file_name + " 1>gizmo.out 2>gizmo.err &" + "\n")
                        submit_script.write("cd ..\n")
                        

#                        submit_script_text = open("../template_submit.sh","r").read().replace("JOBNAME", run_name).replace("PARAMSFILE",params_file_name).replace("HOURS", str(run_length)) # generate the text to write to the submit script
#                        open(run_name + ".sh", "w").write(submit_script_text) # write the submit script
                        chdir("../") # go back to the top level directory
                    else:
                        print("skipped")
                submit_script.write("wait")
                chdir("../") # go back to the top level directory


                
