"""Heaviside spike function vs. arctan surrogate and its derivative -> surrogate_gradients.pdf.

x = U - U_th. Derivative matches Eq. (eq:surrogates).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-4.0, 4.0, 801)

s_atan = 0.5 + np.arctan(np.pi * x) / np.pi
d_atan = 1.0 / (1.0 + (np.pi * x) ** 2)

# Computer Modern via mathtext; text.usetex would need cm-super (type1ec.sty), not installed here.
plt.rcParams.update({"mathtext.fontset": "cm", "font.family": "serif", "font.serif": ["cmr10"],
                     "axes.formatter.use_mathtext": True, "font.size": 9,
                     "legend.fontsize": 8.5, "axes.linewidth": 0.6})

fig, ax = plt.subplots(1, 2, figsize=(6.7, 2.5))
ax[0].plot(x, s_atan, label=r"$\tilde{S}$")
ax[0].step(x, (x >= 0).astype(float), "k", where="post", label=r"$H(U-U_{th})$")
ax[0].set_ylabel(r"$S$")

ax[1].plot(x, d_atan, label=r"$\partial\tilde{S}/\partial U$")
ax[1].plot(x, 0 * x, "k", label=r"$\partial H/\partial U$")
ax[1].annotate("", xy=(0, 1.42), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.5, color="k"))
ax[1].text(0.12, 1.36, r"$\delta(U-U_{th})$")
ax[1].set_ylim(-0.1, 1.55)
ax[1].set_ylabel(r"$\partial S/\partial U$")

for a, tag in zip(ax, "ab"):
    a.grid(alpha=0.3)
    a.legend(loc="upper left")
    a.set_xlabel(r"$U-U_{th}$")
    a.set_title(f"({tag})", y=-0.48)

fig.tight_layout()
fig.savefig(Path(__file__).with_name("surrogate_gradients.pdf"), bbox_inches="tight", pad_inches=0.02)
fig.savefig(Path(__file__).with_name("surrogate_gradients.png"), dpi=200, bbox_inches="tight", pad_inches=0.02)
