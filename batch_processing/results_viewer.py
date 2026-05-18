import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import glob
import sys

path = sys.argv[1]

params=pd.read_csv(f"{path}parameter_space.csv")

min_freq = params["min_rad"][0]
max_freq = params["max_rad"][0]
num_freqs = params["num_rad"][0]
min_angle = params["min_height"][0]
max_angle = params["max_height"][0]
num_angles = params["num_height"][0]
is_s=bool(params["s?"][0])

files = glob.glob(f"{path}raw/*.csv")
                  
print(len(files))

results = pd.DataFrame()

results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["ph", "pr", "trans"], axis = 1).round(5)

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

args = expand_grid(
    {
    "ph": np.linspace(min_angle, max_angle, num_angles),
    "pr": np.linspace(min_freq, max_freq, num_freqs)
    }
).round(5)


results_2 = results.sort_values(by = ["pr", "ph"])
results_2.to_csv(f"{path}full_csv.csv")

results_test = args.merge(results, on=["pr", "ph"], how = "left")

def f(x): 
    return float(str(x).strip("[]"))/-7.810053068641317

trans_test = results_test["trans"].apply(f)
trans_test_array = np.reshape(np.array(trans_test), (num_angles,num_freqs))



# trans_array = np.reshape(np.array(trans_list), (num_angles,num_freqs))
#trans_array_proper = trans_test_array.transpose()
transmittivity_array_proper = np.sqrt(trans_test_array)

freq_THz_1 = np.linspace(min_freq - (max_freq - min_freq)/(2*num_freqs), max_freq + (max_freq - min_freq)/(2*num_freqs), num_freqs +1)
angle_deg_1 = np.linspace(min_angle - (max_angle- min_angle)/(2*num_angles), max_angle + (max_angle- min_angle)/(2*num_angles), num_angles +1)

freq_THz_ = np.linspace(min_freq, max_freq, num_freqs)
angle_deg_ = np.linspace(min_angle, max_angle, num_angles)

fig, ax = plt.subplots()

d = ax.pcolormesh(freq_THz_, angle_deg_, trans_test_array, cmap = "turbo", shading = "nearest")
cbar = plt.colorbar(d, ticks = np.linspace(0,1,6))
d.set_clim(0,1)
plt.xlabel("Pillar Radius (\u03bcm)")
plt.ylabel("Pillar Height (\u03bcm)")
plt.title("$T(R,H)$")

fig.savefig(f"{path}full_result.png")

fig1, ax1 = plt.subplots()

d1 = ax1.pcolormesh(freq_THz_, angle_deg_, transmittivity_array_proper, cmap = "turbo", shading = "nearest")
cbar1 = plt.colorbar(d1, ticks = np.linspace(0,1,6))
d1.set_clim(0,1)
plt.xlabel("Pillar Radius (\u03bcm)")
plt.ylabel("Pillar Height (\u03bcm)")
plt.title("$t(R,H)$")

fig1.savefig(f"{path}full_transmittivity_result.png")

