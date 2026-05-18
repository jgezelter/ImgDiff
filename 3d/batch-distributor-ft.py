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

min_angle = params["min_angle"][0]
max_angle = params["max_angle"][0]
num_angle = params["num_angle"][0]
is_s=params["s?"][0]

angle_deg_=np.linspace(min_angle,max_angle,num_angle)


for i in range(num_sim):
        #files = glob.glob(f"{path}raw/*.csv")
        #results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["ph", "pr", "trans"], axis = 1).round(5)

        #rad_um = args["pr"][index*num_sim + i]
        #height_um = args["ph"][index*num_sim + i]
        angle_deg=angle_deg_[index*num_sim + i]
        '''
        results_test = args.merge(results, on=["pr", "ph"], how = "left")
        if results_test.isna()["trans"][index*num_sim + i]:
              subprocess.run(["python", f"{os.getcwd()}/3d-sim.py", "whatever", f"{angle_deg}", f"{is_s}", f"{path}raw/", f"0.44", f"0.14", "0.6", "0.6"])
        #os.remove(f"{path}raw/batch.{index}.out")
        '''

        subprocess.run(["python", f"{os.getcwd()}/3d-sim-ft-lo.py", "whatever", f"{angle_deg}", f"{is_s}", f"{path}raw/", f"0.44", f"0.14", "0.6", "0.6", "9"])