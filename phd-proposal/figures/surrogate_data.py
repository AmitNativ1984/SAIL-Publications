"""Compute surrogate spike functions and derivatives (float64) -> surrogate_data.dat.

x = U - U_th. Forms match Eq. (eq:surrogates); the forward functions are their antiderivatives.
"""
import sys
from pathlib import Path

import numpy as np

ALPHA, K = 2.0, 4.0
x = np.linspace(-4.0, 4.0, 801)

s_atan = 0.5 + np.arctan(np.pi * ALPHA / 2 * x) / np.pi
s_sig = 1.0 / (1.0 + np.exp(-K * x))
d_atan = (ALPHA / 2) / (1.0 + (np.pi * ALPHA / 2 * x) ** 2)
d_sig = K * np.exp(-K * x) / (1.0 + np.exp(-K * x)) ** 2

out = Path(__file__).with_name("surrogate_data.dat")
np.savetxt(out, np.column_stack([x, s_atan, s_sig, d_atan, d_sig]),
           header="x s_atan s_sig d_atan d_sig", comments="", fmt="%.10f")

if "--check" in sys.argv:
    h = x[1] - x[0]
    for name, s, d in [("atan", s_atan, d_atan), ("sig", s_sig, d_sig)]:
        err = np.max(np.abs(np.gradient(s, h, edge_order=2) - d))
        area = np.sum((d[1:] + d[:-1]) / 2) * h
        print(f"{name:5s} max|dS_num - dS_formula| = {err:.2e}   S(0) = {s[400]:.6f}   "
              f"peak = {d.max():.6f}   integral of dS on [-4,4] = {area:.6f}   "
              f"S(4)-S(-4) = {s[-1] - s[0]:.6f}")
