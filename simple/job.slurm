#!/bin/bash -l
#SBATCH -p volta
#SBATCH --gres=gpu:1
#SBATCH -N 1
#SBATCH --exclusive

source ~/.bashrc

python run-all.py


