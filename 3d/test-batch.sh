#!/bin/bash
#SBATCH --job-name=3d-grating-dim_opt
#SBATCH --time=12:00:00
#SBATCH --output=results/260318/3d-grating-3/raw/batch.%a.out
#SBATCH --mem=10G
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=genoa
#SBATCH --array=0-2200

echo "running on node: $SLURMD_NODENAME"

start_time=`date +%s`


module purge

end_time=`date +%s`

echo "Purge was" `expr $end_time - $start_time` s.
start_time=`date +%s`

module load gcc-toolset/14

end_time=`date +%s`

echo "load gcc-toolset/14 was" `expr $end_time - $start_time` s.
start_time=`date +%s`

module load aocc/5.0.0

end_time=`date +%s`

echo "load aocc/5.0.0 was" `expr $end_time - $start_time` s.
start_time=`date +%s`

module load fftw/aocc-5.0.0/3.3.10

end_time=`date +%s`

echo "load fftw/aocc-5.0.0/3.3.10 was" `expr $end_time - $start_time` s.
start_time=`date +%s`

module load anaconda3/2025.6

end_time=`date +%s`

echo "load anaconda3/2025.6 was" `expr $end_time - $start_time` s.
start_time=`date +%s`

conda activate ImgDiff

end_time=`date +%s`

echo "conda env activate was" `expr $end_time - $start_time` s.


echo "Starting task $SLURM_ARRAY_TASK_ID"
start_time=`date +%s`
python test-distributor.py $SLURM_ARRAY_TASK_ID 1 results/260318/3d-grating-3/
end_time=`date +%s`

echo "task $SLURM_ARRAY_TASK_ID execution time was" `expr $end_time - $start_time` s.