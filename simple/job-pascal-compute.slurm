#!/bin/bash -l
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH -N 1
#SBATCH --exclusive

source ~/.bashrc

#python run-all.py ./output-pascal
python run-all-googlebench.py bin-googlebench-compute/ output-pascal-compute/

