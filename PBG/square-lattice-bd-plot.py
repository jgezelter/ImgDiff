import numpy as np
import glob
import os
import matplotlib.pyplot as plt

path = os.getcwd()

odd_X_files = glob.glob(f"results/260410/band_diagram_blank/raw/odd_X*")
even_X_files = glob.glob(f"results/260410/band_diagram_blank/raw/even_X*")
odd_M_files = glob.glob(f"results/260410/band_diagram_blank/raw/odd_M*")
even_M_files = glob.glob(f"results/260410/band_diagram_blank/raw/even_M*")

odd_X = [[]]
for f in odd_X_files:
    odd_X=np.append(odd_X, np.load(f)[0], axis = 0)
odd_X = odd_X.transpose()

even_X = [[]]
for f in even_X_files:
    even_X=np.append(even_X, np.load(f)[0], axis = 0)
even_X = even_X.transpose()

odd_M = [[]]
for f in odd_M_files:
    odd_M=np.append(odd_M, np.load(f)[0], axis = 0)
odd_M = odd_M.transpose()

even_M = [[]]
for f in even_M_files:
    even_M=np.append(even_M, np.load(f)[0], axis = 0)
even_M = even_M.transpose()

fig,ax=plt.subplots()
ax.plot(odd_X, color = "red", label = r"$\Gamma-X$")
ax.plot(odd_M, color = "blue", label = r"$\Gamma-M$")
ax.set_ylabel("frequency (2\u03c0c/a)")
ax.set_xlabel("|K|")
tick_labs = np.linspace(0,0.5,5)
ax.set_xticks(tick_labs*2)
ax.set_xticklabels(tick_labs)
ax.set_title("Odd Modes")

fig.savefig("results/260410/band_diagram_blank/processed/odd_bd.png")

fig,ax=plt.subplots()
ax.plot(even_X, color = "red", label = r"$\Gamma-X$")
ax.plot(even_M, color = "blue", label = r"$\Gamma-M$")
ax.set_ylabel("frequency (2\u03c0c/a)")
ax.set_xlabel("|K|")
tick_labs = np.linspace(0,0.5,5)
ax.set_xticks(tick_labs*2)
ax.set_xticklabels(tick_labs)
ax.set_title("Even Modes")

fig.savefig("results/260410/band_diagram_blank/processed/even_bd.png")