import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import glob
import sys

path = sys.argv[1]

params=pd.read_csv(f"{path}parameter_space.csv")

min_freq = 220
max_freq = 290
num_freqs = 1000
min_angle = params["min_angle"][0]
max_angle = params["max_angle"][0]
num_angles = params["num_angle"][0]
is_s=bool(params["s?"][0])

files = glob.glob(f"{path}raw/*.csv")
                  
print(len(files))

results = pd.DataFrame()

results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
results["freq_THz"]=np.multiply(results["freqs"],300)

results=results.round(5)

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

args = expand_grid(
    {
    "angle_deg": np.linspace(min_angle, max_angle, num_angles),
    "freq_THz": np.linspace(min_freq, max_freq, num_freqs)
    }
).round(5)


results_2 = results.sort_values(by = ["angle_deg", "freq_THz"])
results_2.to_csv(f"{path}full_csv.csv")

results_test = args.merge(results, on=["angle_deg", "freq_THz"], how = "left")

freq_THz_ = np.linspace(min_freq, max_freq, num_freqs)
angle_deg_ = np.linspace(min_angle, max_angle, num_angles)


trans_test = results_test["trans"]
trans_test_array = np.reshape(np.array(trans_test), (90,num_freqs))

trans_list = results_2["trans"]

trans_empty_list  = trans_list
# trans_array = np.reshape(np.array(trans_list), (num_angles,num_freqs))
trans_array_proper = trans_test_array.transpose()
transmissivity_array_proper = np.sqrt(trans_array_proper)

freq_THz_1 = np.linspace(min_freq - (max_freq - min_freq)/(2*num_freqs), max_freq + (max_freq - min_freq)/(2*num_freqs), num_freqs +1)
angle_deg_1 = np.linspace(min_angle - (max_angle- min_angle)/(2*num_angles), max_angle + (max_angle- min_angle)/(2*num_angles), num_angles +1)



fig, ax = plt.subplots()

d = ax.pcolormesh(angle_deg_, freq_THz_, trans_array_proper, cmap = "turbo", shading = "nearest")
cbar = plt.colorbar(d, ticks = np.linspace(0,1,6))
d.set_clim(0,1)
plt.xlabel("Angle of Incidence (\u00b0)")
plt.ylabel("Frequency (THz)")
plt.title("$T_{pp}(f,\\theta)$")

fig.savefig(f"{path}full_result.png")

fig1, ax1 = plt.subplots()

d1 = ax1.pcolormesh(angle_deg_, freq_THz_, transmissivity_array_proper, cmap = "turbo", shading = "nearest")
cbar1 = plt.colorbar(d1, ticks = np.linspace(0,1,6))
d1.set_clim(0,1)
plt.xlabel("Angle of Incidence (\u00b0)")
plt.ylabel("Frequency (THz)")
if is_s:
    plt.title("$|t_{ss}(f,\\theta)|$")
else:
    plt.title("$|t_{pp}(f,\\theta)|$")

fig1.savefig(f"{path}full_transmissivity_result.png")

fig2, ax2 = plt.subplots()

d2 = ax2.pcolormesh(angle_deg_, freq_THz_, transmissivity_array_proper, cmap = "jet", shading = "nearest")
cbar2 = plt.colorbar(d2, ticks = np.linspace(0,1,6))
d2.set_clim(0,1)
plt.xlabel("Angle of Incidence (\u00b0)")
plt.ylabel("Frequency (THz)")
if is_s:
    plt.title("$|t_{ss}(f,\\theta)|$")
else:
    plt.title("$|t_{pp}(f,\\theta)|$")

fig2.savefig(f"{path}full_transmissivity_result_bad-color.png")