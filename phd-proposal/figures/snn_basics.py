"""LIF neuron response and rate/latency spike encodings -> LIF_neuron.pdf, rate_encoding.pdf, latency_encoding.pdf.

LIF follows the Lapicque model of snnTorch tutorial 1 (R=5, C=5 mF, dt=1 ms, threshold 1, reset by subtraction).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Computer Modern via mathtext; text.usetex would need cm-super (type1ec.sty), not installed here.
plt.rcParams.update({"mathtext.fontset": "cm", "font.family": "serif", "font.serif": ["cmr10"],
                     "axes.formatter.use_mathtext": True, "font.size": 9, "axes.linewidth": 0.6})
OUT = Path(__file__).parent


def save(fig, name, tight=True):
    kw = dict(bbox_inches="tight", pad_inches=0.02) if tight else {}
    fig.savefig(OUT / f"{name}.pdf", **kw)
    fig.savefig(OUT / f"{name}.png", dpi=200, **kw)


# LIF neuron
T, onset, I_in, R, tau, thr = 200, 10, 0.3, 5.0, 25.0, 1.0
I = np.where(np.arange(T) >= onset, I_in, 0.0)
U, S, u = np.zeros(T), np.zeros(T), 0.0
for t in range(T):
    u = u + (-u + I[t] * R) / tau
    S[t] = u >= thr
    U[t] = u
    u -= S[t] * thr

fig, ax = plt.subplots(3, 1, figsize=(6.0, 1.9), sharex=True, gridspec_kw={"height_ratios": [1, 2, 0.45]})
ax[0].plot(I, "C3")
ax[0].set_ylim(-0.02, 0.4)
ax[0].set_ylabel(r"$I_{in}$")
ax[1].plot(U, "C0")
ax[1].axhline(thr, color="k", ls="--", lw=0.8)
ax[1].text(T + 2, thr, r"$\Theta$", va="center")
ax[1].set_ylabel(r"$U[t]$")
ax[2].eventplot(np.flatnonzero(S), colors="k", lineoffsets=0, linelengths=0.8, linewidths=1)
ax[2].set_yticks([])
ax[2].set_ylabel(r"$S_{out}$", rotation=0, ha="right", va="center")
ax[2].set_xlabel("Time step")
ax[2].set_xlim(0, T)
fig.align_ylabels(ax)
fig.tight_layout(h_pad=0.3)
save(fig, "LIF_neuron")

# Encodings: identical figure size and axes rect so (a) and (b) have the same plot height side by side.
FIGSIZE, RECT, STEPS = (3.2, 1.7), [0.2, 0.25, 0.77, 0.72], 50


def raster(trains, labels, name):
    fig = plt.figure(figsize=FIGSIZE)
    a = fig.add_axes(RECT)
    for i, train in enumerate(trains):
        a.eventplot(np.flatnonzero(train), lineoffsets=len(trains) - 1 - i, linelengths=0.5, colors="k", linewidths=0.8)
    a.set_yticks(range(len(trains))[::-1], labels)
    a.set_ylim(-0.6, len(trains) - 0.4)
    a.set_xlim(-1, STEPS)
    a.set_xlabel("Time step")
    save(fig, name, tight=False)


rng = np.random.default_rng(0)
x_rate = [0.95, 0.70, 0.40, 0.10]
raster([rng.random(STEPS) < x for x in x_rate], [f"$x={x:.2f}$" for x in x_rate], "rate_encoding")

x_lat = np.linspace(1.0, 0.05, 8)
latency = [np.arange(STEPS) == round((1 - x) * (STEPS - 1)) for x in x_lat]
raster(latency, [f"$x={x:.2f}$" for x in x_lat], "latency_encoding")
