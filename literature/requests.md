# Literature requests (reviewer → literature agent)

## REQ-20261019-1 · done (see D-1…D-12)
- Need: SNN / neuromorphic policies for quadrotor control or navigation flown on real hardware (Loihi, SpiNNaker, Speck, Akida); closest prior work to Objective 1.
- Why: Preliminary Results claims an attitude-level SNN navigation controller; novelty vs prior SNN drone control is not stated anywhere.
- Source: phd-proposal/phd-proposal.tex:218
- Priority: high

## REQ-20261019-2 · done (see D-13…D-17, D-1, D-4)
- Need: ANN→SNN policy distillation for RL control (PopSAN follow-ups, proximal policy distillation, DAgger-style BC into SNNs); reported student/teacher gaps.
- Why: distillation section has no comparison point for 0.69–0.74 student success; needs a reference gap.
- Source: phd-proposal/phd-proposal.tex:309
- Priority: high

## REQ-20261019-3 · partial (see D-18…D-23, D-40, D-60, D-61; ORACLE name unconfirmed, seeking-in-clutter not found)
- Need: Learned depth-based quadrotor navigation in clutter (Kulkarni & Alexis DCE / ORACLE / seeking-in-clutter, Loquercio et al. "Learning high-speed flight in the wild", Zhang et al. back-to-newton) — success/crash rates and speeds.
- Why: teacher results (87.8% success at level 30) have no external benchmark; "agile" undefined.
- Source: phd-proposal/phd-proposal.tex:229, 262
- Priority: high

## REQ-20261019-4 · done (see D-23…D-26)
- Need: Perception-aware / FOV-aware reward or constraints for learned navigation; discrete-time CBF used as RL reward shaping.
- Why: p_fov and p_cbf are presented as design choices without citation; novelty unclear.
- Source: phd-proposal/phd-proposal.tex:262
- Priority: medium

## REQ-20261019-5 · done (see D-27…D-30, D-21, D-22)
- Need: Memory in RL navigation under limited FOV (recurrent vs frame-stacking vs SNN membrane state); evidence that LIF state acts as memory in control.
- Why: Objective 2 is motivated by an inconclusive GRU result; needs prior evidence the SNN-memory hypothesis is plausible.
- Source: phd-proposal/phd-proposal.tex:288-307
- Priority: medium

## REQ-20261019-6 · done (see D-31…D-35, D-19, D-20)
- Need: Agile autonomous flight SOTA — drone racing (Swift), high-speed flight in the wild, RL vs optimal control; with speed, latency, compute platform.
- Why: background §3.1 table of agile flight; define "agile" with numbers.
- Source: phd-proposal/preliminary-results-layout.md §3.1
- Priority: high

## REQ-20261019-7 · partial (see D-36…D-39, D-41, D-42, D-62; Akida weakly sourced, F450-class power breakdown not sourced)
- Need: Energy per operation (Horowitz ISSCC 2014), critical analyses of SNN energy claims (e.g. Dampfhoffer et al.), neuromorphic chip specs (Loihi 2, SpiNNaker 2, Speck, Akida), drone power breakdown propulsion vs compute (nano/micro/F450 class).
- Why: §3.5 energy argument; risk that compute power is negligible on an F450.
- Source: phd-proposal/preliminary-results-layout.md §3.5
- Priority: high

## REQ-20261019-8 · done (see D-3…D-11, D-1, D-2)
- Need: Neuromorphic processing on drones — Loihi PID (Stagsted 2020, Vitale 2021), optic-flow landing (Dupeyroux 2021), neuromorphic attitude estimation/control (Stroobants), fully neuromorphic vision-to-control (Paredes-Vallés 2024), any newer.
- Why: §3.6 positioning table; the closest related work for the novelty claim.
- Source: phd-proposal/preliminary-results-layout.md §3.6
- Priority: high

## REQ-20261019-9 · done (see D-40, D-43…D-50)
- Need: Event cameras (Gallego survey), event-based drone obstacle avoidance (Falanga 2020, EVDodgeNet, Bhattacharya), event simulators (ESIM, v2e) and any event-camera support for Isaac Gym / Aerial Gym.
- Why: §3.7 and Objective 3 feasibility.
- Source: phd-proposal/preliminary-results-layout.md §3.7
- Priority: medium

## REQ-20261019-10 · done (see D-51…D-55, D-19, D-23)
- Need: Privileged teacher–student learning in robotics (Loquercio 2021, Lee et al. legged), sim-to-real for quadrotors (domain randomisation, latency modelling).
- Why: §3.3 background for the method used in preliminary results.
- Source: phd-proposal/preliminary-results-layout.md §3.3
- Priority: medium

## REQ-20261026-1 · open
- Need: Neuromorphic chips that have flown *onboard* a multirotor (not tethered over WiFi like D-56), and the practical access path for each (Loihi 2 / Kapoho Point via INRC, Akida M.2/PCIe on Jetson, SynSense Speck/Xylo, SpiNNaker2 board): mass, power, interface (USB/PCIe), supported neuron models (CUBA-LIF? population coding?), toolchain from PyTorch/snnTorch.
- Why: Objective 1 now requires deployment "on neuromorphic hardware"; no hardware path exists in the code repos. Need to decide whether the objective is feasible on an F450 or must be reworded to "neuromorphic-compatible SNN on embedded compute".
- Source: phd-proposal/sections/02-research-objectives.tex:4
- Priority: high

## REQ-20261026-2 · open
- Need: SNN RL papers that ablate membrane-state carry-over vs reset between control steps (stateful vs stateless spiking policy), and that use learnable/long time constants (PLIF, ALIF, adaptive threshold) for memory over ~0.5–2 s in control or navigation tasks. Include any that quantify memory horizon of LIF with β≈0.75.
- Why: Objective 2. The current student resets membrane every control step (pop_spiking_actor.py:149), so Objective 2 needs a stateful variant and a principled ablation; need the closest prior design and its result.
- Source: phd-proposal/sections/02-research-objectives.tex:5
- Priority: high

## REQ-20261026-3 · open
- Need: Spiking (or event-native) depth / collision-occupancy estimation from event cameras that runs in real time, and any work using event-derived depth as input to a learned flight policy (beyond D-46, D-56). Also any Aerial Gym / Isaac Gym event simulation added since D-49/D-50.
- Why: Objective 1 merges event cameras into the deliverable; the current perception is a depth-image VAE. Need to know whether "events → collision latent" is a known solved block or a research contribution in itself.
- Source: phd-proposal/sections/02-research-objectives.tex:4
- Priority: medium
