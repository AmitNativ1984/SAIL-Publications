# PhD Proposal — Layout: Background & Preliminary Results

Citations marked *(verify)* are from memory — check each one before it goes into the .bib.
Literature requests for every subsection are in `../literature/requests.md`.

---

# 3. Related Work and Scientific Background — Layout

**Message of the section:** agile flight on small drones is limited by perception-to-action
latency and onboard power → neuromorphic sensing (event cameras) and processing (SNNs)
target exactly those limits → prior neuromorphic drone work has shown pieces of this, but
not *[your gap: learned, vision-based navigation in clutter with an SNN policy, deployed on
a real platform]*.

Every subsection ends with a one-sentence **gap** that points at one of your objectives.
Budget: ~8–10 pages.

## Critical review of the current section (fix before adding)

- **Background and related work are mixed.** Background = what the reader needs to understand
  your method (LIF, encoding, surrogate gradients, PPO, quadrotor control). Related work =
  who did what, and where your work sits. Keep them visibly separate (or at least end each
  subsection with "related work" + "gap").
- **It is SNN-textbook-heavy and positioning-light.** ~150 lines on LIF/training, zero on
  drones, RL, or prior neuromorphic flight. A committee reads this as "the student knows SNNs,
  but does not know the field they claim to contribute to."
- **The SNN training derivation is half-written** (unfinished equations, "Consider the
  immidiate influence…", "The output layer of the a spiking", broken ref
  `eq:RC_discrete_weighted`). For a proposal, cut it to: dead-neuron problem → three families
  → surrogate gradient + BPTT, with one equation. The derivation adds length, not credibility.
- **Empty subsections:** "Population Spiking Actor for Continuous Control", "Drone Dynamics and Control".
- **4 references total.** A proposal background needs ~50–80. This is the most visible weakness.
- **Missing topics you actually use:** reinforcement learning / PPO, teacher–student
  (privileged) learning and policy distillation, sim-to-real, depth-based navigation /
  collision encoding. Your preliminary results depend on all of them and none are introduced.
- **The energy argument is assumed, not made** (see 3.5 — it is the one a reviewer will attack).

## Order and content

### 3.1 Agile Autonomous Flight  *(problem domain first — motivates everything else)*

**Cover**
- What "agile" means — define it with numbers: speed (m/s), acceleration, reaction time,
  obstacle density. You will reuse this definition in Results.
- Model-based pipeline (perception → mapping → planning → control) vs learned end-to-end
  policies; why latency accumulates in the modular stack.
- State of the art: drone racing (Swift, Kaufmann et al., Nature 2023 *(verify)*), learned
  high-speed flight in the wild (Loquercio et al., Sci. Robotics 2021 *(verify)*), RL vs
  optimal control (Song et al., Sci. Robotics 2023 *(verify)*), learned depth-based navigation
  in clutter (Kulkarni & Alexis, DCE / ORACLE *(verify)*).
- What these systems run on (GPU/Jetson-class compute, watts) and their perception latency.
- **Gap:** agile learned flight works, but on power-hungry compute and frame-based sensors
  with tens of ms of latency.

**Show**
- **Table: agile flight SOTA** — work | task | sensor | compute | max speed | latency | sim/real.
  Leave a row for *this work*.

### 3.2 Quadrotor Dynamics and Control Hierarchy  *(background)*

**Cover**
- Rigid-body dynamics in brief (thrust, torques, rotation).
- Control hierarchy: position → velocity → attitude → body-rate → motor; where PX4 sits.
- Which interface learned policies use (CTBR, attitude, velocity) and the trade-off:
  lower level = more agile, harder sim-to-real. Justify your attitude-level choice here.

**Show**
- **Figure:** control-hierarchy block diagram with loop rates; mark where your policy plugs in.
- Equations: 2–3 lines of dynamics, no more.

### 3.3 Learning-Based Control: RL, Teacher–Student, Sim-to-Real  *(background + related work)*

**Cover**
- RL formulation (MDP; POMDP mentioned in one sentence as future work), actor–critic, PPO.
- GPU-parallel simulation (Isaac Gym, Aerial Gym) and why it makes RL on drones feasible.
- Privileged teacher → student distillation in robotics (Loquercio 2021, Lee et al. legged
  locomotion *(verify)*), DAgger (Ross et al. 2011), policy distillation / PPD (Spigler 2024).
- Sim-to-real: domain randomisation, latency modelling, sim-to-sim as an intermediate step.
- **Gap:** teacher–student is standard for ANN students; ANN→SNN policy distillation is rare.

**Show**
- One equation each for the PPO objective and the distillation loss (reuse in Results).

### 3.4 Spiking Neural Networks  *(existing material — trimmed)*

**Cover**
- Neuron model (LIF), spike encodings (rate / latency / population) — keep, tighten.
- Training — trimmed as above.
- **SNNs for RL and continuous control** (the empty subsection): PopSAN (Tang et al. 2020),
  hybrid SNN-ANN actor–critic, conversion vs direct training for control, Huebotter et al. 2025.
- **Gap:** most SNN-RL results are on MuJoCo/Gym benchmarks, not closed-loop vision-based flight.

**Show**
- Keep `LIF_neuron.png` and the encoding figures.
- **Table: SNN for RL/control** — work | task | encoding | training method | timesteps | real robot?

### 3.5 Energy and Latency of Neural Computation  *(the claim a reviewer attacks first)*

**Cover**
- Energy per operation: MAC (multiply-accumulate) vs AC (accumulate only), memory access
  dominating compute (Horowitz, ISSCC 2014 *(verify)*). SNN cost ≈ spikes × fan-out × E_AC;
  ANN cost ≈ MACs × E_MAC.
- **The honest caveats — say them before a reviewer does:**
  - SynOps-based estimates ignore memory access, timesteps T, and the encoder; several
    studies show SNNs win only at low spike rates and few timesteps (Dampfhoffer et al.
    *(verify)*). With T = 5 and population coding, your advantage is not automatic.
  - On GPUs SNNs are *slower and costlier*; the benefit needs neuromorphic hardware.
  - **Drone power budget:** on an F450, propulsion is hundreds of watts; compute is a few
    percent. The energy argument is strong for micro/nano drones (where compute is a large
    share of the budget) and weak for an F450. For the F450, **latency and determinism** are
    the more defensible argument. Decide which you claim, and say so.
- Neuromorphic hardware landscape: Loihi 2, SpiNNaker 2, SynSense Speck/Xylo, BrainChip
  Akida — power, I/O, availability, whether they can be flown.
- **Gap:** energy benefit of SNN control is mostly estimated, rarely measured in flight.

**Show**
- **Table: energy per op** — 32-bit FP MAC, add, SRAM access, DRAM access (pJ).
- **Table: compute platforms** — Jetson Orin / Loihi 2 / Speck / Akida / ... | power (W) |
  latency | mass | flight-proven?
- **Figure (strong if you can make it):** power breakdown for nano / micro / F450-class drones
  — propulsion vs compute vs sensors. Shows exactly where neuromorphic matters.

### 3.6 Neuromorphic Processing in Drone Flight  *(closest related work — most important)*

**Cover**
- Chronological: SNN PID / attitude control on Loihi (Stagsted et al. RSS 2020; Vitale et al.
  ICRA 2021 *(verify)*), neuromorphic optic-flow landing (Dupeyroux et al. ICRA 2021
  *(verify)*), neuromorphic attitude estimation & control (Stroobants et al. *(verify)*),
  fully neuromorphic vision-to-control flight on Loihi (Paredes-Vallés et al., Sci. Robotics
  2024 *(verify)*).
- For each: what was spiking (perception, control, both), which level of control, learned
  or hand-designed, hardware, real flight or not.
- **Gap:** this is where your contribution must be stated precisely — e.g. "no prior work
  flies a learned SNN policy through clutter from depth" — *only after the literature agent
  confirms it.*

**Show**
- **The key positioning table of the proposal:**

  | Work | Sensor | Spiking part | Control level | Learned? | Task | Neuromorphic HW | Real flight |
  |---|---|---|---|---|---|---|---|
  | ... | | | | | | | |
  | **This work** | depth → (event) | policy | attitude | RL + distillation | clutter nav | planned | planned |

### 3.7 Event Cameras and Event-Based Drone Flight  *(Objective 3)*

**Cover**
- Principle: per-pixel asynchronous brightness changes; µs latency, high dynamic range, no
  motion blur, sparse output (Gallego et al. survey, TPAMI 2020 *(verify)*).
- Representations: event streams, voxel grids, time surfaces; natural fit to SNNs.
- Event-based drone flight: dynamic obstacle dodging (Falanga et al., Sci. Robotics 2020
  *(verify)*), EVDodgeNet (Sanket et al. *(verify)*), learned event-based obstacle avoidance
  (Bhattacharya et al. *(verify)*), event-based optic flow for control.
- Simulation: ESIM, v2e *(verify)* — and the gap that Isaac Gym / Aerial Gym have no native
  event camera. **This is a methodological risk for Objective 3; name it.**
- **Gap:** event perception and spiking control rarely combined in a learned, closed-loop
  navigation policy.

**Show**
- **Figure:** frame vs event output for the same motion (classic illustration — make your
  own from sim or a public dataset, don't copy).
- **Table:** depth camera (D435) vs event camera — latency, rate, dynamic range, power, data.

### 3.8 Summary and Research Gap  (½ page)

**Cover**
- 3 bullets, one per objective, each = "the literature shows X, nobody has shown Y, this
  proposal does Y."

**Show**
- Refer back to the positioning table in 3.6 — the empty cells are the PhD.

## What else is missing (beyond the five topics asked for)

| Missing | Why it matters | Where |
|---|---|---|
| RL / PPO background | Results use PPO everywhere; reader can't follow §4.2–4.3 | 3.3 |
| Teacher–student & policy distillation | Your core method; currently uncited | 3.3 |
| Quadrotor dynamics & control hierarchy | Subsection exists but empty; justifies attitude-level actions | 3.2 |
| Depth perception for navigation (DCE, VAE latents) | Your perception stage is borrowed; must be credited | 3.1 or 3.3 |
| Sim-to-real for drones | You claim a digital twin; reader needs the context | 3.3 |
| Neuromorphic hardware details | Objective 1 depends on choosing a chip; feasibility unshown | 3.5 |
| Positioning table | The single most effective way to show novelty | 3.6 |

## How to present it

- **Funnel order:** problem (agile flight) → constraint (latency, power) → candidate solution
  (neuromorphic) → what exists → gap. Not tool-first (SNNs) as it is now.
- **Tables over prose** for comparing prior work — one per subsection where noted above.
  A reviewer scans tables; prose comparisons get skimmed.
- **Every subsection ends with a gap sentence**, and every gap maps to an objective.
- **Quantify claims** (W, ms, pJ, m/s) — "energy-efficient" and "low latency" without a number
  are exactly what a committee challenges.
- **Your own figures** (control hierarchy, power breakdown, frame vs events) beat reused ones.
- **Cite primary sources**, not only surveys; check every *(verify)* above.

---

# 4. Preliminary Results — Layout

**Message of the section:** a spiking policy can fly a quadrotor through dense clutter from
onboard depth alone, and there is a working path from GPU simulation to the real F450.

Memory / POMDP and event cameras are *not* presented here — they appear only as open
problems in §4.5 and in the research plan.

Budget: ~6–8 pages. The SNN section (§4.3) must be the longest.

---

## 4.0 Overview  (½ page)

**Cover**
- The goal: a spiking controller that closes the loop from onboard depth to attitude commands.
- Why simulation first: RL needs millions of flights; early ones crash.
- Why staged (teacher → student): SNN trained from scratch with RL did not progress through
  the curriculum. *State the run and the level it stalled at; if none, say "slow to progress".*
- 3 headline bullets, SNN first, qualitative only (numbers come later):
  1. A population-coded SNN student flies the clutter task, distilled from an ANN teacher.
  2. A measurement-driven reward design produced a teacher that flies dense clutter.
  3. The policy is exported and running against PX4 in Gazebo; hardware is being assembled.

**Show**
- **Figure: pipeline diagram** — depth camera → VAE (32-d) → ANN teacher → SNN student →
  ONNX → ROS 2 node → PX4. Mark which stages run on the drone.

---

## 4.1 Experimental Setup  (1 page)

**Cover**
- **Task:** start → target in a 20 × 20 × [4, 6] m volume; trees, panels, spheres, cylinders,
  walls; Poisson density over 30 curriculum levels (~110–160 obstacles at level 25).
- **Vehicle:** F450 digital twin matched to the Gazebo/PX4 model; measured capture-to-control
  latency trained in; ~33 Hz control.
- **Action:** collective thrust, roll, pitch (±45°), yaw rate (±60°/s) → low-level attitude controller.
- **Observation:** 17-d state + 32-d depth latent = 49-d.
- **Perception:** collision-aware depth VAE — decoder reconstructs obstacles dilated by the
  drone's collision sphere, so the latent encodes *where the drone can fly*. 2–3 sentences.
- **Evaluation protocol (one place, referenced everywhere after):** deterministic policy,
  episodes per evaluation, number of seeds, curriculum levels evaluated, definitions of
  success / crash / timeout.

**Show**
- **Figure:** `vae_collision_encoding.png` (raw depth / collision target / reconstruction).
- **Table (optional, small):** observation and action spaces with dimensions and bounds.

---

## 4.2 ANN Teacher  (≤ 1 page — do not let it outgrow §4.3)

**Cover**
- Architecture: MLP actor-critic 256–256–64, PPO, 1024 parallel envs.
- Reward shaping as a short measurement-driven story:
  1. *Action regularisation* — one sentence: bounds loss + magnitude penalty, saturation
     ~20% → ~2%, task performance unchanged.
  2. *Crash analysis* — the heading term dominated the return and encouraged flying straight
     at the target; most crashes happened while moving outside the camera's view, with a free
     corridor available 1.2 s before impact.
  3. *Fix* — remove heading term; add p_fov (velocity outside the sensed frustum) and p_cbf
     (closing speed vs clearance). Penalties sized from measured rollout statistics.
- Final teacher performance at levels 10 / 20 / 30.
- Close with: the teacher sets the target the SNN must match.

**Show**
- **Table: reward revisions → crash rate at level 30.** Matched training budgets
  (report the `p_fov_ft` run as the control for `+p_cbf`, or drop that row).
- **Figure:** `crash_atlas.png` — the one figure for the crash story.
- **Table: final teacher success / crash at levels 10, 20, 30.** (Can merge with the above.)
- `action_traces.png` — optional; cut if space is tight.

---

## 4.3 Spiking Student  (2–3 pages — the core)

**Cover**
- **Architecture:** PopSAN; 2 hidden layers of 256 current-based LIF neurons (β = 0.75);
  T = 5 timesteps per control step; ANN critic used only during training.
- **Population encoding:** 10 Gaussian-receptive-field neurons per observation dimension (490
  total), deterministic IF encoder; output populations of 10 LIF neurons per action channel,
  rate-decoded.
  - Key point: encoder bounds from the teacher's 1st/99th observation percentiles, because a
    field where the observation never goes is silent (fires only if A ≥ 0.19 at T = 5).
- **Behaviour-cloning warm-up:** DAgger-style mixing, teacher control annealed 1 → 0 over
  1M of 2M steps; student success ~0 → 0.74.
- **PPO fine-tuning with teacher KL regulariser:** two failure modes and the fix —
  - LR stall: distillation term keeps KL above the adaptive-LR threshold → LR floored → ~0.5.
  - Collapse: uncapped LR + entropy bonus → entropy runaway → success 0.
  - Fix: LR cap 1e-3, entropy coeff 0.002 → stable at warm-up level for 720+ epochs.
  - Be explicit: fine-tuning currently *holds* BC performance, does not yet improve it.
- **Headline result — student vs teacher at the same level and teacher.**

**Show**
- **Figure:** `population_encoding.png` (encoding scheme). `LIF_neuron.png` if not already in Background.
- **Equations:** receptive field (Eq. GRF) and the distillation loss (Eq. PPD).
- **Table: BC warm-up** — env steps / BC loss / β / student success / return.
- **Figure:** `distill_overview.png` — success, entropy, LR for stall / collapse / fixed runs.
- **Headline table (must exist):**

  | Policy | Success | Crash | Params | Inference cost | Latency |
  |---|---|---|---|---|---|
  | ANN teacher | | | | MACs | |
  | SNN student | | | | SynOps, spike rate | T = 5 steps → ms |

  Same level, same teacher it was distilled from, same eval protocol.
  If the new (latency-trained p_fov) distillation isn't done, use the level-25 teacher it was
  distilled from and note the new one as in progress.

---

## 4.4 Deployment Path  (½ page — cut to 3 lines in §4.5 if no numbers)

**Cover**
- ONNX export of VAE encoder + SNN actor; parity vs training code (max abs error).
- ROS 2 policy node against PX4 (uXRCE-DDS); Gazebo sim2sim in a simulated pine forest —
  success rate.
- Spiking hover policy exported through the same path (one line).
- Hardware: F450, Pixhawk 6C, Jetson Orin, RealSense D435 — status.

**Show**
- **Small table:** parity error, Gazebo success rate, control-loop rate achieved.
- **Figure (optional):** Gazebo forest screenshot with a flown trajectory.

---

## 4.5 Summary and Open Problems  (½ page)

**Cover**
- What works: SNN flies cluttered navigation in simulation at X% of the teacher; deployment
  path exists.
- What's open, mapped to objectives:

**Show**
- **Table: status per objective.**

  | Objective | Done | In progress | Open |
  |---|---|---|---|
  | 1. SNN controller on neuromorphic HW, real flight | SNN student in sim; ONNX/ROS 2 path | Distillation of latest teacher; hardware build | Neuromorphic HW port; real flights; energy measurement |
  | 2. SNN memory under partial observability | — | — | GRU/SNN memory study, FOV ablations |
  | 3. End-to-end neuromorphic (event camera + SNN) | — | — | Event-based perception replacing depth VAE |

- One-line pointer to the research plan (§5).

---

## Gaps to close before writing

- [ ] Student vs teacher at matched level + spike rate / SynOps vs MACs (§4.3 headline table).
- [ ] Evidence for "SNN from scratch did not progress" (run + stalled level).
- [ ] Matched-budget control for `+p_cbf` (`f450_nav_p_fov_ft`).
- [ ] Seeds and episode counts for every reported rate.
- [ ] ONNX parity error and Gazebo success rate (§4.4).
- [ ] Missing citations: DCE (Kulkarni & Alexis), DAgger (Ross 2011), PPD (Spigler 2024), PopSAN.
