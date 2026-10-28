"""Receptive fields and spike rasters of the trained encoder, from a trace_dump.py rollout.

Usage: python plot_encoder_trace.py <trace.npz> <out_dir>
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TRACE, OUT = sys.argv[1], sys.argv[2]
BLUE = "#2a78d6"
INK, MUTED, GRID, HIST = "#0b0b0b", "#52514e", "#e4e3df", "#c9c8c2"
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "legend.fontsize": 7,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 1.0, "savefig.bbox": "tight", "savefig.dpi": 300, "pdf.fonttype": 42,
})
d = np.load(TRACE, allow_pickle=True)
obs, spikes, means, stds, bounds = d["obs"], d["spikes"], d["means"], d["stds"], d["bounds"]
POP, T = means.shape[1], spikes.shape[2]
DIMS = [(4, r"$v_x$"), (5, r"$v_y$"), (6, r"$v_z$"),
        (17, r"$z_{t,1}$"), (18, r"$z_{t,2}$"), (19, r"$z_{t,3}$")]
WINDOW = 100  # control steps shown in the rasters

fig, axs = plt.subplots(len(DIMS), 2, figsize=(6.3, 6.4),
                        gridspec_kw={"width_ratios": [1, 1.6], "hspace": 0.7, "wspace": 0.25})
for row, (i, name) in enumerate(DIMS):
    ax, ar = axs[row]
    lo, hi = bounds[i]
    x = np.linspace(lo, hi, 400)
    th = ax.twinx()
    th.hist(obs[:, i], bins=40, range=(lo, hi), color=HIST, edgecolor="none")
    th.set_yticks([]); th.spines["right"].set_visible(False)
    ax.set_zorder(th.get_zorder() + 1); ax.patch.set_visible(False)
    for k in range(POP):
        ax.plot(x, np.exp(-0.5 * (x - means[i, k]) ** 2 / stds[i, k] ** 2), color=BLUE, lw=0.9)
    ax.set_xlim(lo, hi); ax.set_ylim(0, 1.05); ax.set_yticks([0, 1])
    ax.set_ylabel(name, rotation=0, ha="right", va="center", fontsize=9)

    s = spikes[:WINDOW, i * POP:(i + 1) * POP, :]          # [step, neuron, T]
    st, n, k = np.nonzero(s)
    ar.scatter(st + k / T, n, marker="|", s=6, lw=0.6, color=INK)
    ar.set_xlim(0, WINDOW); ar.set_ylim(-0.7, POP - 0.3); ar.set_yticks([0, POP - 1])
    ar.text(1.0, 1.0, f"{s.mean():.0%}", transform=ar.transAxes, ha="right", va="bottom",
            fontsize=7, color=MUTED)
    ax.tick_params(axis="x", labelsize=7)
    if row < len(DIMS) - 1:
        ar.set_xticklabels([])
axs[0, 0].set_title("Receptive fields and observation histogram")
axs[0, 1].set_title("Spike raster")
axs[-1, 0].set_xlabel("Normalised observation")
axs[-1, 1].set_xlabel("Control step")
fig.text(axs[0, 1].get_position().x0 - 0.035, 0.5, "Neuron", rotation=90, va="center", ha="center")
fig.savefig(os.path.join(OUT, "encoder_trace.pdf"))
fig.savefig(os.path.join(OUT, "encoder_trace.png"))
print("ok")
