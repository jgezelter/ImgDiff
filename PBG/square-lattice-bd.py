import meep as mp
from meep import mpb
import meep.materials as materials

import numpy as np
import matplotlib.pyplot as plt
import sys
import itertools
import pandas as pd

import math

num_bands = 40

k_point_options = np.linspace(0,1.5*10**(-2),50)
r_options = np.linspace(0,0.5,44)

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

args=expand_grid({
    "k": k_point_options,
    "r": r_options
    }
)

index = int(sys.argv[1])


k_X = [mp.Vector3(0,0,0),mp.Vector3(args["k"][index],0,0)]
k_M = [mp.Vector3(0,0,0),mp.Vector3(args["k"][index]/np.sqrt(2),args["k"][index]/np.sqrt(2),0)]





pp=1
sx=pp
sy=pp
pr=args["r"][index]


default_material=mp.Medium(epsilon=1)

geometry = [
    mp.Block(
        material = mp.Medium(epsilon=12), 
        size=mp.Vector3(sx,sy,0.5),
        center=mp.Vector3()
    ),
    mp.Cylinder(
        material = mp.Medium(epsilon=1),
        height = 0.7, 
        radius = pr, 
        axis = mp.Vector3(0,0,1), 
        center = mp.Vector3()
    )
]


geometry_lattice = mp.Lattice(size = mp.Vector3(sx, sx, 20))

resolution = 40



ms_3d_test = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_X,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

ms_3d_test.run_zodd(mpb.fix_efield_phase)
test_freqs = ms_3d_test.all_freqs

mode_check = [np.inf]*num_bands

for i in range(num_bands):
    
    d_=ms_3d_test.get_dfield(i+1)
    e_=np.conjugate(ms_3d_test.get_efield(i+1))

    u_=np.multiply(d_,e_)
    if i+1==1:
        mode_check[i]=1
    else:
        if 500*np.max(np.abs(u_[0:40,0:40,0:350]))< np.max(np.abs(u_[0:40,0:40,383:413])):
            mode_check[i]=1

inter = np.multiply(test_freqs,mode_check)
out = np.sort(inter)


np.save(f"results/260518/band_diagram_blank/raw/odd_X_{index}", out)
'''

ms_3d_test = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_X,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

ms_3d_test.run_zeven(mpb.fix_efield_phase)
test_freqs = ms_3d_test.all_freqs

mode_check = [np.inf]*num_bands

for i in range(num_bands):
    
    d_=ms_3d_test.get_dfield(i+1)
    e_=np.conjugate(ms_3d_test.get_efield(i+1))

    u_=np.multiply(d_,e_)
    if i+1==1:
        mode_check[i]=1
    else:
        if (10**3)*np.max(np.abs(u_[0:30,0:30,0:250]))< np.max(np.abs(u_[0:30,0:30,290:310])):
            mode_check[i]=1

inter = np.multiply(test_freqs,mode_check)
out = np.sort(inter)

np.save(f"results/260518/band_diagram_blank/raw/even_X_{index}", out)

ms_3d_test = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_M,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

ms_3d_test.run_zodd(mpb.fix_efield_phase)
test_freqs = ms_3d_test.all_freqs

mode_check = [np.inf]*num_bands

for i in range(num_bands):
    
    d_=ms_3d_test.get_dfield(i+1)
    e_=np.conjugate(ms_3d_test.get_efield(i+1))

    u_=np.multiply(d_,e_)
    if i+1==1:
        mode_check[i]=1
    else:
        if (10**3)*np.max(np.abs(u_[0:30,0:30,0:250]))< np.max(np.abs(u_[0:30,0:30,290:310])):
            mode_check[i]=1

inter = np.multiply(test_freqs,mode_check)
out = np.sort(inter)

np.save(f"results/260518/band_diagram_blank/raw/odd_M_{index}", out)

ms_3d_test = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_M,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

ms_3d_test.run_zeven(mpb.fix_efield_phase)
test_freqs = ms_3d_test.all_freqs

mode_check = [np.inf]*num_bands

for i in range(num_bands):
    
    d_=ms_3d_test.get_dfield(i+1)
    e_=np.conjugate(ms_3d_test.get_efield(i+1))

    u_=np.multiply(d_,e_)
    if i+1==1:
        mode_check[i]=1
    else:
        if (10**3)*np.max(np.abs(u_[0:30,0:30,0:250]))< np.max(np.abs(u_[0:30,0:30,290:310])):
            mode_check[i]=1

inter = np.multiply(test_freqs,mode_check)
out = np.sort(inter)

np.save(f"results/260518/band_diagram_blank/raw/even_M_{index}", out)
'''