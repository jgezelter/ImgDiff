import meep as mp
from meep import mpb
import meep.materials as materials
import legume
import legume.viz
import legume.backend as bd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.optimize as spo
import pandas as pd

import math

import sys
import os

def key_vals(r):
    D=0.55
    epsr=12
    lattice = legume.Lattice("square")
    phc = legume.PhotCryst(lattice)
    phc.add_layer(d=D, eps_b=epsr)
    phc.layers[-1].add_shape(legume.Circle(eps=1.0, r=r))
    gme = legume.GuidedModeExp(phc, gmax=6)

    test_k = 0.03
    num_points = 40

    path = lattice.bz_path([[0,0], [test_k,0], [test_k/np.sqrt(2), test_k/np.sqrt(2)], [0,0]], [num_points,1,num_points])
    gme.run(
        kpoints=path["kpoints"], 
        gmode_inds = [0,1,2,3,4,5,6], 
        numeig=40,
        verbose = True
    )

    tot_freq = gme.freqs
    test_freqs = tot_freq[0]
    vals, counts = np.unique(test_freqs.round(7), return_counts=True)
    test_vals = vals[(counts>1) & (vals > 0.01)]

    mask = np.isin(test_freqs.round(7), test_vals)
    masked = tot_freq.transpose()[mask]

    band_locs = np.ndarray((len(test_vals), 2, 2, num_points))

    for i in range(len(test_vals)):
        band_locs[i][0]=masked[i*2:(i+1)*2, 0:num_points]
        band_locs[i][1]=-1*np.flip(masked[i*2:(i+1)*2, 1*(num_points+1):-1], 1)

    
    aniso = (band_locs.mean(axis=1)**2).sum(axis=(1,2))

    chosen_band =abs(band_locs[aniso == min(aniso)][0])-band_locs[aniso == min(aniso)][0][0][0][0]
    dist_to_band = abs(band_locs).mean(axis=(1,2))
    ks = np.array(range(num_points)) * test_k/num_points

    poly = np.polyfit(ks, dist_to_band.transpose(), deg=2)

    a = poly[0]
    b = poly[1]
    omega = test_vals
    return omega, a,b, np.sqrt(aniso)


rs = np.linspace(0,0.5, 8000)

index = int(sys.argv[1])

data = np.ndarray()

for i in range(20):
    sub_index = i + 20*index
    r = rs[sub_index]
    omega, a, b, aniso = key_vals(r)

    temp_data = np.ndarray((5,len(omega)))
    temp_data[0] = r
    temp_data[1] = omega
    temp_data[2] = a
    temp_data[3] = b
    temp_data[4] = aniso

    np.concatenate((data, temp_data.T))

pd.DataFrame(data, columns = ["r", "omega", "a", "b", "aniso"]).to_csv(f"results/260521/band_diagram_optimization/raw/{index}.csv")
    
    
