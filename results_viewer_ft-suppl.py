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
files_4 = glob.glob(f"{path}raw-4/*.csv")
files_5 = glob.glob(f"{path}raw-5/*.csv")
files_6 = glob.glob(f"{path}raw-6/*.csv")
files_7 = glob.glob(f"{path}raw-7/*.csv")
files_8 = glob.glob(f"{path}raw-8/*.csv")
files_9 = glob.glob(f"{path}raw-9/*.csv")

                  
print(len(files))

results = pd.DataFrame()

results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)

if len(files_4) >0:
    results_4=pd.concat([pd.read_csv(f) for f in files_4], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
else:
    results_4 = pd.DataFrame(columns=["angle_deg", "freqs", "trans"])

if len(files_5) >0:
    results_5=pd.concat([pd.read_csv(f) for f in files_5], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
else:
    results_5 = pd.DataFrame(columns=["angle_deg", "freqs", "trans"])

if len(files_6) >0:
    results_6=pd.concat([pd.read_csv(f) for f in files_6], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
else:
    results_6 = pd.DataFrame(columns=["angle_deg", "freqs", "trans"])

if len(files_7) >0:
    results_7=pd.concat([pd.read_csv(f) for f in files_7], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
else:
    results_7 = pd.DataFrame(columns=["angle_deg", "freqs", "trans"])

if len(files_8) >0:
    results_8=pd.concat([pd.read_csv(f) for f in files_8], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
else:
    results_8 = pd.DataFrame(columns=["angle_deg", "freqs", "trans"])

if len(files_9) >0:
    results_9=pd.concat([pd.read_csv(f) for f in files_9], ignore_index=True).set_axis(["angle_deg", "freqs", "trans"], axis = 1)
else:
    results_9 = pd.DataFrame(columns=["angle_deg", "freqs", "trans"])





results["freq_THz"]=np.multiply(results["freqs"],300)

results_4["freq_THz"]=np.multiply(results_4["freqs"],300)
results_5["freq_THz"]=np.multiply(results_5["freqs"],300)
results_6["freq_THz"]=np.multiply(results_6["freqs"],300)
results_7["freq_THz"]=np.multiply(results_7["freqs"],300)
results_8["freq_THz"]=np.multiply(results_8["freqs"],300)
results_9["freq_THz"]=np.multiply(results_9["freqs"],300)


results=results.round(5)

results_4=results_4.round(5)
results_5=results_5.round(5)
results_6=results_6.round(5)
results_7=results_7.round(5)
results_8=results_8.round(5)
results_9=results_9.round(5)


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

'''
results_109 = results.merge(results.merge(results_9, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti", suffixes=None), on=["angle_deg", "freq_THz", "freqs"], how = "outer", suffixes=None)
results_108 = results_109.merge(results_109.merge(results_8, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti", suffixes=None), on=["angle_deg", "freq_THz", "freqs"], how = "outer", suffixes=None)
results_107 = results_108.merge(results_108.merge(results_7, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti", suffixes=None), on=["angle_deg", "freq_THz", "freqs"], how = "outer", suffixes=None)
results_106 = results_107.merge(results_107.merge(results_6, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti", suffixes=None), on=["angle_deg", "freq_THz", "freqs"], how = "outer", suffixes=None)
results_105 = results_106.merge(results_106.merge(results_5, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti", suffixes=None), on=["angle_deg", "freq_THz", "freqs"], how = "outer", suffixes=None)
results_104 = results_105.merge(results_105.merge(results_4, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti", suffixes=None), on=["angle_deg", "freq_THz", "freqs"], how = "outer", suffixes=None)
'''
results_109 = pd.concat([results, results[["angle_deg", "freq_THz", "freqs"]].merge(results_9, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti")])
results_108 = pd.concat([results_109, results_109[["angle_deg", "freq_THz", "freqs"]].merge(results_8, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti")])
results_107 = pd.concat([results_108, results_108[["angle_deg", "freq_THz", "freqs"]].merge(results_7, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti")])
results_106 = pd.concat([results_107, results_107[["angle_deg", "freq_THz", "freqs"]].merge(results_6, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti")])
results_105 = pd.concat([results_106, results_106[["angle_deg", "freq_THz", "freqs"]].merge(results_5, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti")])
results_104 = pd.concat([results_105, results_105[["angle_deg", "freq_THz", "freqs"]].merge(results_4, on=["angle_deg", "freq_THz", "freqs"], how = "right_anti")])


results_test = args.merge(results_104, on=["angle_deg", "freq_THz"], how = "left")



trans_test = results_test["trans"].astype(float)
trans_test_array = np.reshape(np.array(trans_test), (num_angles,num_freqs))

trans_list = results_2["trans"]

trans_empty_list  = trans_list
# trans_array = np.reshape(np.array(trans_list), (num_angles,num_freqs))
trans_array_proper = trans_test_array.transpose()
transmittivity_array_proper = np.sqrt(trans_array_proper)

freq_THz_1 = np.linspace(min_freq - (max_freq - min_freq)/(2*num_freqs), max_freq + (max_freq - min_freq)/(2*num_freqs), num_freqs +1)
angle_deg_1 = np.linspace(min_angle - (max_angle- min_angle)/(2*num_angles), max_angle + (max_angle- min_angle)/(2*num_angles), num_angles +1)

freq_THz_ = np.linspace(min_freq, max_freq, num_freqs)
angle_deg_ = np.linspace(min_angle, max_angle, num_angles)
'''
fig, ax = plt.subplots()

d = ax.pcolormesh(angle_deg_, freq_THz_, trans_array_proper, cmap = "turbo", shading = "nearest")
cbar = plt.colorbar(d, ticks = np.linspace(0,1,6))
d.set_clim(0,1)
plt.xlabel("Angle of Incidence (\u00b0)")
plt.ylabel("Frequency (THz)")
plt.title("$T_{pp}(f,\\theta)$")

fig.savefig(f"{path}full_result.png")
'''
fig1, ax1 = plt.subplots()

d1 = ax1.pcolormesh(angle_deg_, freq_THz_, transmittivity_array_proper, cmap = "turbo", shading = "nearest")
cbar1 = plt.colorbar(d1, ticks = np.linspace(0,1,6))
d1.set_clim(0,1)
plt.xlabel("Angle of Incidence (\u00b0)")
plt.ylabel("Frequency (THz)")
if is_s:
    plt.title("$|t_{ss}(f,\\theta)|$")
else:
    plt.title("$|t_{pp}(f,\\theta)|$")

fig1.savefig(f"{path}full_transmittivity_result-supplementary.png")

