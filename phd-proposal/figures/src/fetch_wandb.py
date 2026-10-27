"""Download the wandb histories behind plot_training_curves.py into <out_dir>/<project>__<run>.csv.

Run inside the aerial_gym_docker devcontainer (needs wandb, pandas, WANDB_API_KEY), not from
a directory containing a ./wandb folder, which shadows the package.
"""
import os, sys
import pandas as pd
import wandb

RUNS = {
    # ANN teacher: p_fov from scratch -> latency fine-tune at level 30 (the distillation teacher)
    "f450_navigation_task": ["xfm0jyko", "9c53czrl"],
    # PopSAN distillation from f450_nav_lat_pfov
    "popsan_ann_teacher_distillation": ["wavp4w4j", "5ni6sidx", "4fppa7eo", "uo90s38c", "wig5qvuk",
                                        "j5skxllu", "tkr6ithi", "bcqeahgz", "k75v1cks"],
    # from-scratch PPO, old environment (May-June 2026): ANN vs PopSAN
    "nav_vae_ann": ["2gusa9bs", "2mjqfv6u", "guyrtybs", "5mztw271", "bqptu3yz"],
    "nav_popsan": ["fzrjwq2x", "270lli8h"],
    "nav_popsan_new_reward": ["zefha2dc", "bkdg555f", "h50ol459", "5dswmowe"],
}
KEYS = ("success_rate", "crash_rate", "curriculum_level", "epoch", "frame", "info/last_lr",
        "losses/entropy", "distill/kd_actor_coeff_eff", "reward/")

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
api = wandb.Api(timeout=300)
for proj, ids in RUNS.items():
    for rid in ids:
        r = api.run(f"{api.default_entity}/{proj}/{rid}")
        keys = [k for k in r.summary.keys() if k.startswith(KEYS) and "face" not in k]
        # one key per call: a multi-key history() drops rows where any key is missing
        dfs = [h.set_index("_step")[[k]] for k in keys
               if len(h := r.history(keys=[k], samples=3000, pandas=True))]
        df = pd.concat(dfs, axis=1).sort_index() if dfs else pd.DataFrame()
        df.to_csv(os.path.join(out, f"{proj}__{rid}.csv"))
        print(proj, rid, r.name, df.shape)
