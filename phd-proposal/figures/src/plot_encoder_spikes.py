"""Encoder-bounds, learned-receptive-field and spike-rate figures from a PopSAN spike dump.

Usage: python plot_encoder_spikes.py <prefix> <out_dir>
<prefix>_dump.pt and <prefix>_report.json come from spike_dump.py (a measure_spikes.py
rollout that also saves normalised observations, per-neuron spike counts and the encoder).
"""
import json, math, os, sys
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PREFIX, OUT = sys.argv[1], sys.argv[2]
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID, HIST = "#0b0b0b", "#52514e", "#e4e3df", "#c9c8c2"
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "legend.fontsize": 7,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.0,
    "legend.frameon": False, "savefig.bbox": "tight", "savefig.dpi": 300,
})
T, THRESH, POP = 5, 0.95, 10
A_MIN = THRESH / T  # constant current needed to fire within the window
NAMES = (["dir_x", "dir_y", "dir_z", "distance", "v_x", "v_y", "v_z", "w_x", "w_y", "w_z",
          "g_x", "g_y", "g_z", "a_f", "a_phi", "a_theta", "a_psidot"]
         + [f"z_{k}" for k in range(32)])

d = torch.load(PREFIX + "_dump.pt")
rep = json.load(open(PREFIX + "_report.json"))
obs = d["obs"].float().numpy()            # [N, 49], normalised as the encoder sees it
bounds = d["obs_bounds"].numpy()          # [49, 2] percentile bounds
mu_l, sd_l = d["means"].numpy(), d["stds"].numpy()  # learned [49, 10]


def init_fields(lo, hi):
    mu = lo[:, None] + np.linspace(0, 1, POP)[None] * (hi - lo)[:, None]
    return mu, np.repeat((0.75 * (mu[:, 1] - mu[:, 0]))[:, None], POP, 1)


def fires(x, lo, hi, mu, sd):
    """[N, 49, 10] bool: neuron reaches threshold within T steps for clipped observation x."""
    xc = np.clip(x, lo, hi)[:, :, None]
    return np.exp(-0.5 * ((xc - mu[None]) / sd[None]) ** 2) >= A_MIN


sym_lo, sym_hi = np.full(49, -3.0), np.full(49, 3.0)
pct_lo, pct_hi = bounds[:, 0], bounds[:, 1]
stats = {}
for name, lo, hi in [("symmetric", sym_lo, sym_hi), ("percentile", pct_lo, pct_hi)]:
    mu, sd = init_fields(lo, hi)
    active = np.zeros((49, POP), bool)
    for k in range(0, len(obs), 20000):
        active |= fires(obs[k:k + 20000], lo, hi, mu, sd).any(0)
    stats[name] = {"silent": int((~active).sum()), "total": active.size,
                   "silent_state": int((~active[:17]).sum()), "silent_latent": int((~active[17:]).sum())}
mu, sd = mu_l, sd_l
active = np.zeros((49, POP), bool)
for k in range(0, len(obs), 20000):
    active |= fires(obs[k:k + 20000], pct_lo, pct_hi, mu, sd).any(0)
stats["learned"] = {"silent": int((~active).sum()), "total": active.size}


def gauss(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2)


def field_panel(ax, i, mu, sd, lo, hi, color, title):
    x = np.linspace(-5, 5, 800)
    h, e = np.histogram(obs[:, i], bins=60, range=(-5, 5))
    ax.bar(e[:-1], h / h.max(), width=e[1] - e[0], align="edge", color=HIST, lw=0)
    for j in range(POP):
        silent = not (gauss(np.clip(obs[:, i], lo, hi), mu[j], sd[j]) >= A_MIN).any()
        ax.plot(x, gauss(x, mu[j], sd[j]), color=MUTED if silent else color,
                ls=":" if silent else "-", lw=0.9)
    ax.axvline(lo, color=INK, lw=0.6, ls="--"); ax.axvline(hi, color=INK, lw=0.6, ls="--")
    ax.set_title(title, loc="left"); ax.set_ylim(0, 1.05); ax.set_xlim(-4, 4)
    ax.grid(False)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png")); plt.close(fig)


# 1. Initial fields: symmetric +/-3 vs percentile bounds, on a skewed and a symmetric dimension.
dims = [(0, "goal direction, $x$"), (12, "gravity, body $z$")]
fig, axs = plt.subplots(2, 2, figsize=(6.3, 3.2), sharey=True, sharex=True)
fig.subplots_adjust(hspace=0.35)
for r, (i, nm) in enumerate(dims):
    for c, (lo, hi, col, lab) in enumerate([(-3.0, 3.0, ORANGE, r"symmetric $\pm 3$"),
                                             (pct_lo[i], pct_hi[i], BLUE, "1st--99th percentile")]):
        m, s = init_fields(np.array([lo]), np.array([hi]))
        field_panel(axs[r, c], i, m[0], s[0], lo, hi, col, f"{nm}: {lab}")
for ax in axs[-1]:
    ax.set_xlabel("normalised observation")
for ax in axs[:, 0]:
    ax.set_ylabel("response $A$")
save(fig, "encoder_bounds")

# 2. Learned fields on the same dimensions.
fig, axs = plt.subplots(1, 2, figsize=(6.3, 1.6), sharey=True)
for c, (i, nm) in enumerate(dims):
    field_panel(axs[c], i, mu_l[i], sd_l[i], pct_lo[i], pct_hi[i], AQUA, f"{nm}: learned")
    axs[c].set_xlabel("normalised observation")
axs[0].set_ylabel("response $A$")
save(fig, "encoder_learned")

# 3. Per-neuron firing rate (spikes per neuron per time step) for each layer.
samples = d["samples"]
layers = [("encoder", "Encoder (490)"), ("lif1", "Hidden 1 (256)"), ("lif2", "Hidden 2 (256)"),
          ("lif3", "Output (40)")]
fig, axs = plt.subplots(1, 4, figsize=(6.3, 1.7), sharey=False)
fig.subplots_adjust(wspace=0.4)
rates = {}
for ax, (k, lab) in zip(axs, layers):
    fr = d["per_neuron"][k].numpy() / (samples * T)
    rates[k] = {"mean": float(fr.mean()), "silent": float((fr == 0).mean()),
                "saturated": float((fr >= 0.99).mean())}
    ax.hist(fr, bins=np.linspace(0, 1, 21), color=BLUE, edgecolor="white", linewidth=0.5)
    ax.axvline(fr.mean(), color=ORANGE, lw=1.0)
    ax.set_title(lab, loc="left"); ax.set_xlabel("firing rate"); ax.set_xlim(0, 1)
axs[0].set_ylabel("neurons")
save(fig, "spike_rates")

json.dump({"silent": stats, "rates": rates}, open(os.path.join(OUT, "encoder_spike_stats.json"), "w"), indent=1)
print(json.dumps({"silent": stats, "rates": rates}, indent=1))
