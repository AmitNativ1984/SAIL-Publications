"""Record the PopSAN encoder over a play rollout and save the raw trace instead of plotting it.

Run inside the aerial_gym_docker devcontainer from /workspaces/aerial_gym_docker:
  python trace_dump.py <out.npz> --task=f450_navigation_task --file=<run>/config.yaml \
      --play --plot-encoding --checkpoint=<run>/nn/<ckpt>.pth --headless=True \
      --curriculum_level=30 --max_episodes=10
"""
import isaacgym  # noqa: F401
import sys
import numpy as np
import torch

OUT = sys.argv.pop(1)
import rl_training.rl_games.tools.plot_encoder_trace as pet


def dump(encoder, trace, layout, save_dir=None):
    np.savez_compressed(
        OUT,
        obs=torch.cat([t["obs"] for t in trace]).numpy(),
        spikes=torch.cat([t["pop_spikes"] for t in trace]).numpy().astype(np.uint8),
        means=encoder.means.detach().cpu().numpy().squeeze(0),
        stds=torch.exp(encoder.log_stds).detach().cpu().numpy().squeeze(0),
        bounds=encoder.obs_bounds.detach().cpu().numpy(),
        layout=np.array([(s.start, s.stop, n) for s, n in layout], dtype=object),
    )
    print("[dump] wrote", OUT, len(trace), "steps")


# runner imports the plot helper at call time, so patching the module attribute suffices
pet.plot_encoder_trace = dump
from rl_training.rl_games import runner

runner.main()
