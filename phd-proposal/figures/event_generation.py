"""Event generation figure -> event_generation.pdf.

Adapted from ../../event-cameras-overview/make_figures.py (fig_generation); panel (b) shows a
white square on a rotating gray disk instead of a rotating dot.
"""
from pathlib import Path

import matplotlib as mpl

mpl.use("pgf")
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

OUT = Path(__file__).parent

ON, OFF = "#e34948", "#2a78d6"
INK, INK2, RULE = "#0b0b0b", "#52514e", "#d9d8d4"

mpl.rcParams.update({
    "pgf.texsystem": "pdflatex", "pgf.rcfonts": False,
    "pgf.preamble": r"\usepackage{amsmath,bm}",
    "font.family": "serif",
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "axes.linewidth": 0.6,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.labelcolor": INK,
    "ytick.labelcolor": INK, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "legend.frameon": False, "legend.fontsize": 8,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
TEXTWIDTH = 6.7  # inches, A4 with 2 cm margins


def simulate(render, T, n_steps, C=0.2, eps=1e-3, ref_offset=0.0):
    """Ideal event camera: a pixel fires each time its log intensity moves C away
    from the level of its last event; timestamps are linearly interpolated."""
    ts = np.linspace(0.0, T, n_steps + 1)
    L_prev = np.log(render(ts[0]) + eps)
    # an offset keeps the reference levels off the static intensity, where tails would fire late
    L_ref = L_prev + ref_offset * C
    ev = []
    for t0, t1 in zip(ts[:-1], ts[1:]):
        L = np.log(render(t1) + eps)
        for p in (1, -1):
            n = np.floor(p * (L - L_ref) / C).astype(int)
            pix = np.nonzero(n > 0)
            if not pix[0].size:
                continue
            cnt = n[pix]
            rep = [np.repeat(a, cnt) for a in pix]
            k = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt) + 1
            level = L_ref[tuple(rep)] + p * k * C
            a, b = L_prev[tuple(rep)], L[tuple(rep)]
            t = t0 + (level - a) / (b - a) * (t1 - t0)
            ev.append(np.stack([rep[-1], rep[0], t, np.full(t.size, p)], 1))
            L_ref[pix] += p * cnt * C
        L_prev = L
    ev = np.concatenate(ev)
    return ev[np.argsort(ev[:, 2], kind="stable")]  # columns: x, y, t, p


# disk and square geometry, in pixels of a 64 x 64 sensor
N, CEN, R_DISK, R_SQ, HALF = 64, 32.0, 28.0, 18.0, 4.0
W = 2 * np.pi * 5.0  # rad/s, 5 revolutions per second
GRAY, WHITE = 0.55, 0.95  # disk and square intensity


def disk(t):
    yy, xx = np.mgrid[:N, :N].astype(float)
    # pixel coordinates in the rotating disk frame
    dx, dy = xx - CEN, yy - CEN
    c, s = np.cos(W * t), np.sin(W * t)
    u, v = c * dx + s * dy, -s * dx + c * dy
    d_sq = np.maximum(np.abs(u - R_SQ), np.abs(v)) - HALF
    square = 1 / (1 + np.exp(d_sq / 0.6))
    inside = 1 / (1 + np.exp((np.hypot(dx, dy) - R_DISK) / 0.6))
    return 0.5 * (1 - inside) + inside * (GRAY + (WHITE - GRAY) * square)


def draw_disk(ax3, t_plane=0.0):
    """Stimulus at t = 0 as an image on the t = 0 plane of the space-time plot."""
    n = 160  # finer than the sensor so the disk edge looks round
    g = np.linspace(0, N, n + 1)
    yy, xx = np.meshgrid(g, g, indexing="ij")
    c = (g[:-1] + g[1:]) / 2
    cy, cx = np.meshgrid(c, c, indexing="ij")
    in_disk = np.hypot(cx - CEN, cy - CEN) < R_DISK
    in_sq = np.maximum(np.abs(cx - CEN - R_SQ), np.abs(cy - CEN)) < HALF
    rgba = np.zeros((n, n, 4))
    rgba[..., :3] = np.where(in_sq, WHITE, GRAY)[..., None]
    rgba[..., 3] = in_disk
    ax3.plot_surface(xx, np.full_like(xx, t_plane), yy, facecolors=rgba, rstride=1, cstride=1,
                     shade=False, linewidth=0, antialiased=False, rasterized=True, zorder=0)
    a = np.deg2rad(np.linspace(25, 115, 40))
    rr = R_DISK + 4
    arc = (CEN + rr * np.cos(a), np.full_like(a, t_plane), CEN + rr * np.sin(a))
    ax3.plot(*arc, color=INK2, lw=0.8, zorder=1)
    return arc


def fig_generation():
    T_ms = 100.0
    # slopes (per ms), smoothed into round turns: event rate follows |dL/dt|, sparse to bursts
    knots = [0, 24, 36, 50, 84, T_ms]
    slopes = [0.012, 0.1, -0.15, -0.012, 0.07]
    tg = np.linspace(0, T_ms, 4001)
    slope = gaussian_filter1d(np.array(slopes)[np.searchsorted(knots, tg, side="right").clip(1, len(slopes)) - 1], 160)
    Lg = np.concatenate([[0.0], np.cumsum((slope[1:] + slope[:-1]) / 2 * np.diff(tg))])
    Lfun = lambda t: np.interp(t, tg, Lg)
    C = 0.2
    ev = simulate(lambda t: np.exp(np.atleast_2d(Lfun(t))) - 1e-3, T_ms, 20000, C=C)
    tt = np.linspace(0, T_ms, 2000)

    fig = plt.figure(figsize=(TEXTWIDTH, 1.85))
    ax = fig.add_axes([0.0, 0.2, 0.5, 0.8])
    ax.plot(tt, Lfun(tt), color=INK, lw=1.2)
    ax.text(12, Lfun(12.0) + 0.12, r"$L(\mathbf{x}_0,t)$", color=INK, ha="center", va="bottom")
    # reference level of the pixel: the log intensity at its last event
    t_steps = np.concatenate([[0], ev[:, 2], [T_ms]])
    ref = np.concatenate([[Lfun(0.0)], Lfun(ev[:, 2]), [Lfun(ev[-1, 2])]])
    ax.step(t_steps, ref, where="post", color=INK2, lw=0.7, ls=(0, (3, 2)))
    on, off = ev[ev[:, 3] > 0], ev[ev[:, 3] < 0]
    ax.scatter(on[:, 2], Lfun(on[:, 2]), marker="^", s=22, color=ON, zorder=3,
               edgecolor="white", lw=0.4, label=r"ON event, $p_k=+1$")
    ax.scatter(off[:, 2], Lfun(off[:, 2]), marker="v", s=22, color=OFF, zorder=3,
               edgecolor="white", lw=0.4, label=r"OFF event, $p_k=-1$")
    tf = np.arange(0, T_ms, 1000 / 30)
    ax.scatter(tf, Lfun(tf), marker="s", s=26, facecolor="none", edgecolor=INK,
               lw=0.9, zorder=4, label="frame sample")
    # without noise every event sits on a level L(0) + kC
    for lev in Lfun(0.0) + C * np.arange(np.floor(Lg.min() / C), np.ceil(Lg.max() / C) + 1):
        ax.axhline(lev, color=RULE, lw=0.5, zorder=0)
    lo = Lfun(0.0)
    lo = Lfun(0.0) + C * (np.floor((Lg.max() - Lfun(0.0)) / C) - 1)  # top gap, clear of the curve
    ax.annotate("", xy=(48, lo + C), xytext=(48, lo),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.7, shrinkA=0, shrinkB=0))
    ax.text(49, lo + C / 2, r"$C$", va="center", color=INK)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(r"log intensity $L=\log I$")
    ax.set_xlim(0, T_ms)
    ax.set_ylim(Lg.min() - 0.12, Lg.max() + 0.12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    # event stream on a parallel time axis: ON up, OFF down
    axe = fig.add_axes([0.0, 0.0, 0.5, 0.15], sharex=ax)
    axe.vlines(on[:, 2], 0, 1, color=ON, lw=1.0)
    axe.vlines(off[:, 2], -1, 0, color=OFF, lw=1.0)
    axe.axhline(0, color=INK2, lw=0.6)
    axe.set_ylim(-1.2, 1.2)
    axe.set_yticks([])
    axe.set_ylabel("events", labelpad=6)
    axe.set_xlabel("time")
    for s in ("top", "right", "bottom", "left"):
        axe.spines[s].set_visible(False)
    axe.plot(1, 0, ">", ms=5, color=INK2, transform=axe.get_yaxis_transform(), clip_on=False)
    ax.legend(loc="upper right", fontsize=7, handlelength=1.2, borderaxespad=0.1)
    ax.set_title("(a) Events at one pixel", loc="left")

    # (b) space-time event stream, with the stimulus at t = 0 on the back plane
    ev2 = simulate(disk, 0.3, 1800, C=0.15, ref_offset=0.5)
    rng = np.random.default_rng(0)
    e = ev2[rng.choice(len(ev2), size=min(4000, len(ev2)), replace=False)]
    ax3 = fig.add_axes([0.52, -0.14, 0.53, 1.26], projection="3d", computed_zorder=False)
    arc = draw_disk(ax3)
    ax3.scatter(e[:, 0], e[:, 2] * 1e3, e[:, 1], c=np.where(e[:, 3] > 0, ON, OFF),
                s=0.6, alpha=0.8, depthshade=False, lw=0, rasterized=True, zorder=2)
    ax3.set_xlabel(r"$x$ (px)", labelpad=-8)
    ax3.set_ylabel("time", labelpad=-12)
    ax3.set_zlabel(r"$y$ (px)", labelpad=-9)
    ax3.tick_params(pad=-3, labelsize=7)
    ax3.set_xlim(0, N); ax3.set_zlim(0, N); ax3.set_ylim(300, 0)
    ax3.set_xticks([0, 32, 64]); ax3.set_zticks([0, 32, 64]); ax3.set_yticks([])
    ax3.view_init(elev=18, azim=-62)
    ax3.set_box_aspect((1, 1.9, 1))
    for a in (ax3.xaxis, ax3.yaxis, ax3.zaxis):
        a.pane.set_facecolor("#fcfcfb"); a.pane.set_edgecolor(RULE)
        a._axinfo["grid"].update(color=RULE, linewidth=0.4)

    ax3.text2D(0.02, 0.93, "(b) Events of a white square on a rotating disk", transform=ax3.transAxes,
               fontsize=9, color=INK)
    ax3.scatter([], [], [], color=ON, s=8, label="ON")
    ax3.scatter([], [], [], color=OFF, s=8, label="OFF")
    ax3.legend(loc="upper left", bbox_to_anchor=(0.04, 0.86), markerscale=1.2, fontsize=7)
    # arrowhead on the projected time axis line (drawn from 0 to t_max), only known after a draw
    fig.draw_without_rendering()
    to_fig = ax3.transData + fig.transFigure.inverted()
    p0, p1 = to_fig.transform(np.column_stack(ax3.yaxis.line.get_data()))
    fig.add_artist(FancyArrowPatch(p0, p1 + 0.08 * (p1 - p0), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=9, color=INK2, lw=0.6,
                                   shrinkA=0, shrinkB=0))
    # arrowhead and label for the rotation arc on the disk
    q = to_fig.transform(np.column_stack(proj3d.proj_transform(*arc, ax3.get_proj())[:2]))
    fig.add_artist(FancyArrowPatch(q[-4], q[-1], transform=fig.transFigure, arrowstyle="-|>",
                                   mutation_scale=8, color=INK2, lw=0.8, shrinkA=0, shrinkB=0))
    fig.text(*q[len(q) // 2] + [0.0, 0.03], r"$\omega$", color=INK, ha="center", va="bottom")
    fig.savefig(OUT / "event_generation.pdf")
    fig.savefig(OUT / "event_generation.png", dpi=200)
    print("events:", len(ev), len(ev2))


if __name__ == "__main__":
    fig_generation()
