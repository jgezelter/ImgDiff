#!/bin/bash
#SBATCH --job-name=3d-grating-disp
#SBATCH --time=23:30:00
#SBATCH --output=results/260226/3d-grating-dispersion_p/med.out
#SBATCH --mem=21G
#SBATCH --array=0-1499:5

module purge
module load anaconda3/2025.6
conda activate ImgDiff

echo "Starting task 1499-$SLURM_ARRAY_TASK_ID"

python 3d_grating-angle-freq_med.py $SLURM_ARRAY_TASK_ID