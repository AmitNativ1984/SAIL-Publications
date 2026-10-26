"""Gaussian receptive fields panel of the population-coding figure -> population_rf.png.

Matches the 1189 px width of population_spikes_{neg,pos}.png; height equals the two stacked rasters.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mus, sigma, xs = np.linspace(-1, 1, 5), 0.35, (-0.3, 0.3)
grid = np.linspace(-1.5, 1.5, 600)

fig, ax = plt.subplots(figsize=(11.89, 6.13), dpi=100)
for i, mu in enumerate(mus):
    ax.plot(grid, np.exp(-(grid - mu) ** 2 / (2 * sigma**2)), lw=2, label=f"neuron {i} (μ={mu:+.1f})")
for x, ls in zip(xs, ("--", "-.")):
    ax.plot([x, x], [0, 1.15], "k", ls=ls, lw=1.5)
    ax.text(x + 0.03, 1.05, f"x = {x:+.2f}" if x > 0 else f"x = {x:.2f}", fontsize=11)
    for i, mu in enumerate(mus):
        ax.plot(x, np.exp(-(x - mu) ** 2 / (2 * sigma**2)), "o", color=f"C{i}", mec="k", ms=8, zorder=3)
ax.set(xlim=(-1.5, 1.5), ylim=(0, 1.3), xlabel="Stimulus value", ylabel="Activation (spike prob.)",
       title="Gaussian receptive fields")
ax.legend(loc="upper center", ncol=5, fontsize=8)
fig.tight_layout()
fig.savefig(Path(__file__).parent / "population_rf.png")
