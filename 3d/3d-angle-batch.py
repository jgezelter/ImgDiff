import math
import cmath
import numpy as np

import matplotlib.pyplot as plt

import meep as mp
from meep import materials

def transmittance(ppx, ppy, pr, ph, angle_deg, wl):
    resolution = 50 # fdtd grid resolution

    theta_r = math.radians(angle_deg) # convert angle to radians

    fcen = 1/wl # source center wavelength
    df = 0.05 * fcen # source bandwidth

    dpml = 1 # perfectly matched layer thickness
    dsub = 5 * ph # thickness of glass below PhC
    dtop = 5 * ph # thickness of glass above PhC

    # cell dimensions
    sx = ppx 
    sy = ppy
    sz = dpml + dsub + ph + dtop + dpml

    cell_size = mp.Vector3(sx, sy, sz)

    # cell Z boundary
    pml_layers = [mp.PML(thickness=dpml, direction=mp.Z)]

    # calculations for index of the glass at target wavelength
    eps_fq = (
        1 + 
        sellmeier(
            omega = materials.fused_quartz_frq1, 
            sigma = materials.fused_quartz_sig1, 
            wavelength = wl
        ) + 
        sellmeier(
            omega = materials.fused_quartz_frq2, 
            sigma = materials.fused_quartz_sig2, 
            wavelength = wl
        ) + 
        sellmeier(
            omega = materials.fused_quartz_frq3, 
            sigma = materials.fused_quartz_sig3, 
            wavelength = wl
        )
    )

    index_fq = math.sqrt(eps_fq) # permittivity to index
            

    k_point = mp.Vector3(0, 0, fcen * index_fq).rotate(mp.Vector3(1, 0, 0), theta_r)

    src_pt = mp.Vector3(0, 0, 0.5 * sz - 0.5 * (dpml + dtop + ph))
    ref_mon_pt = mp.Vector3(0, 0, 1.1 * ph)
    trans_mon_pt = mp.Vector3(0, 0, -0.5 * sz + 0.5 * (dpml + dsub))

    geometry = [
        mp.Block(
            material = materials.fused_quartz, 
            size = mp.Vector3(mp.inf, mp.inf, sz), 
            center = mp.Vector3()
        ), 
        mp.Cylinder( 
            material = materials.aSi, 
            height = ph, 
            radius= pr, 
            axis = mp.Vector3(0, 0, 1), 
            center = mp.Vector3(0, 0, 0.5 * ph)
        )
    ]

    def pw_amp(k, x0):
        def _pw_amp(x):
            return cmath.exp(1j * 2 * math.pi * k.dot(x + x0))
        
        return _pw_amp

    sources = [
        mp.Source(
            mp.ContinuousSource(fcen, fwidth = df), 
            component = mp.Ex, 
            center = src_pt,
            size = mp.Vector3(sx, sy, 0), 
            amp_func=pw_amp(k_point, src_pt)
        )
    ]

    symmetries = [mp.Mirror(mp.Y)]

    sim = mp.Simulation(
        resolution=resolution,
        cell_size=cell_size,
        boundary_layers=pml_layers,
        k_point=k_point,
        geometry=geometry,
        sources=sources, 
        symmetries = symmetries
    )

    baseline_flux = sim.add_flux(
        fcen, 
        0, 
        1, 
        mp.FluxRegion(center = ref_mon_pt, size = mp.Vector3(sx, sy, 0))
    )
    trans_flux = sim.add_flux(
        fcen, 
        0, 
        1, 
        mp.FluxRegion(center = trans_mon_pt, size = mp.Vector3(sx, sy, 0))
    )
    
    sim.run(until = 50)

    b_flux = mp.get_fluxes(baseline_flux)
    t_flux = mp.get_fluxes(trans_flux)
    Tflux = t_flux[0]/b_flux[0]

    return Tflux