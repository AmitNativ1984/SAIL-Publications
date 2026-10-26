# Literature digest

Run 2026-10-19: first full sync. Library inventoried (330 regular items, 2290 keys incl. attachments/annotations), no per-item entries for the backlog. Entries below answer REQ-20261019-1 … -10.

---

# REQ-1 / REQ-8: neuromorphic and SNN drone control (closest prior work)

## D-1 · Fully spiking PPO actor-critic for agile quadcopter flight, real flights vs ANN (van Breukelen Castillo 2025)
- Source: Zotero `SpikingNeuralNetworks` (item WNQ5YFFP; **metadata empty, needs fixing**). DOI 10.1142/s2301385027410147 (Unmanned Systems, 2026); IMAV 2025 paper 17 (https://www.imavs.org/papers/2025/17.pdf)
- Answers: REQ-20261019-1, REQ-20261019-8, REQ-20261019-2
- Venue: IMAV 2025; journal version Unmanned Systems 2026 (Crossref)
- One-line finding: TU Delft (de Croon group) trains a fully spiking LIF actor-critic (3×64, surrogate gradients, rate decoding over C cycles) directly with PPO for gate racing. 20-D state input from mocap/EKF, motor-level output, running on the STM32H743 flight controller (INDIflight), not on neuromorphic hardware. In 12 s real flights the SNN beats a matched ANN: reward 70.63 vs 59.77, 7.94 vs 6.99 m/s, 46.33 vs 40.67 gates. 5–8 cycles give the best resolution/latency trade-off.
- Relevance: **threatens novelty** of any claim to be the first learned SNN policy flown for real, or the first SNN-vs-ANN real-flight comparison (Objective 1). It does not threaten the depth/clutter claim: there is no vision and no obstacles, it is state-based, and it uses direct PPO rather than distillation. It is also evidence that direct SNN PPO works for state-based control, which contrasts with our "SNN from scratch failed to progress" observation (that was depth latent + clutter).
- Use in: §3.6 positioning table (must be a row); Objective 1 novelty statement; §5.3 distillation motivation; T=5 choice (they also land on 5–8 cycles).
- Amit's notes: 19 highlights on the LIF/rate-decoding/current-injection design, the "first fully spiking actor-critic … agile gate navigation" claim, the cycles-vs-latency analysis, and the code repo (github.com/michael2992/msc_spiking_quadcopter_control).

## D-2 · SNN actor-critic PPO for UAV navigation through constrained openings (Walugembe 2026)
- Source: to-add (arXiv:2609.23643)
- Answers: REQ-20261019-1, REQ-20261019-8
- Venue: arXiv preprint, 20 Sep 2026
- One-line finding: Spike-based actor-critic PPO with a Gaussian policy navigates a UAV through sequential 3D openings (inspection scenario) in simulation. 1,913 successes in more than 3,000 episodes (63.77% overall, above 90% late in training), 2.10 windows per episode. The abstract states no sensor modality, no ANN baseline and no hardware deployment (the authors list these as future work).
- Relevance: **threatens novelty** (partial). It is the closest found "learned SNN navigation policy for a UAV among obstacles", and it is recent. It is weaker than our setup (simulation only, no baseline, sensors unstated), but it rules out an unqualified "first SNN navigation policy for drones" claim.
- Use in: §3.6 table; novelty wording for Objective 1.
- Amit's notes: n/a

## D-3 · Fully neuromorphic vision and control for autonomous drone flight (Paredes-Vallés 2024)
- Source: Zotero `paredes-vallesFullyNeuromorphicVision2023` (arXiv version; cite as Science Robotics 9(90):eadi0591, 2024, DOI 10.1126/scirobotics.adi0591)
- Answers: REQ-20261019-8, REQ-20261019-1, REQ-20261019-7
- Venue: Science Robotics 2024
- One-line finding: Event camera (DAVIS240C) → 5-layer, 28.8k-neuron SNN (self-supervised ego-motion) → single linear decoding layer evolved in simulation. The whole pipeline runs on Loihi (Kapoho Bay) at 200 Hz, 27 µJ per inference. Real flights: hover, landing, sideways manoeuvres with yaw. Control is through PX4 attitude/thrust.
- Relevance: baseline candidate, the closest "fully neuromorphic" system. The control part is not RL, it is evolved and linear; there are no obstacles and no clutter.
- Use in: §3.6 table; §3.5 energy (27 µJ); Objective 3 template (also uses ROS 2→PX4).
- Amit's notes: Most-annotated item (112). Highlights cover the Loihi/Kapoho Bay + DAVIS240C + PX4/ROS 2 stack, 200 Hz, evolved 4×9 linear controller, domain randomisation (flow noise, attitude bias, initial conditions), and Flightmare drag modelling. A comment links it to the earlier de Croon Loihi landing work (D-7).

## D-4 · Neuromorphic attitude estimation and control (Stroobants 2025)
- Source: Zotero `stroobantsNeuromorphicAttitudeEstimation2025` (arXiv:2411.13945)
- Answers: REQ-20261019-8, REQ-20261019-2
- Venue: arXiv 2024/2025 (TU Delft)
- One-line finding: An SNN maps raw IMU input to motor commands (estimation and control sub-networks trained separately by imitation of the PX4-like stack, then merged) on a Crazyflie at 500 Hz, on a microcontroller rather than a neuromorphic chip. Attitude tracking error is 3.0° vs 2.7° for the stock controller.
- Relevance: baseline candidate. It is also a reference student/teacher gap for imitation into an SNN: the student reaches ~0.9× the teacher's tracking accuracy.
- Use in: §3.6 table; §5.3 distillation (reference gap, time-shifted targets for SNN delay).
- Amit's notes: Highlights cover the four challenges (sensor bias, SNN delays, reality gap, spikes→smooth motor command), time-shifted targets to compensate SNN delay, integrator-constrained neuron subgroup, and the "first fully neuromorphic attitude estimation and control" claim.

## D-5 · SNN-based PID controller on Loihi for a 1-DoF UAV (Stagsted 2020)
- Source: to-add (DOI 10.15607/RSS.2020.XVI.074)
- Answers: REQ-20261019-8
- Venue: RSS 2020
- One-line finding: A hand-designed SNN PID on Loihi controls a UAV constrained to 1 DoF. Gains are synaptic weights adaptable on chip.
- Relevance: background (first row of the chronological table: hand-designed, 1-DoF).
- Use in: §3.6 table.
- Amit's notes: n/a

## D-6 · Event-driven vision and control for UAVs on a neuromorphic chip (Vitale 2021)
- Source: Zotero `vitaleEventdrivenVisionControl2021` (arXiv:2108.03694)
- Answers: REQ-20261019-8
- Venue: ICRA 2021
- One-line finding: Event-based line tracking implemented as an SNN on Loihi, closing the loop on a constrained 1-DoF dualcopter, with online adaptation of the SNN controller. The authors show faster control rates and lower latency than off-chip processing.
- Relevance: background (spiking perception + hand-designed control, 1-DoF).
- Use in: §3.6 table.
- Amit's notes: none

## D-7 · Neuromorphic control for optic-flow landings on Loihi (Dupeyroux 2021)
- Source: to-add (arXiv:2011.00534)
- Answers: REQ-20261019-8
- Venue: ICRA 2021
- One-line finding: A 35-neuron, 3-layer SNN, evolved in simulation, runs fully embedded on Loihi for divergence-based landing of a real MAV. Thrust setpoint RMSE 0.005 g; 99.8%/99.7% spike-sequence match between simulation and Loihi.
- Relevance: background (evolved, tiny, 1-D task, real flight on Loihi).
- Use in: §3.6 table.
- Amit's notes: n/a (cited in his D-3 annotation)

## D-8 · Directly-trained SNN DQN for event-based UAV obstacle avoidance (Zanatta 2022/2023)
- Source: to-add (DOI 10.1145/3528416.3530865 [CF'22]; DOI 10.1016/j.neucom.2023.126885 [Neurocomputing 562, 2023])
- Answers: REQ-20261019-1, REQ-20261019-8
- Venue: ACM Computing Frontiers 2022; Neurocomputing 2023
- One-line finding: SNNs trained directly with deep Q-learning on DVS input for UAV obstacle avoidance in AirSim/UE4. Performance is comparable to the ANN. The thesis abstract reports ~6× lower energy than CNNs. Simulation only, discrete actions.
- Relevance: **threatens novelty** (partial). This is prior learned-SNN UAV obstacle avoidance, but in simulation only, with discrete DQN actions, event input, no real flight, and no attitude-level continuous control. The related Zotero item `zanattaExploringSpikingNeural2024` is their Sci. Rep. 2024 comparison of SNN vs ANN PPO on robotic tasks.
- Use in: §3.6 table (simulation row); §3.4 SNN-for-RL table.
- Amit's notes: none on the 2024 paper (5 highlights, no comments)

## D-9 · SNN (LGMD) for UAV obstacle avoidance targeting neuromorphic processors (Salt 2020)
- Source: to-add (DOI 10.1109/tnnls.2019.2941506)
- Answers: REQ-20261019-8
- Venue: IEEE TNNLS 2020
- One-line finding: A locust-LGMD-inspired SNN for UAV collision avoidance, with parameters optimised for neuromorphic processors (from title and abstract metadata; full text not read).
- Relevance: background (bio-inspired, not RL).
- Use in: §3.6 table (bio-inspired row).
- Amit's notes: n/a

## D-10 · SNN control of a flapping-wing robot fully onboard an ESP32 (El Filali 2026)
- Source: to-add (arXiv:2605.19430)
- Answers: REQ-20261019-8, REQ-20261019-7
- Venue: arXiv, May 2026 (v3 Sep 2026)
- One-line finding: Two SNNs (state estimation and CPG modulation), trained by imitation learning, fly a <30 g butterfly-like FWMAV untethered, fully onboard an ESP32. Compared with an ANN, latency drops from 1059 to 680 µs (−36%) and power from 0.033 to 0.027 W (−18%).
- Relevance: supports. It shows SNN gains measured on commodity MCUs and is a fresh 2026 real-flight SNN result (not quadrotor, not navigation).
- Use in: §3.6 table; §3.5 (measured, not estimated, energy).
- Amit's notes: n/a

## D-11 · Real-time neuromorphic navigation: event SNN detection + physics-guided planning on a Bebop2 (Joshi/Sanyal/Roy 2024–2025)
- Source: to-add (arXiv:2407.00931; follow-up arXiv:2503.09636)
- Answers: REQ-20261019-8
- Venue: arXiv 2024 / 2025 (Purdue)
- One-line finding: A DAVIS346 event camera feeds a shallow SNN that detects a moving ring. A physics-guided network plans the flight path through it on a Parrot Bebop2. The follow-up extends the stack to a TurtleBot. Spiking perception only; the planning/control is not spiking.
- Relevance: background (hybrid neuromorphic perception, real quadrotor).
- Use in: §3.6 table.
- Amit's notes: n/a

## D-12 · RL ANN policy converted to sigma-delta SNN on Loihi 2 (Stewart 2025)
- Source: Zotero `stewartAutonomousReinforcementLearning2025` (arXiv:2512.03911)
- Answers: REQ-20261019-1, REQ-20261019-2
- Venue: arXiv, Dec 2025 (submitted to NICE 2026)
- One-line finding: A ReLU RL policy for the Astrobee free-flyer is converted to a Sigma-Delta NN and run on Loihi 2, evaluated in Omniverse/Isaac simulation. It is an end-to-end train→convert→deploy pipeline.
- Relevance: method to borrow. It is a concrete Loihi 2 deployment path for an RL policy, and an alternative to PopSAN distillation that a reviewer may ask about.
- Use in: Objective 1 hardware path; §5.3 (conversion vs distillation).
- Amit's notes: none

---

# REQ-2: ANN→SNN policy distillation

## D-13 · PopSAN: population-coded spiking actor for continuous control (Tang 2020)
- Source: Zotero `tangDeepReinforcementLearning2020` (already cited)
- Answers: REQ-20261019-2
- Venue: CoRL 2020 (arXiv:2010.09635)
- One-line finding: The population-coded spiking actor (learnable Gaussian receptive fields µ,σ) is trained jointly with a deep critic (TD3/DDPG/SAC/PPO) and matches ANN performance on MuJoCo. On Loihi it uses 140× less energy per inference than on a Jetson TX2.
- Relevance: method (our student architecture).
- Use in: §5.3; §3.5.
- Amit's notes: Highlights on population encoding/decoding, learnable µ,σ, the 140× Loihi energy figure, and "For PPO, PopSAN predicts the action mean via the clipped surrogate loss".

## D-14 · Proximal Policy Distillation (Spigler 2025)
- Source: Zotero `spiglerProximalPolicyDistillation2025` (arXiv:2407.15134)
- Answers: REQ-20261019-2
- Venue: TMLR, 06/2025
- One-line finding: PPO with an added distillation loss (student-driven) beats student-distill and teacher-distill on Atari, MuJoCo and Procgen. Students reach these fractions of the teacher's score (Table 1): smaller students 0.97× (Atari), 0.99× (MuJoCo), 0.93× (Procgen); same-size students 1.0–1.08×. Pure supervised distillation into smaller students drops to 0.72–0.78× on Procgen.
- Relevance: method (used), and the **reference gap**. ANN→ANN distillation typically recovers ≥0.9× of the teacher. Our SNN student at 0.74 success vs teacher ~0.88 (level 30; note the warm-up is at level 25) is ≈0.84×, below the ANN→ANN range.
- Use in: §5.3 student/teacher comparison.
- Amit's notes: Highlights that the student acts as the control policy, teacher as "skills prior", and distillation + RL in one objective.

## D-15 · ES-Parkour: ANN teacher distilled into spiking student for quadruped parkour (Zhang 2025)
- Source: to-add (arXiv:2503.09985)
- Answers: REQ-20261019-2
- Venue: arXiv, Mar 2025
- One-line finding: An ANN parkour policy is distilled into an SNN (IF neurons, T=4, spiking ResNet-18 event encoder + GRU + 3-layer spiking MLP) by MSE on actions while the student interacts with the environment (DAgger-like), in Isaac Gym with 32 envs. Energy is reported as 11.7% of the ANN's. Per-terrain success is shown only in a figure; simulation only.
- Relevance: method to borrow and closest prior on robot ANN→SNN policy distillation. It shows the pipeline is not new in itself. Our novelty must come from the flight domain plus the analysis of RL fine-tuning failure modes.
- Use in: §5.3; §3.4 SNN-for-RL table.
- Amit's notes: n/a

## D-16 · Population-coded SNNs for high-dimensional robotic control in Isaac Gym (Jaisankar 2025)
- Source: to-add (arXiv:2510.10516)
- Answers: REQ-20261019-2
- Venue: arXiv, Oct 2025
- One-line finding: PopSAN plus deep RL on PixMC Franka manipulation in Isaac Gym, with "comparable" performance to ANNs and up to 96.10% estimated energy saving. Simulation only; the abstract gives no performance numbers.
- Relevance: background (PopSAN in Isaac Gym at scale, same toolchain as ours).
- Use in: §3.4 table.
- Amit's notes: n/a

## D-17 · DAgger (Ross 2011)
- Source: to-add (PMLR 15:627–635)
- Answers: REQ-20261019-2, REQ-20261019-10
- Venue: AISTATS 2011
- One-line finding: "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning", which trains the student on states from its own rollouts.
- Relevance: background (fills the `% TODO cite` at the BC warm-up paragraph).
- Use in: §5.3 BC warm-up.
- Amit's notes: n/a

---

# REQ-3: learned depth-based navigation in clutter (benchmarks)

## D-18 · RL for collision-free flight exploiting deep collision encoding (Kulkarni & Alexis 2024)
- Source: Zotero `kulkarniReinforcementLearningCollisionfree2024` (arXiv:2402.03947)
- Answers: REQ-20261019-3
- Venue: ICRA 2024
- One-line finding: The DCE latent plus odometry feeds a PPO policy in Aerial Gym with a 30-level curriculum (level n = n obstacles in an [8,12]×[5,8]×[4,6] m box). Success: L0 99.4%, L10 90.6%, L20 78.5%, L25 72.7%, **L30 70.8%**, with speed capped at 1.5 m/s and yaw rate at 60°/s. Real flights at 1.2 m/s; inference 15 ms on Orin NX.
- Relevance: **the direct external benchmark** for our 87.8% at level 30. Caveat: our levels are not the same as theirs (our L25 has ~110–160 obstacles in 20×20 m), so compare obstacle density and speed, not level numbers.
- Use in: §4 teacher results; DCE citation (`% TODO cite` in §subsec:vae).
- Amit's notes: none

## D-19 · Learning high-speed flight in the wild (Loquercio 2021)
- Source: Zotero `loquercioLearningHighSpeedFlight2021`
- Answers: REQ-20261019-3, REQ-20261019-6, REQ-20261019-10
- Venue: Science Robotics 2021 (abg5810)
- One-line finding: A privileged MPC expert is imitated by a depth-to-trajectory student. In the simulated forest it reaches 100% success up to 5 m/s and 60% at 10 m/s, while baselines fail at 10 m/s. Average success across environments is 70% at 10 m/s. Real flights at 5–10 m/s in forests, snow, ruins. Total processing latency is 19.1 ms vs 65.2 ms for FastPlanner (Jetson TX2 onboard).
- Relevance: baseline candidate; defines "agile" in clutter (5–10 m/s).
- Use in: §3.1 table; §3.3 privileged teacher-student.
- Amit's notes: 80 highlights; a full note (reused as his Letter of Intent) on the latency/compounding-error argument against sense-map-plan pipelines.

## D-20 · Back to Newton's laws: vision-based agile flight via differentiable physics (Zhang 2025)
- Source: Zotero `zhangBackNewtonsLaws2025`
- Answers: REQ-20261019-3, REQ-20261019-6
- Venue: Nature Machine Intelligence 2025 (DOI 10.1038/s42256-025-01048-0)
- One-line finding: A depth-based policy is trained through differentiable point-mass simulation. Single-agent success is 90% vs 60% for the previous SOTA in complex environments. Real forest flight at up to 20 m/s on a $21 computer, zero-shot sim-to-real.
- Relevance: baseline candidate; sets the current speed bar for depth-based clutter flight.
- Use in: §3.1 table.
- Amit's notes: none

## D-21 · MAVRL: varying-speed RL with memory-augmented depth latent (Yu 2024)
- Source: Zotero `yuMAVRLLearnFly2024` (arXiv:2402.08381)
- Answers: REQ-20261019-3, REQ-20261019-5
- Venue: arXiv 2024 (TU Delft)
- One-line finding: The depth latent is explicitly trained to retain memory of previous depth frames. It outperforms the standard RL latent, and adapting speed gives a better success/agility balance. Deployed on a real drone after minimal fine-tuning. The abstract gives no numbers.
- Relevance: supports Objective 2 (memory helps depth navigation, via the latent rather than recurrence in the policy); baseline candidate.
- Use in: §4 memory subsection; Objective 2.
- Amit's notes: 27 highlights; comment "why variable speed is important".

## D-22 · Vision transformers for end-to-end depth-based quadrotor obstacle avoidance (Bhattacharya 2025)
- Source: Zotero `bhattacharyaVisionTransformersEndtoEnd2025` (arXiv:2405.10391)
- Answers: REQ-20261019-3, REQ-20261019-5
- Venue: arXiv (rev. Apr 2025)
- One-line finding: Compares CNN, U-Net, recurrent and ViT depth→control policies. Adding recurrence improves performance and lowers energy cost at all tested speeds (up to 7 m/s, including hardware).
- Relevance: supports (recurrence helps depth-based avoidance, unlike our inconclusive GRU result).
- Use in: §4 memory; Objective 2.
- Amit's notes: none

---

# REQ-4: perception-aware reward and CBF reward shaping

## D-23 · Learning perception-aware agile flight in cluttered environments (Song 2023)
- Source: Zotero `songLearningPerceptionAwareAgile2023` (arXiv:2210.01841)
- Answers: REQ-20261019-4, REQ-20261019-3, REQ-20261019-10
- Venue: arXiv:2210.01841, 2022/2023 (venue not verified)
- One-line finding: The RL teacher uses a perception-aware reward r_pa = exp(−‖θ_yaw − θ_dir‖) that aligns the camera with the flight direction (toward the farthest collision-free point). It is distilled into a vision-based student; 10× faster computation and higher success than a sampling-based planner (HIL).
- Relevance: **threatens novelty** of p_fov as a design contribution. A reward coupling motion direction to camera FOV is prior art. Ours penalises velocity outside the frustum rather than rewarding yaw alignment, so cite it as a variant and do not claim it as new.
- Use in: §subsec:teacher reward paragraph.
- Amit's notes: 30 highlights; note defines perception-aware flight (Song p.1–3) and that the work targets minimum-time flight in known clutter.

## D-24 · Barrier-function-inspired reward shaping for RL (Nilaksh 2024)
- Source: to-add (arXiv:2403.01410)
- Answers: REQ-20261019-4
- Venue: ICRA 2024
- One-line finding: Reward shaping derived from barrier functions converges 1.4–2.8× faster, with actuation effort down to 50–60% of the vanilla reward (CartPole, Ant, Humanoid). Sim-to-real on a Unitree Go1.
- Relevance: **threatens novelty** of p_cbf as a design contribution. CBF-as-reward-shaping exists. Our discrete-time closing-speed form sized from rollout statistics is a variant; cite it.
- Use in: §subsec:teacher reward paragraph.
- Amit's notes: n/a

## D-25 · Discrete control barrier functions (Agrawal & Sreenath 2017)
- Source: to-add (DOI 10.15607/RSS.2017.XIII.073)
- Answers: REQ-20261019-4
- Venue: RSS 2017
- One-line finding: Extends CBFs to discrete-time systems (NLP/QCQP formulations), applied to bipedal navigation among moving obstacles.
- Relevance: background (the formal source for "discrete-time CBF").
- Use in: §subsec:teacher.
- Amit's notes: n/a

## D-26 · PAMPC: perception-aware MPC for quadrotors (Falanga 2018)
- Source: Zotero `falangaPAMPCPerceptionAwareModel2018`
- Answers: REQ-20261019-4
- Venue: IROS 2018
- One-line finding: The model-based origin of perception awareness: MPC jointly optimises action and keeping a point of interest in the camera FOV.
- Relevance: background.
- Use in: §subsec:teacher; §3.1.
- Amit's notes: none

---

# REQ-5: memory under partial observability; LIF state as memory

## D-27 · GRSN: gated recurrent spiking neurons for POMDPs (Qin 2024)
- Source: Zotero `qinGRSNGatedRecurrent2024` (arXiv:2404.15597)
- Answers: REQ-20261019-5
- Venue: arXiv 2024
- One-line finding: Standard spiking RL runs T SNN steps per RL step (a "temporal mismatch", exactly our T=5 setup). Their temporal-alignment paradigm instead advances neurons one step per RL step, so membrane state accumulates history. With gating (GRSN) it matches RNNs on POMDPs at ~50% of the RNN's power.
- Relevance: **supports** Objective 2 directly, and warns that our current design (state reset per control step? verify) may waste the membrane memory.
- Use in: Objective 2; §subsec:memory.
- Amit's notes: none

## D-28 · LSNN: long short-term memory in spiking networks (Bellec 2018)
- Source: to-add (arXiv:1803.09574)
- Answers: REQ-20261019-5
- Venue: NeurIPS 2018
- One-line finding: Recurrent SNNs with adaptive-threshold neurons (seconds-scale adaptation), trained with BPTT, approach LSTM performance on supervised and RL/learning-to-learn tasks.
- Relevance: supports (spiking neuron state can carry task-relevant memory; plain LIF with β=0.75 has a short horizon).
- Use in: Objective 2 background.
- Amit's notes: n/a

## D-29 · Recurrent model-free RL is a strong baseline for POMDPs (Ni 2022)
- Source: to-add (arXiv:2110.05038)
- Answers: REQ-20261019-5
- Venue: ICML 2022
- One-line finding: With careful architecture and hyperparameters, recurrent model-free RL beats specialised POMDP methods on 18 of 21 environments.
- Relevance: background. It is a counterpoint to "recurrence is costly": our inconclusive GRU result may be a tuning or budget issue, so a reviewer will ask.
- Use in: §subsec:memory.
- Amit's notes: n/a

## D-30 · SpikingNav: embodied navigation with spiking policies whose membrane state is the memory (Zhang 2026)
- Source: to-add (arXiv:2608.05078)
- Answers: REQ-20261019-5
- Venue: arXiv, Aug 2026
- One-line finding: A spiking encoder and a spiking policy keep recurrent policy state through membrane integration and reset (Habitat PointNav/ObjectNav). ObjectNav success is 34.12% vs 31.05% for a matched ANN; under visual corruption 13.71% vs 8.45%. Sensing is validated on a neuromorphic chip.
- Relevance: supports (the membrane state as policy memory is reported to help navigation; not drones).
- Use in: Objective 2.
- Amit's notes: n/a

(See also D-21 MAVRL memory latent, D-22 recurrence helps depth avoidance. D-1 explicitly processes each state independently, so it does not use SNN memory.)

---

# REQ-6: agile flight SOTA

## D-31 · Swift: champion-level drone racing with deep RL (Kaufmann 2023)
- Source: Zotero `kaufmannChampionlevelDroneRacing2023`
- Answers: REQ-20261019-6
- Venue: Nature 620:982–987 (2023)
- One-line finding: Swift beat three world-class pilots in head-to-head races (5/9, 4/7, 6/9 wins) and set the fastest race time (0.5 s ahead of the best human). Sensorimotor latency is 40 ms vs ~220 ms for humans. Onboard Jetson TX2: gate detector 40 ms per pass, policy 8 ms on CPU; 30 Hz camera + T265 VIO.
- Relevance: background (sets the RL agile-flight bar; compute numbers for §3.5).
- Use in: §3.1 table.
- Amit's notes: none

## D-32 · Reaching the limit in autonomous racing: optimal control vs RL (Song 2023)
- Source: to-add (arXiv:2310.10943)
- Answers: REQ-20261019-6
- Venue: Science Robotics 2023
- One-line finding: The RL policy outperforms optimal control and reaches a peak of 108 km/h and more than 12 g, after minutes of training on a workstation.
- Relevance: background (RL vs OC; upper bound of "agile").
- Use in: §3.1 table.
- Amit's notes: n/a

## D-33 · Agilicious open agile quadrotor (Foehn 2022)
- Source: Zotero `foehnAgiliciousOpensourceOpenhardware2022`
- Answers: REQ-20261019-6
- Venue: Science Robotics 2022 (DOI 10.1126/scirobotics.abl6259)
- One-line finding: 750 g platform with a maximum speed of 131 km/h and an onboard GPU (Jetson) for running neural policies at high rate.
- Relevance: background (platform reference; contrast with F450 class).
- Use in: §3.1 table.
- Amit's notes: Highlights 750 g / 131 km/h, onboard GPU, 30 Hz 165° FOV camera.

## D-34 · Agile flight from pixels without state estimation (Geles 2024)
- Source: Zotero `gelesDemonstratingAgileFlight2024`
- Answers: REQ-20261019-6
- Venue: arXiv:2406.12505, 2024 ("Demonstrating" suggests RSS 2024; not verified)
- One-line finding: Pixels map directly to collective thrust and body rates through a gate sequence, at up to 40 km/h and 2 g without explicit state estimation.
- Relevance: background (low-level command interface similar to ours).
- Use in: §3.1 table.
- Amit's notes: none

## D-35 · How fast is too fast? Perception latency in high-speed flight (Falanga 2019)
- Source: Zotero `falangaHowFastToo2019`
- Answers: REQ-20261019-6, REQ-20261019-7
- Venue: IEEE RA-L 2019
- One-line finding: Analytical model linking sensing latency to the maximum safe speed for obstacle avoidance.
- Relevance: supports the "latency, not energy" argument for F450-class drones.
- Use in: §3.5; §3.1 definition of agile.
- Amit's notes: none

(Speeds for the §3.1 table also in D-19 at 5–10 m/s, D-20 at 20 m/s, D-1 at 7.9 m/s SNN, D-40 at 9.8 m/s events.)

---

# REQ-7: energy per operation, SNN energy critiques, chips, drone power

## D-36 · Computing's energy problem (Horowitz 2014)
- Source: to-add (ISSCC 2014 Digest, paper 1.1; PDF verified, Fig. 1.1.9)
- Answers: REQ-20261019-7
- Venue: ISSCC 2014
- One-line finding: Energy at 45 nm, 0.9 V: int add 8b 0.03 pJ, 32b 0.1 pJ; int mult 8b 0.2 pJ, 32b 3.1 pJ; FP add 16b 0.4 pJ, 32b 0.9 pJ; FP mult 16b 1.1 pJ, 32b 3.7 pJ. Cache reads (64-bit): 8 KB 10 pJ, 32 KB 20 pJ, 1 MB 100 pJ; DRAM 1.3–2.6 nJ. A full instruction costs ~70 pJ vs ~0.1 pJ for the add.
- Relevance: background (the E_MAC vs E_AC table; memory dominates).
- Use in: §3.5 energy-per-op table.
- Amit's notes: n/a

## D-37 · Are SNNs really more energy-efficient than ANNs? (Dampfhoffer 2023)
- Source: to-add (DOI 10.1109/tetci.2022.3214509)
- Answers: REQ-20261019-7
- Venue: IEEE TETCI, Jun 2023
- One-line finding: A hardware-aware comparison (Eyeriss-like ANN accelerator vs event-based SNN). IF-neuron SNNs beat efficient ANNs only at very high sparsity, 0.15–1.38 spikes per synapse per inference; LIF costs more than IF.
- Relevance: **threatens** the energy argument as currently stated. It gives the honest threshold to report against our T=5, population-coded (490 input neurons) student.
- Use in: §3.5 caveats.
- Amit's notes: n/a

## D-38 · Are SNNs truly energy-efficient? A hardware perspective (Bhattacharjee 2024)
- Source: to-add (DOI 10.1109/icassp48485.2024.10448269; arXiv:2309.03388)
- Answers: REQ-20261019-7
- Venue: ICASSP 2024
- One-line finding: On a sparsity-aware systolic array (SATA) and on analog crossbars (SpikeSim), measured SNN gains differ significantly from SynOps estimates, due to repeated computation and data movement across timesteps and neuron-module overhead.
- Relevance: background (why SynOps estimates are not enough).
- Use in: §3.5 caveats.
- Amit's notes: n/a

## D-39 · Neuromorphic chip specs: Loihi 2, Speck, SpiNNaker2
- Source: to-add. Loihi 2: Orchard et al., SiPS 2021 (DOI 10.1109/sips52927.2021.00053). Speck: Yao et al., Nat. Commun. 2024 (DOI 10.1038/s41467-024-47811-6). SpiNNaker2: Scholze et al., arXiv:2607.24396 (IEEE OJCAS 2026).
- Answers: REQ-20261019-7
- Venue: as listed
- One-line finding:
  - Loihi 2: up to ~1M neurons and 120M synapses, 128 cores, Intel 4. The 31 mm² die area is from a secondary source (WikiChip). No per-chip power figure found from a primary source.
  - Speck: DVS + SNN SoC, 0.42 mW resting, real-time system power as low as 0.70 mW.
  - SpiNNaker2: 152 PEs (ARM M4F + accelerators), up to 4.5 TOPS INT8 or 2.7 TOPS/W, baseline power below 250 mW.
  - Akida: no primary source verified this run.
- Relevance: background (§3.5 platform table; Objective 1 chip choice).
- Use in: §3.5 compute-platform table.
- Amit's notes: n/a

## D-40 · Approximate imitation learning for event-based flight in clutter (Messikommer 2026)
- Source: Zotero `messikommerApproximateImitationLearning2026` (arXiv:2603.07578; **3 duplicate Zotero items**)
- Answers: REQ-20261019-9, REQ-20261019-3, REQ-20261019-6
- Venue: CoRL 2026
- One-line finding: Representation is learned offline from events; the policy is then fine-tuned online on state only, so no event rendering is needed during RL. Training drops from 52.44 h to 1.86 h (28×). Success 1.0 vs 0.8 for BC, and 0.90 at higher tree density. Real flight through clutter at up to 9.8 m/s from events alone (ANN on Jetson TX2, 11.6 ms). Their vectorised event generator is 34% faster than ESIM-GPU.
- Relevance: **threatens novelty** (Objective 3, partial). Learned event-based clutter flight on a real drone exists, but with an ANN. It is also the method to borrow for the "no event camera in Aerial Gym" risk.
- Use in: §3.7; Objective 3 feasibility.
- Amit's notes: none

## D-41 · A 64 mW DNN visual navigation engine for nano-drones (Palossi 2019)
- Source: to-add (arXiv:1805.01831)
- Answers: REQ-20261019-7
- Venue: IEEE Internet of Things Journal 2019
- One-line finding: DroNet runs on a GAP8 PULP SoC on a Crazyflie at 6 fps within 64 mW (18 fps at peak), using about 3.5% of the nano-drone's power envelope.
- Relevance: supports a measured anchor for the power breakdown. Even on a 27 g nano-drone, CNN compute is a few % of total power, so energy gains in compute only matter where compute is a large share. For an F450 the share is smaller still, which confirms the reviewer's concern; argue latency/mass/heat instead.
- Use in: §3.5 power breakdown figure.
- Amit's notes: n/a

## D-42 · MAVBench: compute's effect on MAV mission energy (Boroujerdian 2018)
- Source: to-add (MICRO 2018, pp. 894–907)
- Answers: REQ-20261019-7
- Venue: IEEE/ACM MICRO 2018
- One-line finding: Closed-loop benchmark showing a non-obvious compute-to-total-energy relation. Faster onboard compute shortens missions (allows higher velocity), improving battery use by up to 1.8×.
- Relevance: supports (the indirect argument: compute latency → speed → mission energy, which applies even when compute power is a small share).
- Use in: §3.5.
- Amit's notes: n/a

---

# REQ-9: event cameras

## D-43 · Event-based vision: a survey (Gallego 2022)
- Source: Zotero `gallegoEventbasedVisionSurvey2022`
- Answers: REQ-20261019-9
- Venue: IEEE TPAMI 44(1), 2022 (arXiv 2019)
- One-line finding: The standard survey: µs latency, >120 dB dynamic range, sparse asynchronous output, and representations (event frames, time surfaces, voxel grids, SNNs).
- Relevance: background.
- Use in: §3.7.
- Amit's notes: 57 highlights; note summarising sensor principle and advantages.

## D-44 · Dynamic obstacle avoidance for quadrotors with event cameras (Falanga 2020)
- Source: Zotero `falangaDynamicObstacleAvoidance2020`
- Answers: REQ-20261019-9
- Venue: Science Robotics 2020 (DOI 10.1126/scirobotics.aaz9712)
- One-line finding: Event-based detection of dynamic obstacles plus a fast avoidance strategy, with 3.5 ms overall latency on a real quadrotor.
- Relevance: background.
- Use in: §3.7.
- Amit's notes: none

## D-45 · EVDodgeNet (Sanket 2020)
- Source: to-add (arXiv:1906.02919)
- Answers: REQ-20261019-9
- Venue: ICRA 2020
- One-line finding: Shallow networks estimate ego-motion and independently moving objects from events, trained in simulation with zero-shot transfer. 70% overall real-world dodging success, all onboard.
- Relevance: background.
- Use in: §3.7.
- Amit's notes: n/a

## D-46 · Monocular event-based vision for obstacle avoidance with a quadrotor (Bhattacharya 2024)
- Source: Zotero `bhattacharyaMonocularEventBasedVision2024` (arXiv:2411.03303)
- Answers: REQ-20261019-9
- Venue: arXiv:2411.03303, Nov 2024 (venue not verified)
- One-line finding: The first static-obstacle avoidance from a monocular event camera. Depth prediction is the pretext task, pre-trained on approximated simulated events and fine-tuned on limited real data. Real avoidance at 5 m/s.
- Relevance: baseline candidate for Objective 3.
- Use in: §3.7.
- Amit's notes: 64 highlights; note on event-camera pros/cons, lack of continuous-time event models in simulation, contributions (first event-driven static avoidance, few-shot sim-to-real, 5 m/s).

## D-47 · ESIM: an open event camera simulator (Rebecq 2018)
- Source: to-add (PMLR 87:969–982)
- Answers: REQ-20261019-9
- Venue: CoRL 2018
- One-line finding: An adaptive-rate renderer coupled to event generation, the standard offline event simulator.
- Relevance: background.
- Use in: §3.7.
- Amit's notes: n/a

## D-48 · v2e: from video frames to realistic DVS events (Hu 2021)
- Source: to-add (arXiv:2006.07722)
- Answers: REQ-20261019-9
- Venue: CVPRW 2021
- One-line finding: Converts frames to events, modelling threshold mismatch, finite intensity-dependent bandwidth and noise. A v2e-trained night-driving detector is ~40% more accurate than a frame-trained YOLOv3.
- Relevance: background.
- Use in: §3.7.
- Amit's notes: n/a

## D-49 · EVIS: real-time event camera simulation in Isaac Sim (Shi 2026)
- Source: to-add (arXiv:2607.08098)
- Answers: REQ-20261019-9
- Venue: arXiv, Jul 2026 (v2 Sep 2026)
- One-line finding: An open-source Isaac Sim plugin generates events from renderer motion vectors and depth (bidirectional warping, depth splatting), in real time across GPU-parallel environments on one GPU. A rotation-speed estimator trained only on EVIS transfers with 2.75 rad/s MAE on real data.
- Relevance: method to borrow. It addresses the Aerial Gym gap if training moves to Isaac Sim/Lab; no Isaac Gym / Aerial Gym event support was found.
- Use in: Objective 3 risk paragraph.
- Amit's notes: n/a

## D-50 · EsaacSim: multimodal event camera add-on for Isaac Sim (Bugueno-Cordova 2026)
- Source: to-add (arXiv:2608.08522)
- Answers: REQ-20261019-9
- Venue: ECCV 2026 Workshop (NeVi)
- One-line finding: Online event simulation in Isaac Sim (grayscale/RGGB) with ROS 2 output. Effective 240–960 Hz event rates, 7–29 ms per frame, <400 MB extra GPU memory on an RTX 4060.
- Relevance: method to borrow (second option).
- Use in: Objective 3 risk paragraph.
- Amit's notes: n/a

(Also in Zotero: `zieglerRealtimeEventSimulation2023`, real-time event simulation from frame cameras, ICRA 2023.)

---

# REQ-10: privileged teacher–student and quadrotor sim-to-real

## D-51 · Learning quadrupedal locomotion over challenging terrain (Lee 2020)
- Source: to-add (DOI 10.1126/scirobotics.abc5986)
- Answers: REQ-20261019-10
- Venue: Science Robotics 2020
- One-line finding: The canonical privileged-teacher → proprioceptive-student (temporal history) pipeline, transferred zero-shot to ANYmal in the wild.
- Relevance: background.
- Use in: §3.3.
- Amit's notes: n/a

## D-52 · Learning by cheating (Chen 2019)
- Source: to-add (arXiv:1912.12294)
- Answers: REQ-20261019-10
- Venue: CoRL 2019
- One-line finding: A privileged agent is distilled into a vision-based driving agent. 100% success on the original CARLA benchmark and a new NoCrash record.
- Relevance: background (origin of the "learning-by-cheating" framing used in D-23).
- Use in: §3.3.
- Amit's notes: n/a

## D-53 · Student-informed teacher training (Messikommer 2025)
- Source: Zotero `messikommerStudentInformedTeacherTraining2025` (arXiv:2412.09149)
- Answers: REQ-20261019-10, REQ-20261019-5
- Venue: arXiv:2412.09149, 2024/2025 (venue not verified)
- One-line finding: The teacher is trained aware of the student's limited observability (e.g. a teacher that sees obstacle distances vs a student that sees only images), to avoid un-imitable teacher behaviour.
- Relevance: method to borrow. Our crash atlas (2/3 of crashes outside the FOV) is exactly the teacher/student observability mismatch it addresses.
- Use in: §3.3; §5.3.
- Amit's notes: none

## D-54 · Sim-to-(multi)-real: robust low-level control across quadrotors (Molchanov 2019)
- Source: to-add (DOI 10.1109/iros40897.2019.8967695)
- Answers: REQ-20261019-10
- Venue: IROS 2019
- One-line finding: A single RL low-level controller, trained with dynamics randomisation, transfers to several different real quadrotors.
- Relevance: background (domain randomisation for quadrotors).
- Use in: §3.3.
- Amit's notes: n/a

## D-55 · What matters in zero-shot sim-to-real RL for quadrotors (Chen 2025)
- Source: Zotero `chenWhatMattersLearning2025` (arXiv:2412.11764)
- Answers: REQ-20261019-10
- Venue: IEEE RA-L 2025
- One-line finding: Identifies five factors for robust zero-shot PPO quadrotor control and packages them in SimpleFlight.
- Relevance: method to borrow (checklist for F450 deployment).
- Use in: §3.3; deployment section.
- Amit's notes: none

(Also in Zotero: `yuDepthTransferLearning2025`, Depth Transfer (VAE depth latent aligned from stereo to sim for drone clutter flight in Isaac Gym), directly relevant to our VAE sim-to-real; `loquercioDeepDroneRacing2020`; `feredeOneNetRule2025`; `aljalboutRealityGapRobotics2025`; `kaufmannBenchmarkComparisonLearned2022`.)

---

Run 2026-10-22: scheduled sync. Zotero ok, no new library items since 2026-10-19 (latest addition 2026-06-18). No open requests; gaps from partial REQ-3 and REQ-7 followed up. Watch search via arXiv API.

# Watch: novelty threats

## D-56 · Event-driven neuromorphic navigation pipeline for MAVs, SNN planner on Loihi (Jiang 2026)
- Source: to-add (arXiv:2610.21978)
- Answers: watch, REQ-20261019-1, REQ-20261019-8
- Venue: arXiv preprint, 15 Oct 2026 (Jiang, Zhou, Fang; Northeastern Univ. Shenyang, same group as Neuro-Planner D-58)
- One-line finding: Prophesee EVK4 events go into a spiking U-Net (depth), then SEW-ResNet features, then a population-coded spiking navigation module. That module outputs a polar waypoint plus velocity and acceleration, and a quintic polynomial turns this into trajectory points for a PX4/Pixhawk controller. It is trained supervised end-to-end with differentiable trajectory losses ("guidance learning", iPlanner/YOPO style) in Flightmare with vid2e events, so there is no RL and no distillation. Sim success SNN vs ANN: 45/48 vs 45/48 at 0.5 m/s, 46/48 vs 47/48 at 1 m/s, 48/48 vs 47/48 at 2 m/s. Real world: 7/10 indoor and 9/10 outdoor, with no real ANN comparison and no real speed reported. Power is 19.57% of the ANN for perception and 12.37% for navigation on Loihi vs Orin NX. The Loihi (Kapoho Bay) is **offboard**: Orin NX → WiFi → x86 host → NxSDK. The perception SNN is simulated on the Orin.
- Relevance: **threatens novelty** of Objective 3. It claims "the first end-to-end event-driven neuromorphic paradigm for MAV visual navigation" and the first physical demonstration. Our remaining differentiators: our policy is a control-level policy rather than a waypoint planner, it runs onboard rather than off-board over WiFi, it is agile (≤2 m/s sim vs our target), and it is RL plus ANN→SNN distillation rather than supervised trajectory loss.
- Use in: §3.6 positioning table (must be a row); Objective 3 novelty statement (drop "first end-to-end neuromorphic drone navigation" and claim onboard, control-level and agile); §3.7.
- Amit's notes: n/a (not in Zotero)

## D-57 · SNN RL with adaptive surrogate gradients and a privileged guide, motor-level control on a real Crazyflie (Van den Berghe 2025)
- Source: to-add (arXiv:2510.24461)
- Answers: watch, REQ-20261019-1, REQ-20261019-2, REQ-20261019-5
- Venue: arXiv preprint, 28 Oct 2025 (Van den Berghe, Stroobants, Janapa Reddi, de Croon; TU Delft)
- One-line finding: Feedforward LIF SNN (18→256→128→4, population encode/decode, soft reset) outputs four motor commands at 100 Hz on a Crazyflie 2.1. A privileged TD3 ANN guide drives the first 50 warm-up steps, and its transitions go into the replay buffer together with a decaying BC term (JSRL-like, not DAgger). Shallower or scheduled surrogate slopes give 2.1× better RL performance. The sim return is 400 vs ≤ −200 for BC and TD3BC. Real flights (figure-8, square, circle): xy error 0.04 m for the SNN vs 0.10 m for an ANN with action history; trajectory error 0.24 vs 0.21 m. **The ANN without action history could not stabilise the drone, but the stateless-input SNN could.** The authors call the SNN less reliable than prior ANN controllers. No neuromorphic chip is used and energy is estimated.
- Relevance: **threatens novelty** (partial) of Objective 1: a second real-flight learned SNN policy from TU Delft, alongside D-1. It does not threaten the clutter/depth claim. It **supports** Objective 2: direct evidence that LIF state replaces explicit action history in real flight control. It is also a method to borrow (guide-policy warm-up for the SNN-from-scratch failure).
- Use in: §3.6 table; Objective 2 motivation (strongest real-hardware evidence for membrane-as-memory); §5.3 distillation (guide plus BC baseline); surrogate-slope choice.
- Amit's notes: n/a (not in Zotero)

## D-58 · Neuro-Planner: SNN actor with hybrid DDPG for depth-camera MAV 3D navigation (Jiang 2022)
- Source: Zotero `jiangNeuroPlanner3DVisual2022` (LLEFN3HT), arXiv:2210.02305
- Answers: watch, REQ-20261019-1 (missed in first sync)
- Venue: arXiv preprint, Oct 2022
- One-line finding: Two-state LIF spiking actor with an ANN critic (hybrid DDPG plus STBP; STBP, BPTT and SLAYER compared) for depth-camera 3D MAV navigation, in software-in-the-loop simulation only. Success rate is 4.3% and 5.3% higher than the original DDPG in two environments. It claims to be the "first … neuromorphic computing and DRL for MAV 3D visual navigation".
- Relevance: **threatens novelty** (partial). It predates us on "SNN policy from a depth camera for MAV navigation in clutter" in simulation. It has no real flight and no distillation.
- Use in: §3.6 table; Objective 1 novelty wording.
- Amit's notes: no annotations; tagged important / Agile Flight / Neuromorphic.

# Watch: perception-aware reward (REQ-4 follow-up)

## D-59 · ClearNav: heading-alignment and lateral-slip rewards for depth-based quadrotor flight (Azad 2026)
- Source: to-add (arXiv:2610.17419)
- Answers: watch, REQ-20261019-4
- Venue: arXiv preprint, 12 Oct 2026
- One-line finding: The authors attribute most collisions in clutter to motion the camera does not see. They add three terms to a differentiable-physics depth policy (Habitat-sim scenes, point-mass dynamics): heading alignment −ŷ_ref·ŷ, lateral slip v_lat²(‖v‖+1), and proximity speed. Over 18 held-out scenarios and 2,304 paired flights, success is +6.8 points and collisions are −65% vs the baseline. The proximity term alone gives −70% collisions. Max speed is 5 m/s, with an onboard Orin NX real flight. Significant on static scenes only.
- Relevance: **threatens novelty** of p_fov as a contribution. It is near-identical in spirit: keep motion inside the FOV. It also gives a citable quantitative precedent.
- Use in: reward-design section (cite next to Song 2023 D-23); downgrade p_fov from contribution to design choice.
- Amit's notes: n/a

# REQ-3 follow-up: NTNU deep-collision-prediction line

## D-60 · Motion-primitives navigation using deep collision prediction (Nguyen 2022)
- Source: to-add (arXiv:2201.03254, DOI 10.1109/ICRA46639.2022.9812231)
- Answers: REQ-20261019-3
- Venue: ICRA 2022
- One-line finding: A network predicts collision cost for each motion-primitive sequence from the depth image and the estimated velocities, with the Unscented Transform and MC dropout for uncertainty. It is validated in sim, lab and field. The abstract gives no numbers. This is very likely the paper the NTNU group calls ORACLE, but the abstract does not use the name, so this is unconfirmed.
- Relevance: background (lineage of the DCE used by Kulkarni D-18 and by our VAE).
- Use in: §3.2 learned navigation in clutter.
- Amit's notes: n/a

## D-61 · seVAE: semantically-enhanced deep collision prediction (Kulkarni 2023)
- Source: to-add (arXiv:2307.11522, DOI 10.1109/IROS55552.2023.10342297)
- Answers: REQ-20261019-3
- Venue: IROS 2023
- One-line finding: A semantically-enhanced VAE compresses depth while preserving thin obstacles, and a 3D collision-prediction network scores motion primitives. It is map-free and needs no full pose, it is tested in sim and real, and it beats an end-to-end baseline. The abstract gives no numbers. Code: github.com/ntnu-arl/sevae.
- Relevance: method to borrow / background (direct ancestor of our collision-aware depth VAE).
- Use in: §3.2; VAE method section.
- Amit's notes: n/a

# REQ-7 follow-up: Akida

## D-62 · Akida AKD1000 measured energy per inference (Kaczmarek 2026)
- Source: to-add (arXiv:2603.13880)
- Answers: REQ-20261019-7
- Venue: STEAR 2026 workshop @ HiPEAC 2026
- One-line finding: Robustness benchmark on the BrainChip AKD1000 (28 nm, 80 NPUs) reports about 45 µJ per inference for the defended network. BrainChip's own AKD1000 product brief gives a 300 MHz max clock and no wattage figure. The AKD1500 is vendor-rated at 800 GOPS and <300 mW, according to a CNX Software report that has not been checked against a primary source.
- Relevance: background (only measured Akida number found; weak source).
- Use in: §3.5 chip-spec table, Akida row (mark as workshop and vendor figures).
- Amit's notes: n/a

---

Run 2026-10-26: scheduled sync. Zotero ok, no new library items (latest addition is still 2026-06-18). Feeds were not checked because no feed tool was available. No open requests. The watch search (arXiv API, 6 queries) found only one paper submitted after 2026-10-22: DiffDreamer, arXiv:2610.31617, world model plus differentiable sim for agile tracking and racing. It has no clutter or SNN component and was skipped. The two entries below are from 6–11 Oct and were missed on 10-22. There are no novelty threats.

# Watch: learned navigation in clutter (REQ-3 / REQ-6 benchmarks)

## D-63 · Stereo-Planner: stereo RGB to trajectory, zero-shot sim-to-real (Shen 2026)
- Source: to-add (arXiv:2610.15560)
- Answers: watch, REQ-20261019-3, REQ-20261019-6
- Venue: arXiv preprint, 11 Oct 2026 (Lihua Xie group, NTU)
- One-line finding: The planner turns stereo RGB images straight into a trajectory. It uses a pretrained vision-grounding scene representor and an attention trajectory decoder, trained only in simulation on differentiable trajectory costs (no RL). Results: 95% sim success at 8 m/s, real flight up to 7 m/s on a compact quadrotor, 24.27 ms mean inference on an Orin NX. Competitive with depth-based planners.
- Relevance: baseline candidate (an external speed/success/latency number for the "agile" definition, and a contrast to our depth-VAE plus RL).
- Use in: §3.1 agile-flight table; teacher benchmark discussion.
- Amit's notes: n/a

## D-64 · Sensor-layout-agnostic RL navigation via spherical range canonicalization (Rehberg & Alexis 2026)
- Source: to-add (arXiv:2610.08306)
- Answers: watch, REQ-20261019-3
- Venue: arXiv preprint, 6 Oct 2026 (NTNU ARL, the Aerial Gym / DCE group)
- One-line finding: Depth from any camera layout is merged into one robot-centric spherical range image with a validity mask, and an RL policy is trained with heavy camera randomization. It transfers zero-shot to layouts with up to 7 cameras, and success goes from 78% to 95% as coverage grows. Real flights were done in a cluttered corridor and a forest, including sensor dropouts. The abstract does not name the simulator.
- Relevance: background / method to borrow. Blind-spot masking is relevant to our limited-FOV problem (p_fov, Objective 2), and the success-vs-coverage curve quantifies how FOV limits success.
- Use in: §3.2; Objective 2 motivation (FOV limits success).
- Amit's notes: n/a
