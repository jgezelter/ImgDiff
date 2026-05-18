import sys
import os

import numpy as np
import math
import cmath

import meep as mp
from meep import materials
import meep.visualization as vis

import pandas as pd
import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable


freq_THz = float(sys.argv[1])
angle_deg = float(sys.argv[2])
polarization_s = bool(int(sys.argv[3]))
path = sys.argv[4]

ph=float(sys.argv[5]) # pillar height
pr=float(sys.argv[6]) # pillar radius
ppx=float(sys.argv[7]) # unit cell x length
ppy=float(sys.argv[8]) # unit cell y length

resolution = 50 # fdtd grid resolution

theta_r = math.radians(angle_deg) # convert angle to radians

fcen = freq_THz/300 # source center frequency (MEEP units)

dpml = 1 # perfectly matched layer thickness
dpad = 10 # thickness of glass above/below PhC

# cell dimensions
sx = ppx 
sy = ppy
sz = dpml + dpad + ph + dpad + dpml

cell_size = mp.Vector3(sx, sy, sz)

# cell Z boundary
pml_layers = [mp.PML(thickness=dpml, direction=mp.Z)]

k_point = mp.Vector3(0, 0, fcen * 1).rotate(mp.Vector3(0, 1, 0), theta_r)

src_pt = mp.Vector3(0,0, 0.5 * (sz - 2 * dpml - ph))
ref_mon_pt = mp.Vector3(0,0, 0.5 * (dpad + dpml))
trans_mon_pt = mp.Vector3(0,0, -0.5 * (ph + dpad + dpml))

default_material = mp.Medium(index = 1)

geometry_base=[
    
]

geometry_trial = [
    mp.Block(
        material=mp.Medium(index=1.345),
        size=mp.Vector3(sx,sy,2),
        center=mp.Vector3(0,0,-(2+ph)/2)
    ),
    mp.Cylinder(
        material = mp.Medium(index=3.42),
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


if polarization_s:
    sources = [
        mp.Source(
            mp.GaussianSource(fcen,df=0,), 
            component = mp.Ey, 
            center = src_pt,
            size = mp.Vector3(sx, sy, 0), 
            amp_func=pw_amp(k_point, src_pt)
        )
    ]
else:
    sources = [
        mp.Source(
            mp.GaussianSource(fcen), 
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
    default_material = default_material, 
    geometry=geometry_base
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
    geometry=geometry_trial,
    symmetries = symmetries
)

trans_flux = sim.add_flux(
    fcen, 
    0, 
    1, 
    mp.FluxRegion(center = trans_mon_pt, size = mp.Vector3(sx, sy, 0))
)
if polarization_s:
    sim.run(until_after_sources=mp.stop_when_fields_decayed(dt=0.05,c=mp.Ey,pt=trans_mon_pt,decay_by=1e-9))


t_flux = mp.get_fluxes(trans_flux)
#Tflux = t_flux[0]/b_flux[0]

## plotting and storing results

fig, ax = plt.subplots(1,3)

### plot epsilon
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

### plot vertical slice of fields
sim_center_1, sim_size_1 = vis.get_2D_dimensions(
    sim, 
    mp.Volume(
        center = mp.Vector3(0,0,0), 
        size = mp.Vector3(sx, 0, (sz - 2 * dpml - ph)-0.1)
    )
)
xmin, xmax, ymin, ymax, zmin, zmax = vis.box_vertices(
        sim_center_1, sim_size_1, False
    )
extent_1 = [xmin, xmax, zmin, zmax]

if polarization_s:
    field_data_1 = np.rot90(np.real(sim.get_array(center=sim_center_1, size=sim_size_1, component=mp.Ey)))
else:
    field_data_1 = np.rot90(np.real(sim.get_array(center=sim_center_1, size=sim_size_1, component=mp.Hy)))

image_1=ax[1].imshow(
    field_data_1, 
    extent=extent_1, 
    cmap="RdBu",
    norm = mpl.colors.CenteredNorm(halfrange=np.amax(field_data_1)),
    interpolation="spline36")
fig.colorbar(
    mappable=image_1
)
ax[1].set_xlabel("X")
ax[1].set_ylabel("Z")
ax[1].set_xticks([-sx/2,0,sx/2])

### plot horizontal slice of fields
sim_center_2, sim_size_2 = vis.get_2D_dimensions(
    sim, 
    mp.Volume(
        center = mp.Vector3(0,0,0), 
        size = mp.Vector3(sx, sy, 0)
    )
)
xmin, xmax, ymin, ymax, zmin, zmax = vis.box_vertices(
        sim_center_2, sim_size_2, False
    )
extent_2 = [xmin, xmax, ymin, ymax]

if polarization_s:
    field_data_2 = np.rot90(np.real(sim.get_array(center=sim_center_2, size=sim_size_2, component=mp.Ey)))
else:
    field_data_2 = np.rot90(np.real(sim.get_array(center=sim_center_2, size=sim_size_2, component=mp.Hy)))

image_2=ax[2].imshow(
    field_data_2, 
    extent=extent_2, 
    cmap="RdBu",
    norm = mpl.colors.CenteredNorm(halfrange=np.amax(field_data_2)),
    interpolation="spline36")
fig.colorbar(
    mappable=image_2
)
ax[2].set_xlabel("X")
ax[2].set_ylabel("Y")

plt.tight_layout()

fig.savefig(f"{path}{ph}-{pr}.png")

out_data = {
    "ph": [ph], 
    "pr": [pr], 
    "trans": [t_flux]
}

out = pd.DataFrame(out_data)
out.to_csv(f"{path}{ph}-{pr}.csv", index = False)




  