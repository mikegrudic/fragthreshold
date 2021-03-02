#!/bin/bash                                                                     
#SBATCH -J JOBNAME -p normal -N 1 --ntasks-per-node 28 -t 48:00:00 -A AST20019 
export OMP_NUM_THREADS=2
source $HOME/.bashrc
ibrun ./GIZMO PARAMSFILE 0 1>gizmo.out 2>gizmo.err &
wait
