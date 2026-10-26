"""Figures for the event-camera overview, rendered from events produced by an ideal
event-camera simulator (event generation model of Gallego et al., 2022, Eq. 2)."""
from pathlib import Path

import matplotlib as mpl

mpl.use("pgf")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter, map_coordinates

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

ON, OFF = "#e34948", "#2a78d6"
INK, INK2, RULE = "#0b0b0b", "#52514e", "#d9d8d4"
SEQ = LinearSegmentedColormap.from_list(
    "seq", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
DIV = LinearSegmentedColormap.from_list(
    "div", ["#184f95", OFF, "#f0efec", ON, "#a32d2c"])

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


def simulate(render, T, n_steps, C=0.2, eps=1e-3):
    """Ideal event camera: a pixel fires each time its log intensity moves C away
    from the level of its last event; timestamps are linearly interpolated."""
    ts = np.linspace(0.0, T, n_steps + 1)
    L_prev = np.log(render(ts[0]) + eps)
    L_ref = L_prev.copy()
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


def make_scene(h=130, w=170):
    """Static texture of shapes with soft edges, viewed through a moving window."""
    yy, xx = np.mgrid[:h, :w]
    S = np.full((h, w), 0.25)
    S[(xx - 62) ** 2 + (yy - 58) ** 2 < 10 ** 2] = 0.9
    S[(xx - 115) ** 2 + (yy - 85) ** 2 < 8 ** 2] = 0.05
    S[40:58, 95:113] = 0.65
    S[75:80, 50:90] = 0.8
    S[(yy > 88) & (yy < 112) & (np.abs(xx - 70) < (yy - 88) * 0.6)] = 0.7
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                S[90 + 5 * i:95 + 5 * i, 110 + 5 * j:115 + 5 * j] = 0.8
    return gaussian_filter(S, 0.8)


SENSOR = (72, 96)
V_TRUE = np.array([60.0, 25.0])  # px/s, (vx, vy)
OFFSET = np.array([45.0, 35.0])


def scene_renderer(S):
    yy, xx = np.mgrid[:SENSOR[0], :SENSOR[1]].astype(float)

    def render(t):
        u = xx + OFFSET[0] - V_TRUE[0] * t
        v = yy + OFFSET[1] - V_TRUE[1] * t
        return map_coordinates(S, [v, u], order=1, mode="nearest")
    return render


def style_image_ax(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(RULE)


# Figure 1: event generation ------------------------------------------------------
def fig_generation():
    T_ms = 100.0
    Lfun = lambda t: 0.9 * np.sin(2 * np.pi * t / 70) + 0.3 * np.sin(2 * np.pi * t / 23 + 0.7)
    C = 0.2
    ev = simulate(lambda t: np.exp(np.atleast_2d(Lfun(t))) - 1e-3, T_ms, 20000, C=C)
    tt = np.linspace(0, T_ms, 2000)

    fig = plt.figure(figsize=(TEXTWIDTH, 2.35))
    ax = fig.add_axes([0.0, 0.0, 0.5, 1.0])
    ax.plot(tt, Lfun(tt), color=INK, lw=1.2, label=r"$L(\mathbf{x}_0,t)$")
    # reference level of the pixel: the log intensity at its last event
    t_steps = np.concatenate([[0], ev[:, 2], [T_ms]])
    ref = np.concatenate([[Lfun(0.0)], Lfun(ev[:, 2]), [Lfun(ev[-1, 2])]])
    ax.step(t_steps, ref, where="post", color=INK2, lw=0.7, ls=(0, (3, 2)),
            label="level at last event")
    on, off = ev[ev[:, 3] > 0], ev[ev[:, 3] < 0]
    ax.scatter(on[:, 2], Lfun(on[:, 2]), marker="^", s=22, color=ON, zorder=3,
               edgecolor="white", lw=0.4, label=r"ON event, $p_k=+1$")
    ax.scatter(off[:, 2], Lfun(off[:, 2]), marker="v", s=22, color=OFF, zorder=3,
               edgecolor="white", lw=0.4, label=r"OFF event, $p_k=-1$")
    tf = np.arange(0, T_ms, 1000 / 30)
    ax.scatter(tf, Lfun(tf), marker="s", s=26, facecolor="none", edgecolor=INK,
               lw=0.9, zorder=4, label="frame at 30 fps")
    # without noise every event sits on a level L(0) + kC
    for lev in Lfun(0.0) + C * np.arange(-7, 5):
        ax.axhline(lev, color=RULE, lw=0.5, zorder=0)
    lo = Lfun(0.0)
    ax.annotate("", xy=(12, lo + C), xytext=(12, lo),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.7, shrinkA=0, shrinkB=0))
    ax.text(13, lo + C / 2, r"$C$", va="center", color=INK)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel(r"log intensity $L=\log I$")
    ax.set_xlim(0, T_ms)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="lower left", ncol=1, fontsize=7, handlelength=1.6,
              bbox_to_anchor=(0.0, -0.02))
    ax.set_title("(a) Events at one pixel", loc="left")

    # (b) space-time stream of a rotating dot
    n = 64
    yy, xx = np.mgrid[:n, :n].astype(float)
    w = 2 * np.pi * 5.0

    def dot(t):
        cx, cy = 32 + 18 * np.cos(w * t), 32 + 18 * np.sin(w * t)
        r = np.hypot(xx - cx, yy - cy)
        return 0.15 + 0.75 / (1 + np.exp((r - 5) / 0.6))
    ev2 = simulate(dot, 0.3, 1800, C=0.25)
    rng = np.random.default_rng(0)
    sel = rng.choice(len(ev2), size=min(5000, len(ev2)), replace=False)
    e = ev2[sel]
    ax3 = fig.add_axes([0.53, -0.08, 0.5, 1.16], projection="3d")
    ax3.scatter(e[:, 0], e[:, 2] * 1e3, e[:, 1], c=np.where(e[:, 3] > 0, ON, OFF),
                s=0.6, alpha=0.8, depthshade=False, lw=0, rasterized=True)
    ax3.set_xlabel(r"$x$ (px)", labelpad=-8)
    ax3.set_ylabel("time (ms)", labelpad=-6)
    ax3.set_zlabel(r"$y$ (px)", labelpad=-9)
    ax3.tick_params(pad=-3, labelsize=7)
    ax3.set_xlim(0, 64); ax3.set_zlim(0, 64); ax3.set_ylim(0, 300)
    ax3.set_xticks([0, 32, 64]); ax3.set_zticks([0, 32, 64]); ax3.set_yticks([0, 100, 200, 300])
    ax3.view_init(elev=18, azim=-62)
    ax3.set_box_aspect((1, 1.9, 1))
    for a in (ax3.xaxis, ax3.yaxis, ax3.zaxis):
        a.pane.set_facecolor("#fcfcfb"); a.pane.set_edgecolor(RULE)
        a._axinfo["grid"].update(color=RULE, linewidth=0.4)
    ax3.text2D(0.02, 0.93, "(b) Event stream of a rotating dot", transform=ax3.transAxes,
               fontsize=9, color=INK)
    ax3.scatter([], [], [], color=ON, s=8, label="ON")
    ax3.scatter([], [], [], color=OFF, s=8, label="OFF")
    ax3.legend(loc="upper left", bbox_to_anchor=(0.04, 0.88), markerscale=1.2, fontsize=7)
    fig.savefig(OUT / "event_generation.pdf")
    fig.savefig(OUT / "event_generation.png", dpi=200)
    print("fig1 events:", len(ev), len(ev2))


# Figures 2-4 share one simulated sequence -------------------------------------------
S = make_scene()
EV = simulate(scene_renderer(S), 0.6, 720, C=0.2)
print("scene events:", len(EV))


def accumulate(x, y, w, shape=SENSOR):
    """Bilinear voting of weighted points into an image."""
    H = np.zeros(shape[0] * shape[1])
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    for dx, dy, wt in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)),
                       (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        xi, yi = x0 + dx, y0 + dy
        ok = (xi >= 0) & (xi < shape[1]) & (yi >= 0) & (yi < shape[0])
        H += np.bincount(yi[ok] * shape[1] + xi[ok], weights=(w * wt)[ok],
                         minlength=H.size)
    return H.reshape(shape)


def fig_representations(t0=0.0, t1=0.25, B=5, tau=0.05):
    e = EV[(EV[:, 2] >= t0) & (EV[:, 2] < t1)]
    x, y, t, p = e[:, 0].astype(int), e[:, 1].astype(int), e[:, 2], e[:, 3]
    frame = np.zeros(SENSOR)
    np.add.at(frame, (y, x), p)
    t_last = np.full(SENSOR, -np.inf)
    np.maximum.at(t_last, (y, x), t)
    ts = np.exp(-(t1 - t_last) / tau)
    tn = (B - 1) * (t - t0) / (t1 - t0)
    vox = np.zeros((B,) + SENSOR)
    for b in range(B):
        np.add.at(vox[b], (y, x), p * np.maximum(0, 1 - np.abs(b - tn)))

    fig = plt.figure(figsize=(TEXTWIDTH, 1.55))
    gs = fig.add_gridspec(1, 5, wspace=0.06)
    m = np.percentile(np.abs(frame[frame != 0]), 98)
    ax = fig.add_subplot(gs[0]); style_image_ax(ax)
    ax.imshow(frame, cmap=DIV, vmin=-m, vmax=m, interpolation="nearest")
    ax.set_title("(a) Event frame", loc="left")
    ax = fig.add_subplot(gs[1]); style_image_ax(ax)
    ax.imshow(ts, cmap=SEQ, vmin=0, vmax=1, interpolation="nearest")
    ax.set_title("(b) Time surface", loc="left")
    mv = np.percentile(np.abs(vox[vox != 0]), 98)
    for i, b in enumerate((0, 2, 4)):
        ax = fig.add_subplot(gs[2 + i]); style_image_ax(ax)
        ax.imshow(vox[b], cmap=DIV, vmin=-mv, vmax=mv, interpolation="nearest")
        ax.text(0.97, 0.05, rf"$b={b}$", transform=ax.transAxes, ha="right",
                va="bottom", fontsize=8, color=INK,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
        if i == 0:
            ax.set_title(rf"(c) Voxel grid, $B={B}$ (bins 0, 2, 4)", loc="left")
    fig.savefig(OUT / "event_representations.pdf")
    fig.savefig(OUT / "event_representations.png", dpi=200)


def fig_contrast_max(t0=0.0, t1=0.25):
    e = EV[(EV[:, 2] >= t0) & (EV[:, 2] < t1)]
    x, y, t = e[:, 0], e[:, 1], e[:, 2] - t0
    ones = np.ones_like(x)
    iwe = lambda th: accumulate(x - t * th[0], y - t * th[1], ones)
    vx = np.arange(-20, 141, 2.0)
    vy = np.arange(-55, 106, 2.0)
    F = np.array([[iwe((a, b)).var() for a in vx] for b in vy])
    j, i = np.unravel_index(F.argmax(), F.shape)
    th_star = np.array([vx[i], vy[j]])
    print("theta* =", th_star, "true =", V_TRUE)

    I0, Is = iwe((0.0, 0.0)), iwe(th_star)
    vmax = np.percentile(Is[Is > 0], 99)
    fig = plt.figure(figsize=(TEXTWIDTH, 1.75))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.33, 1.33, 1.25], wspace=0.12)
    for k, (img, title) in enumerate(((I0, r"(a) $H(\mathbf{x};\bm{\theta}=\mathbf{0})$"),
                                      (Is, r"(b) $H(\mathbf{x};\bm{\theta}^{*})$"))):
        ax = fig.add_subplot(gs[k]); style_image_ax(ax)
        ax.imshow(img, cmap=SEQ, vmin=0, vmax=vmax, interpolation="nearest")
        ax.set_title(title, loc="left")
        ax.set_xlabel(rf"$\sigma^2(H)={img.var():.1f}$", labelpad=2)
    ax = fig.add_subplot(gs[2])
    ax.imshow(F, cmap=SEQ, origin="lower", aspect="auto",
              extent=[vx[0] - 1, vx[-1] + 1, vy[0] - 1, vy[-1] + 1])
    ax.plot(0, 0, "o", ms=5, mfc="white", mec=INK, mew=0.8)
    ax.annotate(r"$\mathbf{0}$", (0, 0), xytext=(4, -9), textcoords="offset points",
                fontsize=8, color=INK)
    ax.plot(*th_star, "o", ms=6, mfc=ON, mec="white", mew=0.8)
    ax.annotate(r"$\bm{\theta}^{*}$", th_star, xytext=(5, 4),
                textcoords="offset points", fontsize=8, color="white")
    ax.set_xlabel(r"$v_x$ (px/s)", labelpad=1)
    ax.set_ylabel(r"$v_y$ (px/s)", labelpad=1)
    ax.set_title(r"(c) $f(\bm{\theta})=\sigma^2(H)$", loc="left")
    fig.savefig(OUT / "contrast_maximization.pdf")
    fig.savefig(OUT / "contrast_maximization.png", dpi=200)
    return th_star


def fig_lif(cx=40, cy=30, r=3, dt=2e-3, beta=0.9, w=0.05, theta=1.0):
    sel = (np.abs(EV[:, 0] - cx) <= r) & (np.abs(EV[:, 1] - cy) <= r)
    e = EV[sel]
    steps = int(round(0.6 / dt))
    X = np.histogram(e[:, 2], bins=steps, range=(0, 0.6))[0]
    U, S_out = np.zeros(steps), np.zeros(steps)
    for k in range(steps):
        prev_u = U[k - 1] if k else 0.0
        prev_s = S_out[k - 1] if k else 0.0
        U[k] = beta * prev_u + w * X[k] - prev_s * theta
        S_out[k] = float(U[k] >= theta)
    tk = np.arange(steps) * dt * 1e3

    fig, axs = plt.subplots(3, 1, figsize=(TEXTWIDTH, 2.6), sharex=True,
                            gridspec_kw=dict(height_ratios=[1.3, 1.5, 0.45], hspace=0.4))
    pid = (e[:, 1] - (cy - r)) * (2 * r + 1) + (e[:, 0] - (cx - r))
    for pol, col, lab in ((1, ON, "ON"), (-1, OFF, "OFF")):
        m = e[:, 3] == pol
        axs[0].scatter(e[m, 2] * 1e3, pid[m], s=3, marker="|", color=col, lw=0.8, label=lab)
    axs[0].set_ylabel("pixel", labelpad=2)
    axs[0].set_yticks([])
    axs[0].legend(loc="center", ncol=1, markerscale=3, fontsize=7,
                  bbox_to_anchor=(0.615, 0.5))
    axs[0].set_title(rf"(a) Input events $X[t]$ from a ${2*r+1}\times{2*r+1}$ patch", loc="left",
                     fontsize=8.5, pad=2)
    axs[1].plot(tk, U, color=INK, lw=0.9)
    axs[1].axhline(theta, color=INK2, lw=0.7, ls=(0, (3, 2)))
    axs[1].text(4, theta, r"$\Theta$", ha="left", va="bottom", color=INK)
    axs[1].set_ylabel(r"$U[t]$", labelpad=2)
    axs[1].set_title(r"(b) Membrane potential", loc="left", fontsize=8.5, pad=2)
    spk = tk[S_out > 0]
    axs[2].vlines(spk, 0, 1, color=INK, lw=0.9)
    axs[2].set_yticks([])
    axs[2].set_ylabel(r"$S_{out}$", labelpad=2)
    axs[2].set_xlabel("time (ms)")
    axs[2].set_xlim(0, 600)
    for a in axs:
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    fig.savefig(OUT / "lif_events.pdf")
    fig.savefig(OUT / "lif_events.png", dpi=200)
    print("lif: input events", len(e), "output spikes", int(S_out.sum()))


if __name__ == "__main__":
    fig_generation()
    fig_representations()
    fig_contrast_max()
    fig_lif()
