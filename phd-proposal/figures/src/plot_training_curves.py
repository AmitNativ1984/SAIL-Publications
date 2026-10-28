"""Training-curve figures for the preliminary-results section, from wandb history CSVs.

Usage: python plot_training_curves.py <csv_dir> <out_dir>
CSV names are <wandb_project>__<run_id>.csv (see fetch_wandb.py).
"""
import sys, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV, OUT = sys.argv[1], sys.argv[2]
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "legend.fontsize": 7,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.4,
    "legend.frameon": False, "savefig.bbox": "tight", "savefig.dpi": 300, "pdf.fonttype": 42,
})


def load(name):
    return pd.read_csv(os.path.join(CSV, name + ".csv"))


def series(d, key, x="epoch"):
    s = d[[x, key]].dropna()
    return s[x].to_numpy(), s[key].to_numpy()


def smooth(y, w):
    return pd.Series(y).rolling(w, min_periods=1, center=True).mean().to_numpy()


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"))
    fig.savefig(os.path.join(OUT, name + ".png"))
    plt.close(fig)


# 1. Curriculum progress from scratch: the fastest ANN run vs the best PopSAN run, same (old) env
#    and reward (commits 0c4a807 / a7e4157 differ only in checkpoint upload and run naming).
def old_run(proj, rid):
    d = load(f"{proj}__{rid}")
    s = d[["_step", "curriculum_level/iter"]].dropna()
    # tensorboard-synced runs: _step is the shared log counter; both runs are 1000 PPO epochs
    return 1000 * s["_step"] / d["_step"].max(), s["curriculum_level/iter"]

fig, ax = plt.subplots(figsize=(3.4, 2.0))
for (proj, rid), c, lab in [(("nav_vae_ann", "2gusa9bs"), BLUE, "ANN"),
                            (("nav_popsan_new_reward", "zefha2dc"), ORANGE, "PopSAN")]:
    x, y = old_run(proj, rid)
    ax.plot(x, y, color=c, label=lab)
ax.set_xlabel("PPO epoch")
ax.set_ylabel("Curriculum level")
ax.set_ylim(-0.5, 26.5); ax.set_xlim(0, 1000)
ax.legend(loc="lower right")
save(fig, "scratch_curriculum")

# reference for the distillation figure: the distillation teacher's level-30 training success
b = load("f450_navigation_task__9c53czrl")

# 3. Distillation: adaptive vs constant LR after the teacher term is released.
runs = [("wavp4w4j", ORANGE, "adaptive LR"), ("bcqeahgz", BLUE, r"constant LR $10^{-4}$")]
teacher_succ = b["success_rate"].dropna().tail(50).mean()
fig, axs = plt.subplots(3, 1, figsize=(3.4, 4.2), sharex=True)
for rid, c, lab in runs:
    d = load(f"popsan_ann_teacher_distillation__{rid}")
    x, y = series(d, "success_rate"); axs[0].plot(x, smooth(y, 9), color=c, label=lab)
    x, y = series(d, "info/last_lr"); axs[1].plot(x, y, color=c)
    x, y = series(d, "losses/entropy"); axs[2].plot(x, smooth(y, 9), color=c)
    xk, k = series(d, "distill/kd_actor_coeff_eff")
    rel = xk[(k <= 0)].min()
    for ax in axs:
        ax.axvline(rel, color=c, lw=0.8, ls=":")
axs[0].axhline(teacher_succ, color=MUTED, lw=0.8, ls="--")
axs[0].text(1990, teacher_succ + 0.02, "ANN teacher", color=MUTED, fontsize=7, ha="right")
axs[0].set_ylabel("Success rate"); axs[0].set_ylim(0, 1)
axs[0].legend(loc="lower right")
axs[1].set_yscale("log"); axs[1].set_ylabel("Learning rate")
axs[2].set_ylabel("Policy entropy"); axs[2].set_xlabel("PPO epoch")
axs[1].text(1950, 2e-6, "dotted: teacher term released", color=MUTED, fontsize=7, ha="right", va="bottom")
axs[2].set_xlim(0, 2000)
save(fig, "distill_stability")
print("ok")
