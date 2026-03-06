#!/bin/bash
#SBATCH --job-name=primes                        # create a short name for your job
#SBATCH --account=akey                           # which account to use
#SBATCH --nodes=1                                # node count
#SBATCH --ntasks=1                               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1                        # cpu-cores per task
#SBATCH --mem=1G                                 # total cpu requested memory
#SBATCH --time=00:10:00                          # total run time limit (HH:MM:SS)
#SBATCH --output=slurm-%x-%j.out                 # output file named with job-name and job-id

#set bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

python find_primes.py
