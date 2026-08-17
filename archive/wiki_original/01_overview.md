# 01 — SYSTEM OVERVIEW

## Philosophy

**"Ptolemy speaks because he knows."**

Ainulindale Engine is a modular derivation, visualisation, and sonification system for the SMNNIP (Standard Model of Neural Network Information Propagation) framework and the Ainulindale Conjecture.

It is not a machine learning framework. It is a mathematical engine. Every output is a derivation. Every sound is a computation. Every address is a coordinate.

## What it is not

- Not a transformer. Not an LLM.
- Not a training loop. No backpropagation here.
- Not a statistics engine. Results are exact or they are labelled CONJECTURE.

## Architecture

```
ainulindale_engine/
├── engine/
│   ├── registry.py        Module registry — the contract
│   ├── constants.py       Single source of truth for all constants
│   ├── units.py           Radian-primary unit transforms
│   ├── console_qt.py      Qt viewer (Phase 3)
│   └── console_curses.py  Curses console — Ptolemy /derivation
├── modules/
│   ├── inversion/         (I|O) map, phi attractor, d* gap
│   ├── lagrangian/        L_NN four terms, running coupling, RG flow
│   ├── noether/           ∂_μJ^μ, blockchain ledger, resonance artifacts
│   ├── noether_information/ J_info, entropic arrow, information capacity
│   ├── berry_keating/     H_NN, d* workbench, T map scaffold
│   ├── sonification/      ω = pitch, wavetables, quasi-particle rests
│   ├── hyperwebster/      Horner bijection, Fano address, SemanticWord
│   └── jwst/              8 NIRCam filters → 𝕆 element
└── __main__.py            Entry point, arg routing, module registration
```

## The Cayley-Dickson Tower

All mathematics lives in the tower:

```
ℝ (dim 1)  →  ℂ (dim 2)  →  ℍ (dim 4)  →  𝕆 (dim 8)  →  𝕊 (dim 16, boundary)
 U(0)/trivial   U(1)           SU(2)          G₂/SU(3)      [zero-divisors]
```

Each step up loses one algebraic property:
- ℝ → ℂ: ordering
- ℂ → ℍ: commutativity
- ℍ → 𝕆: associativity
- 𝕆 → 𝕊: zero-divisors appear (sedenion boundary — training stops here)

The lost property **is** the signal. It encodes the gauge structure of that layer.

**Two currents flow in opposite directions through the tower:**

- **Noether Current J^μ (forward: ℝ→𝕆):** Synthesis — the Builder. Complexity escalation. The `hear()` function.
- **Noether Information Current J_info (backward: 𝕆→ℝ):** Distillation — the Evaluator. Dimensional reduction to the prime. The `speak()` function.

Where they meet, meaning crystallises. The prime that forms at the intersection is the semantic unit. This counter-rotation is the Riemann-Fermat Heartbeat.

→ [Wiki: Cayley-Dickson Tower (full treatment)](19_cayley_dickson_tower.md)

## The (I|O) Inversion Map

The 2-stroke engine at the core of SMNNIP:

```
J_N: (r, θ) → (1/r, θ + π/2)
```

- Compression stroke: r → 1/r
- Expansion stroke: 1/r → r
- Fixed point: r = 1 (the horizon)
- Recursion attractor: r = φ (golden ratio)
- Sedenion: top dead center — engine seized, one-way ratchet

## The Ainulindale Lagrangian

```
L_NN = (2/π) ∮ [L_kin + L_mat + (1/φ)·L_bias + L_coup] r dr dθ
```

Four terms in exact analogy with the Standard Model:
- L_kin: gauge field kinetic term (Yang-Mills)
- L_mat: matter kinetic term (Dirac)
- L_bias: Higgs/Mexican hat potential (SSB when μ² < 0)
- L_coup: Yukawa coupling (scaled by 1/φ — corrected April 13 2026)

## Entry Points

```bash
python3 -m ainulindale_engine --info       # print registry and exit
python3 -m ainulindale_engine --qt         # Qt viewer + VisPy + QTermWidget
python3 -m ainulindale_engine --curses     # curses console (Ptolemy /derivation)
python3 -m ainulindale_engine --headless   # no GUI, text output
```

## Ptolemy Integration

The curses mode (`--curses`) is the `/derivation` shortcut in Ptolemy.
When PtolBus is live, ainulindale_engine will be wired as a Philadelphos submodule.
The Qt viewer runs standalone or as a detached Ptolemy window.

## Versioning

All files start at v0.111. Increment 0.001 per change.
Previous versions move to `.archive/` (git-ignored).
Commit format: `YYYY-MM-DD: [file] — [one-line context]`
The commit message is the Arrow of Time for the codebase.
