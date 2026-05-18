import sys
import os
import glob

import numpy as np
import math
import cmath

import pandas as pd
import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

import subprocess

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

index = int(sys.argv[1])
num_sim = int(sys.argv[2])
path = sys.argv[3]

#params=pd.read_csv(f"parameter_space.csv")

min_freq = 0.4
max_freq = 0.5
num_freq = 2201
is_s=1

freq_=np.linspace(min_freq,max_freq,num_freq)
'''
args=expand_grid({
    "pr": rad_um_,
    "ph": height_um_
    }
)
'''
for i in range(num_sim):
        #files = glob.glob(f"{path}raw/*.csv")
        #results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["ph", "pr", "trans"], axis = 1).round(5)

        freq = freq_[index*num_sim + i]
        #height_um = args["ph"][index*num_sim + i]

        #results_test = args.merge(results, on=["pr", "ph"], how = "left")
        #if results_test.isna()["trans"][index*num_sim + i]:
        subprocess.run(["python", f"{os.getcwd()}/test-sim.py", f"{freq}", "0", f"{is_s}", f"{path}raw/", f"0.1", f"0.3", "1", "1"])
        #os.remove(f"{os.getcwd()}raw/batch.{index}.out")
