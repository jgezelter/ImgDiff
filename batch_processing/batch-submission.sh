#!/bin/bash
#SBATCH --job-name=square-lattice-bd
#SBATCH --time=1:30:00
#SBATCH --output=results/260521/band_diagram_optimization/out/batch.%a.out
#SBATCH --mem=2G
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=genoa
#SBATCH --array=0-399

echo "running on node: $SLURMD_NODENAME"

module purge
module load gcc-toolset/14
module load aocc/5.0.0
module load fftw/aocc-5.0.0/3.3.10
module load anaconda3/2025.12
conda activate legume-env

echo "Starting task $SLURM_ARRAY_TASK_ID"
start_time=`date +%s`
python square-lattice-legume.py $SLURM_ARRAY_TASK_ID
end_time=`date +%s`

echo "task $SLURM_ARRAY_TASK_ID execution time was" `expr $end_time - $start_time` s.