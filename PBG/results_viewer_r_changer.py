import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import glob
import sys

path = sys.argv[1]

files = glob.glob(f"{path}raw/*.csv")
                  
print(len(files))

results = pd.DataFrame()

results = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


results_2 = results.sort_values(by = ["r"])

fig, ax = plt.subplots(4)

ax[0].plot(results_2["r"], results_2["omega"])
ax[1].plot(results_2["r"], results_2["a"])
ax[2].plot(results_2["r"], results_2["b"])
ax[3].plot(results_2["r"], results_2["aniso"])
plt.xlabel("Pillar Radius (\u03bcm)")
ax[0].set_ylabel("omega")
ax[1].set_ylabel("a")
ax[2].set_ylabel("b")
ax[3].set_ylabel("aniso")

fig.savefig(f"{path}full_result.png")
