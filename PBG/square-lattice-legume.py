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
    test_vals = vals[(counts>1) & (vals != 0)]

    mask = np.isin(test_freqs.round(7), test_vals)
    masked = tot_freq.transpose()[mask]

    band_locs = np.ndarray((len(test_vals), 2, 2, num_points))

    for i in range(len(test_vals)):
        band_locs[i][0]=masked[i*2:(i+1)*2, 0:num_points]
        band_locs[i][1]=-1*np.flip(masked[i*2:(i+1)*2, 1*(num_points+1):-1], 1)

    
    aniso = (band_locs.sum(axis=1)**2).sum(axis=(1,2))

    chosen_band =abs(band_locs[aniso == min(aniso)][0])-band_locs[aniso == min(aniso)][0][0][0][0]
    dist_to_band = abs(chosen_band).min(axis=(0,1))
    ks = np.array(range(num_points)) * test_k/num_points

    a = np.polyfit(ks, dist_to_band, deg=2)[0]
    b = np.polyfit(ks, dist_to_band, deg=2)[1]
    omega = band_locs[aniso == min(aniso)][0][0][0][0]
    return omega, a,b, np.sqrt(min(aniso))


rs = np.linspace(0,0.5, 8000)

index = int(sys.argv[1])

data = np.ndarray((4,3))

for i in range(20):
    sub_index = i + 20*index
    r = rs[sub_index]
    omega, a, b, aniso = key_vals(r)

    data[i][0] = r
    data[i][1] = omega
    data[i][2] = a
    data[i][3] = b
    data[i][4] = aniso

pd.DataFrame(data, columns = ["r", "a", "aniso", "b"]).to_csv(f"results/260521/band_diagram_optimization/raw/{index}.csv")
    
    
