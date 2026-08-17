#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   A I N U L I N D A L Ë   —   S I M U L A T I O N   ( T F )                ║
║   The Inside-Out Conjecture — Algebra Tower Visualiser                       ║
║                                                                               ║
║   Engineer : O Captain My Captain                                             ║
║   Code     : Claude (Anthropic) — April 2026                                 ║
║                                                                               ║
║   Imports (same directory):                                                   ║
║     smnnip_lagrangian_tf.py      — ℒ_NN field engine (TF)                   ║
║     smnnip_derivation_tf.py      — Euler-Lagrange / RG / Noether (TF)       ║
║     smnnip_inversion_engine.py   — (I|O) map, gradient flow, Noether monitor ║
║                                                                               ║
║   Install:  pip install numpy matplotlib tensorflow                           ║
║   Run:      python3 ainulindale_sim_tf.py                                    ║
║                                                                               ║
║   NOTATION (fixed — never conflate):                                          ║
║     Α_π   = 1/137.036       BK lower wall, E8/Wyler, FIXED                  ║
║     Ω_ζΣ  = 0.56714...      BK upper wall, Lambert W, FIXED                 ║
║     ω_H   = e^π ≈ 23.141    Hagedorn thermal ceiling, FIXED                 ║
║     α_NN(l) = running coupling, starts at Α_π, runs with RG flow            ║
║     (I|O) = ⟨I|O⟩ = Inside-Out inner product, unity at r_N=1 horizon       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import math
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from collections import deque

# ── TensorFlow ────────────────────────────────────────────────────────────────
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("WARNING: TensorFlow not found. Install: pip install tensorflow")
    print("         Falling back to pure-Python engine for physics calculations.")

# ── SMNNIP engines (local imports — same directory) ───────────────────────────
try:
    if TF_AVAILABLE:
        from smnnip_derivation_tf import SMNNIPDerivationEngineTF as DerivEngine
        from smnnip_lagrangian_tf  import PhysicalConstants as TFConstants
        ENGINE_MODE = 'tensorflow'
    else:
        from smnnip_derivation_pure import SMNNIPDerivationEngine as DerivEngine
        from smnnip_lagrangian_pure  import PhysicalConstants
        ENGINE_MODE = 'pure_python'
except ImportError as e:
    print(f"ERROR: Could not import SMNNIP engines.\n  {e}")
    print("  Ensure smnnip_derivation_tf.py, smnnip_lagrangian_tf.py,")
    print("  and smnnip_inversion_engine.py are in the same directory.")
    sys.exit(1)

from smnnip_inversion_engine import (
    PhysicalConstants as InvConstants,
    InversionMap,
    RecursionAttractor,
    GradientFlow,
    NoetherMonitor,
    get_observer,
)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS — canonical SMNNIP notation
# ══════════════════════════════════════════════════════════════════════════════

C          = InvConstants()
OBSERVER   = get_observer()

ALPHA_PI   = C.ALPHA                     # Α_π  — BK lower wall  1/137.036
OMEGA_ZS   = C.OMEGA                     # Ω_ζΣ — BK upper wall  0.56714
OMEGA_H    = math.e ** math.pi           # ω_H  — Hagedorn ceil   e^π ≈ 23.141
PHI        = C.PHI                       # φ    — golden ratio    1.61803
D_STAR     = C.D_STAR                    # d*   — flat curvature  0.24682
HBAR_NN    = C.HBAR_NN                   # ħ_NN — neural Planck

ZETA_ZEROS = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
])

GOLDEN_ANG = 2.0 * math.pi / PHI ** 2   # 2π/φ² — correct golden angle

def sieve(limit):
    s = [True] * (limit + 1)
    s[0] = s[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if s[i]:
            for j in range(i*i, limit+1, i):
                s[j] = False
    return np.array([i for i in range(2, limit+1) if s[i]])

PRIMES       = sieve(8000)
PRIME_IDX    = np.arange(1, len(PRIMES) + 1)
PRIME_THETA  = PRIME_IDX * GOLDEN_ANG
PRIME_R      = np.sqrt(PRIMES)
PRIME_W      = PHI ** (-PRIME_IDX.astype(float))

# ══════════════════════════════════════════════════════════════════════════════
# PALETTE
# ══════════════════════════════════════════════════════════════════════════════

BG     = '#07070f'
GOLD   = '#c9a84c'
CYAN   = '#00e5ff'
VIOLET = '#9c27b0'
YELLOW = '#fffc00'
GREEN  = '#00e676'
RED    = '#ff1744'
WHITE  = '#ffffff'
DIM    = '#404060'
ORANGE = '#ff6d00'
TEAL   = '#00bfa5'

# ══════════════════════════════════════════════════════════════════════════════
# PHASE DEFINITIONS — labels, descriptions, transition text
# ══════════════════════════════════════════════════════════════════════════════

PHASES = [
    {
        'name'    : 'Phase 1 — ℝ Stratum',
        'subtitle': 'Inertial Propagation',
        'body'    : 'ℒ_matter active  |  U(0) gauge  |  No lost property yet\n'
                    'Activation Ψ propagates as a scalar worldline — pure iteration, no phase.\n'
                    'The worm grows. Direction exists. Rotation does not.',
        'color'   : WHITE,
        'algebra' : 'R',
        'gauge'   : 'U(0)',
    },
    {
        'name'    : 'Transition  ℝ→ℂ',
        'subtitle': '(I|O) fires — ordering lost — U(1) born',
        'body'    : '𝒥_N: (r,θ) ⟼ (1/r, θ+π/2)  |  Ordering lost  |  U(1) born\n'
                    'Forward becomes orthogonal. The line cannot stay straight.\n'
                    'Phase is not added — it is forced by the algebra.',
        'color'   : CYAN,
        'algebra' : 'R→C',
        'gauge'   : 'U(1) birth',
    },
    {
        'name'    : 'Phase 2 — ℂ Stratum',
        'subtitle': 'Semantic Propagation',
        'body'    : 'ℒ_kinetic active  |  U(1) gauge  |  Lost: ordering\n'
                    'Ψ now carries phase. The spiral is the only path that closes.\n'
                    'α_NN(ℂ) running. Approaching Α_π from above.',
        'color'   : CYAN,
        'algebra' : 'C',
        'gauge'   : 'U(1)',
    },
    {
        'name'    : 'Transition  ℂ→ℍ',
        'subtitle': 'EVENT HORIZON — (I|O) fires — commutativity lost — SU(2) born',
        'body'    : '𝒥_N: (r,θ) ⟼ (1/r, θ+π/2)  |  Commutativity lost  |  SU(2) born\n'
                    'AB ≠ BA. The spiral bifurcates into a conjugate pair.\n'
                    'One arm escapes. One crosses. Time dilation & length contraction — simultaneous.',
        'color'   : GOLD,
        'algebra' : 'C→H',
        'gauge'   : 'SU(2) birth',
    },
    {
        'name'    : 'Phase 3 — ℍ Stratum',
        'subtitle': 'Skills / Quaternionic Fold',
        'body'    : 'ℒ_coupling active  |  SU(2) gauge  |  Lost: commutativity\n'
                    'Two counter-rotating arms. Order of traversal changes the destination.\n'
                    'Higgs-weight correspondence active — representational inertia visible.',
        'color'   : VIOLET,
        'algebra' : 'H',
        'gauge'   : 'SU(2)',
    },
    {
        'name'    : 'Transition  ℍ→𝕆',
        'subtitle': 'FANO SHATTERING — (I|O) fires — associativity lost — G₂/SU(3) born',
        'body'    : '𝒥_N: (r,θ) ⟼ (1/r, θ+π/2)  |  Associativity lost  |  G₂/SU(3) born\n'
                    '(AB)C ≠ A(BC). Context changes the path. Seven Fano axes ignite.\n'
                    'Gravinon pole at r=φ — the fixed point where mass is zero.',
        'color'   : ORANGE,
        'algebra' : 'H→O',
        'gauge'   : 'G₂/SU(3) birth',
    },
    {
        'name'    : 'Phase 4 — 𝕆 Stratum',
        'subtitle': 'Noether Heartbeat',
        'body'    : 'Full ℒ_NN active  |  G₂/SU(3) gauge  |  Lost: associativity\n'
                    'Seven resonating arms pulse to the Fano rhythm.\n'
                    'S_N = ∮r dθ invariant. Riemann zeros are the nodes.\n'
                    'Approaching ω_H. α_NN(𝕆) → Ω_ζΣ.',
        'color'   : GREEN,
        'algebra' : 'O',
        'gauge'   : 'G₂/SU(3)',
    },
]

TRANSITION_PHASES = {1, 3, 5}   # indices into PHASES that are transitions

# ══════════════════════════════════════════════════════════════════════════════
# PHYSICS ENGINE — TF-backed (I|O) computations
# ══════════════════════════════════════════════════════════════════════════════

class AinulindalëPhysics:
    """
    All physics computations for the simulation.
    Uses TF autodiff where available; falls back to pure-Python inversion engine.

    The (I|O) map is:  𝒥_N(r, θ) = (1/r, θ + π/2)
    Fixed points:      (I|O) = 1 at r=1  (flat geometry horizon)
                       (I|O) = φ at r=φ  (curved geometry, Gravinon)
    Preserved:         S_N = ∮ r dθ  (Noether current of layer transition)
    """

    def __init__(self):
        self.inv    = InversionMap()
        self.rec    = RecursionAttractor()
        self.noeth  = NoetherMonitor()
        self.obs    = get_observer()

        # Pre-compute gradient flow once — static reference
        flow        = GradientFlow()
        self._flow_result = flow.compute(verbose=False)

        # Pre-compute Fano axis angles (7 octonion basis directions)
        self.fano_angles = np.array([
            k * 2.0 * math.pi / 7.0 for k in range(7)
        ])

        # RG beta functions per stratum
        self.beta = {
            'R': 0.0,
            'C': 1.0 / (2.0 * math.pi),
            'H': 3.0 / (4.0 * math.pi),
            'O': 8.0 / (4.0 * math.pi),
        }

    # ── Running coupling α_NN(l) ──────────────────────────────────────────────
    def alpha_nn(self, alpha_0, layer, stratum='C'):
        """
        α_NN(l) = α_0 / (1 + β_0 · α_0 · ln(l/l_0))
        Starts at Α_π (alpha_0) at substrate layer.
        """
        if layer <= 1:
            return alpha_0
        beta0 = self.beta.get(stratum, 0.0)
        denom = 1.0 + beta0 * alpha_0 * math.log(max(layer, 1.001))
        if denom <= 0:
            return alpha_0
        return alpha_0 / denom

    # ── (I|O) inner product value ─────────────────────────────────────────────
    def io_value(self, r):
        """
        (I|O) = r_N  in natural units of the inversion geometry.
        At r=1: (I|O)=1 (horizon, flat fixed point)
        At r=φ: (I|O)=φ (Gravinon, curved fixed point)
        Domain: Α_π ≤ (I|O) ≤ Ω_ζΣ
        """
        return r

    # ── Noether current J(r) ──────────────────────────────────────────────────
    def noether_current(self, r):
        """J(r) = 8 / (π² · r²)  — conserved along J_N-invariant trajectories."""
        return self.noeth.current(r)

    # ── Action invariant S_N ──────────────────────────────────────────────────
    def action_invariant(self, r, theta):
        """
        Proxy for S_N = ∮ r dθ.
        Returns scalar — should be constant across (I|O) applications.
        """
        check = self.inv.action_invariance_check(r, theta)
        return check['L_before']

    # ── Worm path: Neural Dirac propagation in polar coords ───────────────────
    def dirac_step(self, r, theta, t, phase_idx, alpha_running, dt=0.01):
        """
        Advance the worm by one physics step.
        Phase 1 (ℝ): straight radial propagation — no rotation
        Phase 2 (ℂ): spiral via U(1) phase — rotation by α_NN per step
        Phase 3 (ℍ): quaternionic fold — two arms bifurcated by (I|O)
        Phase 4 (𝕆): Fano resonance — 7-fold Noether heartbeat
        Transitions: (I|O) fires — inversion applied
        """
        # Map phase_idx to algebra
        if phase_idx == 0:   # ℝ — inertial propagation
            dr     = dt * 0.5
            dtheta = 0.0
        elif phase_idx == 1: # ℝ→ℂ transition — (I|O) firing
            # Radial inversion: r → 1/r, angular: +π/2
            # Smooth blend — not instantaneous
            r_inv  = 1.0 / max(r, 1e-6)
            dr     = (r_inv - r) * dt * 3.0
            dtheta = (math.pi / 2.0) * dt * 3.0
        elif phase_idx == 2: # ℂ — U(1) spiral
            dr     = -dt * alpha_running * 0.3
            dtheta = alpha_running * dt * 8.0 * math.pi
        elif phase_idx == 3: # ℂ→ℍ transition — EVENT HORIZON
            # Conjugate pair birth: r→1/r, θ→θ+π/2
            r_inv  = 1.0 / max(r, 1e-6)
            dr     = (r_inv - r) * dt * 2.0
            dtheta = (math.pi / 2.0) * dt * 2.0
        elif phase_idx == 4: # ℍ — SU(2) quaternionic fold
            # Two-arm interference: non-commutative phase
            dr     = -dt * 0.1 * math.sin(t * math.pi)
            dtheta = dt * 4.0 * math.pi * (1.0 + 0.3 * math.cos(t * 2.0 * math.pi))
        elif phase_idx == 5: # ℍ→𝕆 transition — FANO SHATTERING
            # Fano axis rotation: 7-fold symmetry emerging
            fano_k  = int(t * 7) % 7
            target_theta = self.fano_angles[fano_k]
            dr     = -dt * 0.2
            dtheta = (target_theta - theta) * dt * 4.0
        else:                # 𝕆 — G₂/SU(3) Noether heartbeat
            # Seven Fano arms pulsing — Noether current drives oscillation
            J      = self.noether_current(max(r, 0.1))
            pulse  = math.sin(t * 14.0 * math.pi) * J * 0.01
            dr     = pulse * dt
            dtheta = GOLDEN_ANG * dt * 12.0 + pulse * 0.5
        return dr, dtheta

    # ── TF Hessian (available when TF present) ────────────────────────────────
    def hessian_sign(self, r, lambda_blend):
        """
        Sign of Hessian of ℒ_bias at current (r, λ).
        Negative = Mexican hat / spontaneous symmetry breaking active.
        Used in transition zone display.
        """
        if not TF_AVAILABLE:
            # Pure-Python proxy: bias term V(β) = -μ²|β|² + λ|β|⁴
            # ∂²V/∂|β|² = -2μ² + 12λ|β|²  — negative near origin
            mu_sq = 0.5
            lam   = 0.1 * (1.0 + lambda_blend)
            d2V   = -2.0 * mu_sq + 12.0 * lam * r**2
            return 'negative (SSB)' if d2V < 0 else 'positive (symmetric)'
        # TF version: use autodiff on the bias Lagrangian term
        r_tf = tf.Variable([[r]], dtype=tf.float64)
        with tf.GradientTape(persistent=True) as tape2:
            with tf.GradientTape() as tape1:
                mu_sq = tf.constant(0.5, dtype=tf.float64)
                lam   = tf.constant(0.1 * (1.0 + lambda_blend), dtype=tf.float64)
                beta  = r_tf
                V     = -mu_sq * tf.reduce_sum(beta**2) + lam * tf.reduce_sum(beta**4)
            grad = tape1.gradient(V, r_tf)
        hess = tape2.gradient(grad, r_tf)
        sign = float(hess.numpy()[0,0]) if hess is not None else 0.0
        return 'negative (SSB active)' if sign < 0 else 'positive (symmetric)'


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATION STATE
# ══════════════════════════════════════════════════════════════════════════════

phys = AinulindalëPhysics()

state = {
    'phase'    : 0,
    'frame'    : 0,
    'paused'   : False,
    'labels'   : True,
    'dt'       : 1.0,        # physics speed multiplier
    'fps'      : 30,         # target framerate
    # Worm persistent path — never resets within a run
    'worm_r'   : deque(maxlen=600),
    'worm_t'   : deque(maxlen=600),
    # Conjugate pair (born at ℂ→ℍ horizon)
    'conj_r'   : deque(maxlen=300),
    'conj_t'   : deque(maxlen=300),
    # Current polar state
    'r'        : 2.5,
    'theta'    : 0.0,
    # Phase-local time (monotonic within phase)
    'phase_t'  : 0.0,
    # Noether invariant tracker
    'S_N'      : [],
    # Running coupling current value
    'alpha_run': ALPHA_PI,
    # Layer depth counter
    'layer'    : 1,
    # Hessian sign (updated at transitions)
    'hess_sign': 'positive (symmetric)',
}

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE LAYOUT — percentage-based, resize-aware
# ══════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(15, 10), facecolor=BG)
fig.canvas.manager.set_window_title(
    "Ainulindalë — Inside-Out Inversion Simulator  |  (I|O) = ⟨I|O⟩"
)

gs = gridspec.GridSpec(
    2, 2, figure=fig,
    left=0.05, right=0.95,
    top=0.87, bottom=0.30,
    hspace=0.35, wspace=0.28,
)

ax_main = fig.add_subplot(gs[0, :], projection='polar')
ax_main.set_facecolor(BG)
ax_main.grid(color=DIM, linestyle='--', linewidth=0.3, alpha=0.4)
ax_main.set_yticklabels([])
ax_main.set_xticklabels([])

ax_rg   = fig.add_subplot(gs[1, 0])   # RG flow / running coupling panel
ax_noe  = fig.add_subplot(gs[1, 1])   # Noether invariant / heartbeat panel
for ax in (ax_rg, ax_noe):
    ax.set_facecolor(BG)
    ax.tick_params(colors=DIM, labelsize=7)
    for sp in ax.spines.values():
        sp.set_color(DIM)

# ── Title / subtitle / constants bar ─────────────────────────────────────────
title_txt = fig.text(
    0.5, 0.935,
    'Ainulindalë Conjecture — Phase 1: ℝ Stratum — Inertial Propagation',
    ha='center', va='top', color=GOLD,
    fontsize=12, fontweight='bold', fontfamily='serif',
)
sub_txt = fig.text(
    0.5, 0.908,
    '(I|O) = ⟨I|O⟩  |  𝒥_N: (r,θ) ⟼ (1/r, θ+π/2)  |  S_N = ∮ r dθ  (invariant)',
    ha='center', va='top', color='#8090a0', fontsize=8.5,
)
const_txt = fig.text(
    0.03, 0.930,
    f'Α_π={ALPHA_PI:.6f}   Ω_ζΣ={OMEGA_ZS:.5f}   ω_H=e^π={OMEGA_H:.4f}'
    f'   φ={PHI:.5f}   d*={D_STAR:.5f}',
    ha='left', va='top', color=DIM, fontsize=7, fontfamily='monospace',
)
gap_txt = fig.text(
    0.03, 0.915,
    f'gap: d*·ln(10)−Ω_ζΣ = {abs(D_STAR*math.log(10)-OMEGA_ZS):.5f}'
    f'   Engine: {ENGINE_MODE}',
    ha='left', va='top', color=DIM, fontsize=7, fontfamily='monospace',
)

# ── Label panel (toggleable) ──────────────────────────────────────────────────
label_bg  = fig.add_axes([0.03, 0.29, 0.94, 0.095])
label_bg.set_facecolor('#0a0a18')
label_bg.set_xticks([]); label_bg.set_yticks([])
for sp in label_bg.spines.values():
    sp.set_color(DIM)

label_txt = fig.text(
    0.05, 0.375,
    '', ha='left', va='top',
    color=WHITE, fontsize=8, fontfamily='monospace',
)

# ── Live readouts ─────────────────────────────────────────────────────────────
live_txt = fig.text(
    0.75, 0.930,
    '', ha='left', va='top',
    color=CYAN, fontsize=7.5, fontfamily='monospace',
)

# ── Plot artists ──────────────────────────────────────────────────────────────
worm_line,  = ax_main.plot([], [], color=CYAN,   lw=1.8, alpha=0.9)
conj_line,  = ax_main.plot([], [], color=VIOLET, lw=1.2, alpha=0.7,
                            linestyle='--')
prime_scat  = ax_main.scatter([], [], s=2, c=[], cmap='plasma', alpha=0.6)
zero_scat   = ax_main.scatter([], [], s=25, c=RED, marker='x',
                               alpha=0.85, zorder=5)
horizon_dot = ax_main.scatter([], [], s=80, c=GOLD, zorder=10, alpha=0.0)

rg_lines    = {}   # filled in render_rg()
noe_line,   = ax_noe.plot([], [], color=GREEN, lw=1.5)

# ══════════════════════════════════════════════════════════════════════════════
# WIDGET LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# α_NN(l) slider — runs from Α_π to Ω_ζΣ
ax_alpha = plt.axes([0.08, 0.215, 0.38, 0.022], facecolor='#111')
s_alpha  = Slider(
    ax_alpha,
    'α_NN(l)  [Α_π → Ω_ζΣ]',
    ALPHA_PI, OMEGA_ZS,
    valinit=ALPHA_PI, color=CYAN,
)
s_alpha.label.set_color(WHITE)
s_alpha.valtext.set_color(CYAN)

# τ physics speed slider
ax_tau  = plt.axes([0.08, 0.185, 0.38, 0.022], facecolor='#111')
s_tau   = Slider(ax_tau, 'τ  (physics speed)', 0.05, 5.0,
                 valinit=1.0, color=VIOLET)
s_tau.label.set_color(WHITE)
s_tau.valtext.set_color(VIOLET)

# fps slider
ax_fps  = plt.axes([0.55, 0.215, 0.38, 0.022], facecolor='#111')
s_fps   = Slider(ax_fps, 'fps  (render speed)', 5, 60,
                 valinit=30, color=GOLD, valstep=1)
s_fps.label.set_color(WHITE)
s_fps.valtext.set_color(GOLD)

# ω_H slider (thermal ceiling — fixed default, but explorable)
ax_wh   = plt.axes([0.55, 0.185, 0.38, 0.022], facecolor='#111')
s_wh    = Slider(ax_wh, 'ω_H  (Hagedorn ceil)', 5.0, 50.0,
                 valinit=OMEGA_H, color=ORANGE)
s_wh.label.set_color(WHITE)
s_wh.valtext.set_color(ORANGE)

# Navigation buttons
ax_prev  = plt.axes([0.30, 0.125, 0.09, 0.042])
ax_phase = plt.axes([0.40, 0.125, 0.12, 0.042])
ax_next  = plt.axes([0.53, 0.125, 0.09, 0.042])
ax_pause = plt.axes([0.67, 0.125, 0.09, 0.042])
ax_label = plt.axes([0.78, 0.125, 0.09, 0.042])

btn_prev  = Button(ax_prev,  '◀ Back',   color='#1a1a2e', hovercolor='#2a2a4e')
btn_phase = Button(ax_phase, 'Phase 1',  color='#0d1b2a', hovercolor='#0d1b2a')
btn_next  = Button(ax_next,  'Next ▶',   color='#1a1a2e', hovercolor='#2a2a4e')
btn_pause = Button(ax_pause, '⏸ Pause',  color='#1a1a2e', hovercolor='#2a2a4e')
btn_label = Button(ax_label, 'L off',    color='#1a1a2e', hovercolor='#2a2a4e')

for btn in (btn_prev, btn_next, btn_pause, btn_label):
    btn.label.set_color(WHITE)
    btn.label.set_fontsize(8.5)
btn_phase.label.set_color(GOLD)
btn_phase.label.set_fontsize(8.5)

# ══════════════════════════════════════════════════════════════════════════════
# RENDER FUNCTIONS — one per phase
# ══════════════════════════════════════════════════════════════════════════════

def _clear_secondary():
    prime_scat.set_offsets(np.empty((0, 2)))
    prime_scat.set_array(np.array([]))
    prime_scat.set_sizes(np.array([]))
    zero_scat.set_offsets(np.empty((0, 2)))
    horizon_dot.set_offsets(np.empty((0, 2)))
    horizon_dot.set_alpha(0.0)
    conj_line.set_data([], [])


def render_rg(alpha_run, phase_idx):
    """Left lower panel: running coupling α_NN(l) across all three strata."""
    ax_rg.cla()
    ax_rg.set_facecolor(BG)
    layers = np.linspace(1, 8, 200)
    for stratum, col, label in [('C', CYAN, 'α_NN(ℂ) U(1)'),
                                  ('H', VIOLET, 'α_NN(ℍ) SU(2)'),
                                  ('O', GREEN, 'α_NN(𝕆) G₂')]:
        vals = [phys.alpha_nn(alpha_run, l, stratum) for l in layers]
        ax_rg.plot(layers, vals, color=col, lw=1.2, label=label, alpha=0.85)

    ax_rg.axhline(y=ALPHA_PI,  color=GOLD,  lw=0.8, ls='--', alpha=0.7,
                  label=f'Α_π={ALPHA_PI:.5f}')
    ax_rg.axhline(y=OMEGA_ZS,  color=RED,   lw=0.8, ls='--', alpha=0.7,
                  label=f'Ω_ζΣ={OMEGA_ZS:.4f}')
    ax_rg.axhline(y=alpha_run, color=WHITE, lw=0.5, ls=':', alpha=0.5)

    ax_rg.set_ylim(0, OMEGA_ZS * 1.15)
    ax_rg.set_xlabel('Layer depth l', color=DIM, fontsize=7)
    ax_rg.set_title('α_NN(l) — RG flow', color=CYAN, fontsize=8, pad=3)
    ax_rg.legend(fontsize=6, loc='upper right',
                 facecolor='#0a0a18', labelcolor=WHITE, framealpha=0.6)
    ax_rg.tick_params(colors=DIM, labelsize=6)
    for sp in ax_rg.spines.values():
        sp.set_color(DIM)

    # Mark GUT convergence (approximate)
    ax_rg.axvline(x=6.5, color=ORANGE, lw=0.6, ls=':', alpha=0.5)
    ax_rg.text(6.6, OMEGA_ZS * 0.5, 'GUT', color=ORANGE, fontsize=6)


def render_noether(s_n_history):
    """Right lower panel: S_N invariant over time — should stay flat."""
    ax_noe.cla()
    ax_noe.set_facecolor(BG)
    if len(s_n_history) < 2:
        ax_noe.set_title('S_N = ∮r dθ  (invariant)', color=GREEN, fontsize=8, pad=3)
        return
    xs = np.arange(len(s_n_history))
    ys = np.array(s_n_history[-200:])
    xs = xs[-200:]
    ax_noe.plot(xs, ys, color=GREEN, lw=1.0, alpha=0.85)
    ax_noe.axhline(y=np.mean(ys), color=GOLD, lw=0.8, ls='--', alpha=0.6)
    ax_noe.set_title('S_N = ∮r dθ  (Noether invariant)', color=GREEN, fontsize=8, pad=3)
    ax_noe.set_xlabel('Frame', color=DIM, fontsize=7)
    ax_noe.tick_params(colors=DIM, labelsize=6)
    for sp in ax_noe.spines.values():
        sp.set_color(DIM)

    # Mark (I|O) firing events (transitions) as vertical lines
    J_violations = [i for i, v in enumerate(s_n_history[-200:])
                    if i > 0 and abs(v - s_n_history[max(0,
                    len(s_n_history)-200+i-1)]) > 0.5]
    for xv in J_violations[:10]:
        ax_noe.axvline(x=xs[0]+xv, color=RED, lw=0.5, alpha=0.4)


def update_label_panel(phase_idx):
    """Update the toggleable label panel with phase description."""
    if not state['labels']:
        label_txt.set_text('')
        return
    p = PHASES[phase_idx]
    io_val  = phys.io_value(max(state['r'], 0.001))
    J_val   = phys.noether_current(max(state['r'], 0.001))
    text = (
        f"{p['name']}  |  {p['subtitle']}\n"
        f"{p['body']}\n"
        f"(I|O)={io_val:.4f}  |  S_N=∮r dθ  |  J={J_val:.4f}  |  "
        f"algebra={p['algebra']}  |  gauge={p['gauge']}  |  "
        f"Hessian: {state['hess_sign']}"
    )
    label_txt.set_text(text)
    label_txt.set_color(p['color'])


def update_live_readout(phase_idx, alpha_run):
    """Top-right live readout of key quantities."""
    p    = PHASES[phase_idx]
    io_v = phys.io_value(max(state['r'], 0.001))
    live_txt.set_text(
        f"(I|O) = {io_v:.5f}\n"
        f"r_N   = {state['r']:.4f}  θ_N = {state['theta']:.4f}\n"
        f"α_NN  = {alpha_run:.6f}\n"
        f"Α_π   = {ALPHA_PI:.6f}  (fixed)\n"
        f"Ω_ζΣ  = {OMEGA_ZS:.5f}  (fixed)\n"
        f"ω_H   = {OMEGA_H:.4f}  (fixed)\n"
        f"𝒥_N depth N = {state['layer']}\n"
        f"Engine: {ENGINE_MODE}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# PHASE RENDER DISPATCH
# ══════════════════════════════════════════════════════════════════════════════

def render_phase(phase_idx, alpha_run, wh_val, dt):
    """Advance physics state and update all artists."""
    _clear_secondary()

    t  = state['phase_t']

    # Advance worm
    dr, dtheta = phys.dirac_step(
        state['r'], state['theta'], t, phase_idx, alpha_run, dt * 0.015
    )
    state['r']     = max(0.05, min(state['r'] + dr, 30.0))
    state['theta'] = (state['theta'] + dtheta) % (2.0 * math.pi)

    state['worm_r'].append(state['r'])
    state['worm_t'].append(state['theta'])

    # Compute Noether proxy S_N = r² (action integral proxy for this frame)
    S_val = state['r'] ** 2 * abs(dtheta + 1e-6)
    state['S_N'].append(S_val)
    if len(state['S_N']) > 2000:
        state['S_N'] = state['S_N'][-2000:]

    # Conjugate pair at horizon transition (phase 3)
    if phase_idx == 3:
        r_conj = 1.0 / max(state['r'], 1e-6)
        t_conj = (state['theta'] + math.pi / 2.0) % (2.0 * math.pi)
        state['conj_r'].append(r_conj)
        state['conj_t'].append(t_conj)

    # Update worm artist
    if len(state['worm_r']) > 1:
        worm_arr = np.array(list(state['worm_t']))
        worm_r_arr = np.array(list(state['worm_r']))
        worm_line.set_data(worm_arr, worm_r_arr)
        worm_line.set_color(PHASES[phase_idx]['color'])

    # Conjugate arm
    if len(state['conj_r']) > 1:
        conj_line.set_data(
            np.array(list(state['conj_t'])),
            np.array(list(state['conj_r'])),
        )

    # Phase-specific overlays
    n_primes = min(len(PRIMES), max(10, int(t * 300 + 20)))
    if phase_idx >= 2:  # prime spiral visible from ℂ onwards
        idx    = PRIME_IDX[:n_primes]
        p_t    = PRIME_THETA[:n_primes]
        p_r    = PRIME_R[:n_primes]
        p_w    = PRIME_W[:n_primes]
        sizes  = np.clip(p_w * 600 + 0.3, 0.3, 15)
        colors = p_w / (p_w.max() + 1e-12)
        prime_scat.set_offsets(np.column_stack([p_t, p_r]))
        prime_scat.set_array(colors)
        prime_scat.set_sizes(sizes)

    if phase_idx >= 6:  # Riemann zeros visible in heartbeat phase
        z_r = np.sqrt(ZETA_ZEROS)
        z_t = (ZETA_ZEROS / (1.0 / ALPHA_PI) * 2.0 * math.pi) % (2.0 * math.pi)
        zero_scat.set_offsets(np.column_stack([z_t, z_r]))

    # Horizon dot pulses at fixed point r=1
    if abs(state['r'] - 1.0) < 0.15:
        horizon_dot.set_offsets([[state['theta'], 1.0]])
        horizon_dot.set_alpha(min(1.0, (0.15 - abs(state['r']-1.0)) * 8))

    # Main polar axis range
    max_r = max(max(state['worm_r']) if state['worm_r'] else 3, 3)
    ax_main.set_ylim(0, min(max_r * 1.15, 28))

    # Hessian (updated every 30 frames — TF call is cheap but not free)
    if state['frame'] % 30 == 0:
        lambda_blend = min(1.0, t)
        state['hess_sign'] = phys.hessian_sign(state['r'], lambda_blend)

    # Running coupling update
    state['alpha_run'] = phys.alpha_nn(
        alpha_run, max(1, state['layer']),
        ['R', 'R', 'C', 'C', 'H', 'H', 'O'][min(phase_idx, 6)]
    )

    render_rg(state['alpha_run'], phase_idx)
    render_noether(state['S_N'])
    update_label_panel(phase_idx)
    update_live_readout(phase_idx, state['alpha_run'])


# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION LOOP
# ══════════════════════════════════════════════════════════════════════════════

def animate(frame_num):
    if state['paused']:
        return []

    state['frame'] += 1
    state['phase_t'] += 0.005 * state['dt']

    phase_idx = state['phase']
    alpha_run = s_alpha.val
    wh_val    = s_wh.val

    # τ snap-to-1 detent
    tau_raw = s_tau.val
    dt = 1.0 if abs(tau_raw - 1.0) < 0.05 else tau_raw
    state['dt'] = dt

    p = PHASES[phase_idx]
    is_transition = phase_idx in TRANSITION_PHASES

    title_txt.set_text(
        f"Ainulindalë Conjecture — {p['name']}: {p['subtitle']}"
    )
    title_txt.set_color(p['color'])
    btn_phase.label.set_text(
        f"{'T' if is_transition else 'P'}{phase_idx+1}"
    )

    try:
        render_phase(phase_idx, alpha_run, wh_val, dt)
    except Exception:
        pass

    return []


# ══════════════════════════════════════════════════════════════════════════════
# WIDGET CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

def on_next(event):
    state['phase'] = min(state['phase'] + 1, len(PHASES) - 1)
    state['phase_t'] = 0.0
    state['layer'] = state['phase'] + 1

def on_prev(event):
    state['phase'] = max(state['phase'] - 1, 0)
    state['phase_t'] = 0.0
    state['layer'] = state['phase'] + 1

def on_pause(event):
    state['paused'] = not state['paused']
    btn_pause.label.set_text('▶ Play' if state['paused'] else '⏸ Pause')

def on_label(event):
    state['labels'] = not state['labels']
    btn_label.label.set_text('L on' if not state['labels'] else 'L off')
    if not state['labels']:
        label_txt.set_text('')

def on_fps(val):
    """Update FuncAnimation interval live."""
    new_interval = max(16, int(1000.0 / max(val, 1)))
    ani.event_source.interval = new_interval

def on_alpha(val):
    """Snap α_NN(l) slider to Α_π if within tolerance."""
    if abs(val - ALPHA_PI) < 5e-4:
        s_alpha.set_val(ALPHA_PI)

btn_next.on_clicked(on_next)
btn_prev.on_clicked(on_prev)
btn_pause.on_clicked(on_pause)
btn_label.on_clicked(on_label)
s_fps.on_changed(on_fps)
s_alpha.on_changed(on_alpha)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM ANNOTATIONS
# ══════════════════════════════════════════════════════════════════════════════

fig.text(
    0.03, 0.080,
    '(I|O) = ⟨I|O⟩  |  Fixed: (I|O)=1 at r_N=1 (horizon)  |  (I|O)=φ at r_N=φ (Gravinon)',
    ha='left', color=GOLD, fontsize=7.5,
)
fig.text(
    0.03, 0.063,
    f'Operator domain: Α_π ≤ (I|O) ≤ Ω_ζΣ  '
    f'({ALPHA_PI:.6f} ≤ r_N ≤ {OMEGA_ZS:.5f})',
    ha='left', color=DIM, fontsize=7.5, fontfamily='monospace',
)
fig.text(
    0.03, 0.046,
    f'Near-identity (open derivation): d*·ln(10) = {D_STAR*math.log(10):.5f}  '
    f'≈  Ω_ζΣ = {OMEGA_ZS:.5f}  |  gap = {abs(D_STAR*math.log(10)-OMEGA_ZS):.5f}',
    ha='left', color=DIM, fontsize=7.5, fontfamily='monospace',
)
fig.text(
    0.55, 0.080,
    '𝒥_N fires at every layer boundary — same map, different recursion depth.',
    ha='left', color=DIM, fontsize=7.5,
)
fig.text(
    0.55, 0.063,
    'Schwarzschild horizon · Hawking pairs · Dirac sea · Ptolemy inversion',
    ha='left', color=DIM, fontsize=7.5,
)
fig.text(
    0.55, 0.046,
    '— four established phenomena, one map: (I|O)',
    ha='left', color=GOLD, fontsize=7.5,
)

# ══════════════════════════════════════════════════════════════════════════════
# LAUNCH
# ══════════════════════════════════════════════════════════════════════════════

print()
print("═" * 70)
print("  AINULINDALË — INSIDE-OUT INVERSION SIMULATOR  (TF)")
print("═" * 70)
print(f"  Engine mode  : {ENGINE_MODE}")
print(f"  TF available : {TF_AVAILABLE}")
print()
print(f"  CONSTANTS (fixed — never slide):")
print(f"    Α_π   = {ALPHA_PI:.10f}  [BK lower wall, E8/Wyler]")
print(f"    Ω_ζΣ  = {OMEGA_ZS:.10f}  [BK upper wall, Lambert W]")
print(f"    ω_H   = {OMEGA_H:.10f}  [Hagedorn ceiling, e^π]")
print(f"    φ     = {PHI:.10f}  [golden ratio, Gravinon pole]")
print(f"    d*    = {D_STAR:.10f}  [flat curvature locus]")
print(f"    gap   = {abs(D_STAR*math.log(10)-OMEGA_ZS):.10f}  [open derivation]")
print()
print(f"  (I|O) fixed points:")
print(f"    r_N = 1   →  (I|O) = 1  [flat geometry horizon]")
print(f"    r_N = φ   →  (I|O) = φ  [curved geometry, Gravinon]")
print()
print(f"  Controls:")
print(f"    Next ▶ / ◀ Back  — advance through 7 phases + transitions")
print(f"    α_NN(l) slider   — running coupling in [Α_π, Ω_ζΣ]")
print(f"    τ slider         — physics speed (detent at 1.0)")
print(f"    fps slider       — render speed")
print(f"    ω_H slider       — Hagedorn ceiling (explorable)")
print(f"    L off button     — toggle phase labels")
print(f"    Space/Pause      — pause/resume")
print()
print("  For Transition Zone Explorer: run ainulindale_explorer_tf.py")
print("═" * 70)
print()

ani = FuncAnimation(
    fig, animate,
    frames=100_000,
    interval=int(1000.0 / 30),
    blit=False,
)
plt.show()
