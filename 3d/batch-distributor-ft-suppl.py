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
freq_THz_=np.linspace(220/300,290/300,1000)
args=expand_grid(
      {
      "angle_deg": angle_deg_,
      "freqs": freq_THz_
      }
)


for i in range(num_sim):
        for decay in range(5,10):
            files = glob.glob(f"{path}raw/*.csv")
            results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["angle_deg","freqs", "trans"], axis = 1).round(5)

            #rad_um = args["pr"][index*num_sim + i]
            #height_um = args["ph"][index*num_sim + i]
            angle_deg=angle_deg_[index*num_sim + i]
            
            results_test = args.merge(results, on=["angle_deg", "freqs"], how = "left")
            if results_test.isna()["trans"][(index*num_sim + i)*1000]:
                subprocess.run(["python", f"{os.getcwd()}/3d-sim-ft.py", "whatever", f"{angle_deg}", f"{is_s}", f"{path}raw-{decay}/", f"0.44", f"0.14", "0.6", "0.6", f"{decay}"])
            #os.remove(f"{path}raw/batch.{index}.out")
            '''
            for decay in range(4,10):
                subprocess.run(["python", f"{os.getcwd()}/3d-sim-ft.py", "whatever", f"{angle_deg}", f"{is_s}", f"{path}raw-{decay}/", f"0.44", f"0.14", "0.6", "0.6", f"{decay}"])
                '''