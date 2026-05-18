import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import glob

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())
    
angle_deg_ = np.linspace(0, 20, 1)
freq_THz_ = np.linspace(220, 290, 20)
    
args = expand_grid({
    "angle": angle_deg_, 
    "freq": freq_THz_
    })

files = glob.glob("results_med/*.csv")
                  
print(len(files))

results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True).set_axis(["angle", "freq", "trans"], axis = 1)

expanded_results = args.set_index(["angle", "freq"]).join(results.set_index(["angle", "freq"]))

data_pivot = results.pivot(
    index = "freq",
    columns = "angle"
)
    
ooga = data_pivot.to_numpy()

fig, ax = plt.subplots()
c = ax.pcolor(ooga, cmap = "jet", clim = (0,1))
cbar = plt.colorbar(c, ticks = np.linspace(0,1,6))


plt.savefig("results_med/full_result.png")