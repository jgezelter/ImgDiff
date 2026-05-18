import sys

import numpy as np
import math
import cmath

import meep as mp
from meep import materials
import meep.visualization as vis

import pandas as pd
import itertools

import matplotlib.pyplot as plt
import glob

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def transmittance(ppx, ppy, pr, ph, angle_deg, freq_THz):
    resolution = 150 # fdtd grid resolution

    theta_r = math.radians(angle_deg) # convert angle to radians

    fcen = freq_THz/300 # source center wavelength

    dpml = 1 # perfectly matched layer thickness
    dpad = 5 * ph # thickness of glass above/below PhC

    # cell dimensions
    sx = ppx 
    sy = ppy
    sz = dpml + dpad + ph + dpad + dpml

    cell_size = mp.Vector3(sx, sy, sz)

    # cell Z boundary
    pml_layers = [mp.PML(thickness=dpml, direction=mp.Z)]

    k_point = mp.Vector3(0, 0, fcen * 1.45).rotate(mp.Vector3(0, 1, 0), theta_r)

    src_pt = mp.Vector3(0,0, 0.5 * (sz - 2 * dpml - ph))
    ref_mon_pt = mp.Vector3(0,0, 0.5 * (dpad + dpml))
    trans_mon_pt = mp.Vector3(0,0, -0.5 * (ph + dpad + dpml))

    default_material = mp.Medium(index = 1.45)

    geometry = [
        mp.Cylinder(
            material = mp.Medium(index=3.67),
            height = ph, 
            radius = pr, 
            axis = mp.Vector3(0,0,1), 
            center = mp.Vector3()
        )
    ]

    def pw_amp(k, x0):
        def _pw_amp(x):
            return cmath.exp(1j * 2 * math.pi * k.dot(x + x0))
        
        return _pw_amp

    sources = [
        mp.Source(
            mp.ContinuousSource(fcen), 
            component = mp.Hy, 
            center = src_pt,
            size = mp.Vector3(sx, sy, 0), 
            amp_func=pw_amp(k_point, src_pt)
        )
    ]

    symmetries = []

    sim_base = mp.Simulation(
        resolution=resolution,
        cell_size=cell_size,
        boundary_layers=pml_layers,
        k_point=k_point,
        sources=sources, 
        symmetries = symmetries, 
        default_material = default_material
    )

    trans_flux = sim_base.add_flux(
        fcen, 
        0, 
        1, 
        mp.FluxRegion(center = trans_mon_pt, size = mp.Vector3(sx, sy, 0))
    )
    
    sim_base.run(until = 20)

    b_flux = mp.get_fluxes(trans_flux)

    sim = mp.Simulation(
        resolution=resolution,
        cell_size=cell_size,
        boundary_layers=pml_layers,
        k_point=k_point,
        sources=sources, 
        default_material = default_material, 
        geometry=geometry,
        symmetries = symmetries
    )

    trans_flux = sim.add_flux(
        fcen, 
        0, 
        1, 
        mp.FluxRegion(center = trans_mon_pt, size = mp.Vector3(sx, sy, 0))
    )
    
    sim.run(until = 20)

    
    t_flux = mp.get_fluxes(trans_flux)
    Tflux = t_flux[0]/b_flux[0]
    
    fig, ax = plt.subplots(1,3)
    vis.plot_eps(
        sim = sim, 
        ax = ax[0], 
        output_plane=mp.Volume(
            center = mp.Vector3(), 
            size = mp.Vector3(sx, 0, sz)),
        eps_parameters =  {
            "interpolation": "spline36",
            "cmap": "jet",
            "alpha": 1.0,
            "contour": False,
            "contour_linewidth": 1,
            "frequency": None,
            "resolution": None,
            "colorbar": True,
        }, 
        colorbar_parameters={
            "label": None,
            "orientation": "vertical",
            "extend": None,
            "position": "right",
            "size": "10%",
            "pad": "10%",
        }
        
    )
    vis.plot_fields(
        sim = sim, 
        fields=mp.Hy,
        ax = ax[1], 
        output_plane=mp.Volume(
            center = mp.Vector3(), 
            size = mp.Vector3(sx, 0, sz)),
        field_parameters={
            "interpolation": "spline36",
            "cmap": "RdBu",
            "alpha": 0.8,
            "post_process": np.real,
            "colorbar": True,
        },
        colorbar_parameters={
            "label": None,
            "orientation": "vertical",
            "extend": None,
            "position": "right",
            "size": "10%",
            "pad": "10%",
        }
        
    )
    vis.plot_fields(
        sim = sim, 
        fields=mp.Hy,
        ax = ax[2], 
        output_plane=mp.Volume(
            center = mp.Vector3(), 
            size = mp.Vector3(sx, sy, 0)),
        field_parameters={
            "interpolation": "spline36",
            "cmap": "RdBu",
            "alpha": 0.8,
            "post_process": np.real,
            "colorbar": True,
        },
        colorbar_parameters={
            "label": None,
            "orientation": "vertical",
            "extend": None,
            "position": "right",
            "size": "10%",
            "pad": "10%",
        }
        
    )

    #sim.plot2D(fields=mp.Ey, output_plane=mp.Volume(center = mp.Vector3(), size = mp.Vector3(sx, sy, 0)), ax=ax[1])
    fig.savefig(f"results/260226/3d-grating-dispersion_p/raw/{angle_deg}-{freq_THz}.png")

    return Tflux
    
    
            

if __name__ == "__main__":
    ppx = 0.6
    ppy = 0.6
    pr = 0.14
    ph = 0.44

    angle_deg_ = np.linspace(0, 20, 30)
    freq_THz_ = np.linspace(220, 290, 50)

    args = expand_grid({"angle": angle_deg_, 
                        "freq": freq_THz_})
    

    
    for i in range(1):
        angle_deg = args["angle"][int(sys.argv[1]) + i]
        freq_THz = args["freq"][int(sys.argv[1]) + i]
    
        out_data = {
            "angle_deg": [angle_deg], 
            "freq_THz": [freq_THz], 
            "trans": [transmittance(ppx, ppy, pr, ph, angle_deg, freq_THz)]
        }
    
        out = pd.DataFrame(out_data)
        filename = f"results/260226/3d-grating-dispersion_p/raw/{angle_deg}-{freq_THz}.csv"
        out.to_csv(filename, index = False)




  