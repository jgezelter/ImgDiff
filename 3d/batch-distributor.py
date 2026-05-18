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

params=pd.read_csv(f"{path}parameter_space.csv")

min_rad = params["min_rad"][0]
max_rad = params["max_rad"][0]
num_rad = params["num_rad"][0]
min_height = params["min_height"][0]
max_height = params["max_height"][0]
num_height = params["num_height"][0]
is_s=params["s?"][0]

rad_um_=np.linspace(min_rad,max_rad,num_rad)
height_um_=np.linspace(min_height, max_height, num_height)

args=expand_grid({
    "pr": rad_um_,
    "ph": height_um_
    }
)

for i in range(num_sim):
        files = glob.glob(f"{path}raw/*.csv")
        results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["ph", "pr", "trans"], axis = 1).round(5)

        rad_um = args["pr"][index*num_sim + i]
        height_um = args["ph"][index*num_sim + i]

        results_test = args.merge(results, on=["pr", "ph"], how = "left")
        if results_test.isna()["trans"][index*num_sim + i]:
              subprocess.run(["python", f"{os.getcwd()}/3d-sim.py", "37.474057025", "0", f"{is_s}", f"{path}raw/", f"{height_um}", f"{rad_um}", "4", "4"])
        #os.remove(f"{path}raw/batch.{index}.out")
