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

fig, ax = plt.subplots(1,3)
fig.set_size_inches(16,9)
fig.subplots_adjust(wspace = 0.5)

size = 1

s0=ax[0].scatter(results_2["r"], results_2["omega"], c=results_2["a"], s=size, norm = "log")
s1=ax[1].scatter(results_2["r"], results_2["omega"], c=results_2["b"], s=size, norm = "log")
s2=ax[2].scatter(results_2["r"], results_2["omega"], c=results_2["aniso"], s=size, norm = "log")
fig.supxlabel("Pillar Radius (\u03bcm)")
fig.supylabel("Center Freq (2\u03c0c/a)")
ax[0].set_title("a")
ax[1].set_title("b")
ax[2].set_title("aniso")
ax[0].set_xlim(0.05,0.5)
ax[1].set_xlim(0.05,0.5)
ax[2].set_xlim(0.05,0.5)
fig.colorbar(s0, ax=ax[0])
fig.colorbar(s1, ax=ax[1])
fig.colorbar(s2, ax=ax[2])

fig.savefig(f"{path}full_result.png")
