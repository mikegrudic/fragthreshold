#!/usr/bin/env python
# coding: utf-8

# In[3]:
###Don't run on head node. Run inside fragset2 directory.

from os import system, mkdir, chdir
import os
from glob import glob
from os.path import isdir
import numpy as np
import h5py
import multiprocessing 
from multiprocessing import Pool
# In[8]:

nproc = multiprocessing.cpu_count()

sims_dir = "/scratch1/08056/hlane17/fragset2/"

def TarDirectory(f):
    return print("tar -czvf " + f + ".tar.gz " + "/scratch1/08056/hlane17/fragset2/" + f) #!

dir = glob(sims_dir+"mach*alpha*")
dirs = os.path.basename(os.path.normpath(dir))
Pool(nproc).map(TarDirectory, dirs)

# In[ ]:




