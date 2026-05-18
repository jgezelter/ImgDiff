#!/bin/bash
#SBATCH --job-name=3d-grating-disp
#SBATCH --time=3:30:00
#SBATCH --output=results/260226/3d-grating-dispersion_p/short.out
#SBATCH --mem=8G
#SBATCH --array=0-1499

module purge
module load anaconda3/2025.6
conda activate ImgDiff

echo "Starting task $SLURM_ARRAY_TASK_ID"

python 3d_grating-angle-freq_short.py $SLURM_ARRAY_TASK_ID