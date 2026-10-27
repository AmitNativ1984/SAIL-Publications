"""measure_spikes.py's rollout, also saving normalised observations, per-neuron spike counts
and the encoder's receptive fields. usage: spike_dump.py <popsan.pth> <level> <teacher.pth> <out_prefix>"""
import isaacgym  # noqa: F401
import json, os, sys
sys.path.insert(0, "/workspaces/aerial_gym_docker/analysis")
sys.path.insert(0, "/workspaces/aerial_gym_docker")
import torch
import config  # noqa: F401
from aerial_gym.registry.task_registry import task_registry
from measure_spikes import load_popsan
from crash_cause_eval import build_actor, _NORM_CLAMP
from spike_ops import SpikeCounter, format_report, linear_macs

ckpt, level, teacher, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
num_envs, num_steps = 128, 2000
dev = "cuda:0"
net, mean, std = load_popsan(ckpt, dev)
aw = torch.load(teacher, map_location="cpu", weights_only=False)["model"]
ann_macs = linear_macs(build_actor(aw)[0])

from config.task_config import F450NavTaskConfig
F450NavTaskConfig.curriculum.min_level = level
F450NavTaskConfig.curriculum.max_level = level
task = task_registry.make_task("f450_navigation_task", num_envs=num_envs, headless=True, use_warp=True)

counter = SpikeCounter(net)
arrivals = episodes = 0
obs_log = []
obs = task.reset()[0]["observations"]
with torch.no_grad():
    for s in range(num_steps):
        o_n = torch.clamp((obs - mean) / std, -_NORM_CLAMP, _NORM_CLAMP)
        if s % 4 == 0:
            obs_log.append(o_n.cpu())
        mu = net({"obs": o_n})[0]
        o, _, term, trunc, infos = task.step(mu.clamp(-1, 1))
        obs = o["observations"]
        arrivals += int(infos["arrivals"].bool().sum())
        episodes += int((term.bool() | trunc.bool()).sum())
        if (s + 1) % 250 == 0:
            print(f"step {s+1}/{num_steps} episodes {episodes} success {100*arrivals/max(episodes,1):.1f}%", flush=True)

report = counter.report(ann_macs)
report.update({"checkpoint": ckpt, "ann_checkpoint": teacher, "level": level, "episodes": episodes,
               "success_rate": arrivals / max(episodes, 1), "num_envs": num_envs, "num_steps": num_steps})
print(format_report(report))
json.dump(report, open(out + "_report.json", "w"), indent=1)
enc = net.pop_encoder
torch.save({
    "obs": torch.cat(obs_log).half(),
    "per_neuron": {k: t.per_neuron.cpu() for k, t in counter.tallies.items()} if hasattr(counter, "tallies") else None,
    "samples": getattr(counter, "samples", None),
    "obs_bounds": enc.obs_bounds.cpu(),
    "means": enc.means.detach().cpu().squeeze(0),
    "stds": torch.exp(enc.log_stds.detach().cpu()).squeeze(0),
}, out + "_dump.pt")
print("wrote", out)
task.close()
