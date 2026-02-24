#!/bin/bash
#SBATCH --job-name=array                         # create a short name for your job
#SBATCH --account=akey                           # which account to use
#SBATCH --nodes=1                                # node count
#SBATCH --ntasks=1                               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1                        # cpu-cores per task (equal to $SLURM_CPUS_PER_TASK)
#SBATCH --mem=1G                                 # total cpu requested memory
#SBATCH --time=02:00:00                          # total run time limit (HH:MM:SS)
#SBATCH --array=1-10                             # array'd jobs (each job will have $SLURM_ARRAY_TASK_ID)
#SBATCH --output=slurm_outs/slurm-%x-%A_%a.out   # for array job, name slurm-out with job-name (%x), job-id (%A), and array-num (%a)

#set bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

echo "Hello world!"
echo "I am job ${SLURM_ARRAY_TASK_ID} of ${SLURM_ARRAY_TASK_COUNT}"
