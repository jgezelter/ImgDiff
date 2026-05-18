#!/bin/bash
#SBATCH --job-name=3d-grating-ft-p-9
#SBATCH --time=23:50:00
#SBATCH --output=results/260325/3d-grating-ft-p-9/raw/batch.%a.out
#SBATCH --mem=10G
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=genoa
#SBATCH --array=0-99

echo "running on node: $SLURMD_NODENAME"

module purge
module load gcc-toolset/14
module load aocc/5.0.0
module load fftw/aocc-5.0.0/3.3.10
module load anaconda3/2025.12
conda activate ImgDiffP

echo "Starting task $SLURM_ARRAY_TASK_ID"
start_time=`date +%s`
mp
python batch-distributor-ft.py $SLURM_ARRAY_TASK_ID 1 results/260325/3d-grating-ft-p-9/
end_time=`date +%s`

echo "task $SLURM_ARRAY_TASK_ID execution time was" `expr $end_time - $start_time` s.