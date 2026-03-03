#!/bin/bash
#SBATCH --job-name=single_job                    # create a short name for your job
#SBATCH --account=akey                           # which account to use
#SBATCH --nodes=1                                # node count
#SBATCH --ntasks=1                               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1                        # cpu-cores per task (equal to $SLURM_CPUS_PER_TASK)
#SBATCH --mem=1G                                 # total cpu requested memory
#SBATCH --time=01:00:00                          # total run time limit (HH:MM:SS)
#SBATCH --output=slurm_outs/slurm-%x-%j.out      # for non-array job, name slurm-out with job-name (%x) and job-num (%j)

#set bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

echo "Hello world! I'm a single non-array job"
