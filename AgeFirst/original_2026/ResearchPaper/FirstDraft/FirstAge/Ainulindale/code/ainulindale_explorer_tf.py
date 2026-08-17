#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   A I N U L I N D A L Ë   —   T R A N S I T I O N   E X P L O R E R  (TF)  ║
║   Inside-Out Inversion (I|O) — Static Fractal Explorer                       ║
║                                                                               ║
║   NO FuncAnimation. NO continuous loop.                                      ║
║   All computation is event-driven: render on demand, idle between.           ║
║   Full 4200-state resolution available without memory pressure.               ║
║                                                                               ║
║   Engineer : O Captain My Captain                                             ║
║   Code     : Claude (Anthropic) — April 2026                                 ║
║                                                                               ║
║   Run:  python3 ainulindale_explorer_tf.py                                   ║
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
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.patches import Circle

# ── TensorFlow ────────────────────────────────────────────────────────────────
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

# ── SMNNIP engines ────────────────────────────────────────────────────────────
try:
    from smnnip_inversion_engine import (
        PhysicalConstants, InversionMap, RecursionAttractor,
        GradientFlow, NoetherMonitor, get_observer,
    )
except ImportError as e:
    print(f"ERROR: Could not import smnnip_inversion_engine.py\n  {e}")
    sys.exit(1)

try:
    if TF_AVAILABLE:
        from smnnip_derivation_tf import SMNNIPDerivationEngineTF as DerivEngine
        ENGINE_MODE = 'tensorflow'
    else:
        from smnnip_derivation_pure import SMNNIPDerivationEngine as DerivEngine
        ENGINE_MODE = 'pure_python'
except ImportError:
    DerivEngine  = None
    ENGINE_MODE  = 'inversion_only'

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

C        = PhysicalConstants()
OBS      = get_observer()

ALPHA_PI = C.ALPHA
OMEGA_ZS = C.OMEGA
OMEGA_H  = math.e ** math.pi
PHI      = C.PHI
D_STAR   = C.D_STAR
HBAR_NN  = C.HBAR_NN

# ── Palette ───────────────────────────────────────────────────────────────────
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

# ══════════════════════════════════════════════════════════════════════════════
# TRANSITION DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

TRANSITIONS = [
    {
        'name'       : 'T1: ℝ→ℂ',
        'full'       : 'Transition 1 — ℝ→ℂ  |  Ordering lost  |  U(1) born',
        'description': '𝒥_N: (r,θ) ⟼ (1/r, θ+π/2)  |  Phase is not added — it is forced.\n'
                       'The line cannot stay straight. (I|O) fires. The worm bends 90°.\n'
                       'U(1) symmetry emerges because the π/2 rotation IS the U(1) generator.',
        'lower_alg'  : 'R',
        'upper_alg'  : 'C',
        'symmetry'   : 1,     # angular fold count
        'color'      : CYAN,
        'gauge_born' : 'U(1)',
    },
    {
        'name'       : 'T2: ℂ→ℍ',
        'full'       : 'Transition 2 — ℂ→ℍ  |  Commutativity lost  |  SU(2) born  ← EVENT HORIZON',
        'description': '𝒥_N fires inside a space that already has phase.\n'
                       'AB ≠ BA. The spiral bifurcates. Conjugate pair born at r_N=1.\n'
                       'One arm r>1 (escapes). One arm r<1 (crosses). Both are (I|O) partners.',
        'lower_alg'  : 'C',
        'upper_alg'  : 'H',
        'symmetry'   : 2,     # SU(2) — 2-fold spinor
        'color'      : GOLD,
        'gauge_born' : 'SU(2)',
    },
    {
        'name'       : 'T3: ℍ→𝕆',
        'full'       : 'Transition 3 — ℍ→𝕆  |  Associativity lost  |  G₂/SU(3) born  ← FANO SHATTERING',
        'description': '𝒥_N fires in non-commutative space. 7 Fano imaginary units activated.\n'
                       '(AB)C ≠ A(BC). Context changes path. Seven-fold resonance ignites.\n'
                       'Gravinon pole at r_N=φ — zero-mass fixed point of (I|O).',
        'lower_alg'  : 'H',
        'upper_alg'  : 'O',
        'symmetry'   : 7,     # Fano plane — 7-fold
        'color'      : ORANGE,
        'gauge_born' : 'G₂/SU(3)',
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PHYSICS ENGINE FOR EXPLORER
# ══════════════════════════════════════════════════════════════════════════════

class ExplorerPhysics:
    """
    All computations for the static explorer.
    No animation loop — compute on demand.
    TF used for batch Hessian computation when available.
    """

    def __init__(self):
        self.inv   = InversionMap()
        self.rec   = RecursionAttractor()
        self.noeth = NoetherMonitor()
        self.flow  = GradientFlow()

    # ── Blended (I|O) map at blend depth λ ───────────────────────────────────
    def blended_jn(self, r, theta, lam):
        """
        At λ=0: lower algebra multiplication rules (straight path)
        At λ=1: upper algebra multiplication rules (post-inversion)
        At λ=0.5: HORIZON — both rules equally active — maximum complexity
        Returns (r_new, theta_new) under the blended map.
        """
        # Lower algebra: identity map (no inversion)
        r_lower     = r
        theta_lower = theta
        # Upper algebra: full (I|O) inversion
        r_upper     = 1.0 / max(r, 1e-9)
        theta_upper = (theta + math.pi / 2.0) % (2.0 * math.pi)
        # Blend
        r_new     = (1.0 - lam) * r_lower + lam * r_upper
        theta_new = (1.0 - lam) * theta_lower + lam * theta_upper
        # Normalize theta
        theta_new = theta_new % (2.0 * math.pi)
        return r_new, theta_new

    # ── Iterated orbit under blended map ─────────────────────────────────────
    def orbit(self, r0, theta0, lam, n_iter=80):
        """
        Iterate the blended J_N map n_iter times from (r0, theta0).
        Returns arrays of r and theta — the orbit.
        """
        rs     = [r0]
        thetas = [theta0]
        r, theta = r0, theta0
        for _ in range(n_iter):
            r, theta = self.blended_jn(r, theta, lam)
            rs.append(r)
            thetas.append(theta)
            if r > 50 or r < 1e-6:   # escaped or collapsed
                break
        return np.array(rs), np.array(thetas)

    # ── Orbit diagram: r_∞ as function of λ ──────────────────────────────────
    def orbit_diagram(self, r0, theta0, n_lambda=200, n_iter=120,
                      n_discard=60):
        """
        For each λ in [0,1]: iterate blended J_N, discard transient,
        record the final r values. This is the bifurcation diagram.

        Returns: (lambdas, r_finals) as 1D arrays.
        n_lambda=200 gives smooth diagram; 1000 gives publication quality.
        """
        lambdas  = np.linspace(0.0, 1.0, n_lambda)
        r_finals = []
        for lam in lambdas:
            r, theta = r0, theta0
            # Burn-in
            for _ in range(n_discard):
                r, theta = self.blended_jn(r, theta, lam)
                if r > 50 or r < 1e-6:
                    break
            # Collect
            collected = []
            for _ in range(n_iter - n_discard):
                r, theta = self.blended_jn(r, theta, lam)
                if r > 50 or r < 1e-6:
                    break
                collected.append(r)
            r_finals.append(collected)
        return lambdas, r_finals

    # ── Hessian sign at (r, λ) using TF if available ─────────────────────────
    def hessian_grid(self, r_vals, lambda_vals):
        """
        Compute sign of d²V/d|β|² at each (r, λ) point.
        Negative = symmetry breaking active (Mexican hat).
        Returns 2D array of signs: -1 (SSB) or +1 (symmetric).

        When TF available: batched autodiff over the full grid.
        When pure Python: analytic formula.
        """
        R, L = np.meshgrid(r_vals, lambda_vals)
        mu_sq = 0.5
        if TF_AVAILABLE:
            r_tf = tf.constant(R.flatten(), dtype=tf.float64)
            lam_tf = tf.constant(L.flatten(), dtype=tf.float64)
            with tf.GradientTape(persistent=True) as t2:
                with tf.GradientTape() as t1:
                    lam_eff = 0.1 * (1.0 + lam_tf)
                    V = -mu_sq * r_tf**2 + lam_eff * r_tf**4
                g = t1.gradient(V, r_tf)
            h = t2.gradient(g, r_tf)
            signs = np.sign(h.numpy()).reshape(R.shape)
        else:
            lam_eff = 0.1 * (1.0 + L)
            d2V = -2.0 * mu_sq + 12.0 * lam_eff * R**2
            signs = np.sign(d2V)
        return signs

    # ── Noether current along orbit ───────────────────────────────────────────
    def noether_along_orbit(self, rs):
        """J(r) = 8/(π²r²) along an orbit. Should stay constant."""
        return np.array([self.noeth.current(max(float(r), 1e-6)) for r in rs])

    # ── Angular symmetry sectors ──────────────────────────────────────────────
    def symmetry_sectors(self, n_fold, r_range=(0.5, 4.0)):
        """
        Generate the n_fold symmetry sector lines for the given transition.
        Returns list of (theta, r_array) pairs — radial spokes.
        """
        thetas = [k * 2.0 * math.pi / n_fold for k in range(n_fold)]
        rs     = np.linspace(r_range[0], r_range[1], 50)
        return [(th, rs) for th in thetas]


# ══════════════════════════════════════════════════════════════════════════════
# EXPLORER STATE
# ══════════════════════════════════════════════════════════════════════════════

phys = ExplorerPhysics()

xstate = {
    'transition'  : 0,       # index into TRANSITIONS
    'lam'         : 0.0,     # blend depth λ ∈ [0,1]
    'r_zoom'      : 5.0,     # polar r axis limit
    'r0'          : 2.0,     # orbit seed r
    'theta0'      : 0.0,     # orbit seed θ
    'step_count'  : 200,     # λ resolution for orbit diagram
    'n_iter'      : 120,     # iterations per λ step
    'zoom_center' : 'r=1',   # 'r=1' or 'r=φ'
    'show_sectors': True,
    'show_orbit'  : True,
    'show_hessian': True,
    'auto_step'   : False,
    'labels'      : True,
    # Cached orbit diagram (recomputed on transition or step_count change)
    '_orb_lambdas': None,
    '_orb_rfinals': None,
    '_hess_grid'  : None,
}

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(16, 10), facecolor=BG)
fig.canvas.manager.set_window_title(
    "Ainulindalë — Transition Explorer  |  (I|O) Static Fractal Mode"
)

gs = gridspec.GridSpec(
    2, 3, figure=fig,
    left=0.04, right=0.97,
    top=0.88, bottom=0.30,
    hspace=0.38, wspace=0.30,
)

ax_polar  = fig.add_subplot(gs[0, 0], projection='polar')  # main orbit view
ax_bifurc = fig.add_subplot(gs[0, 1])                       # bifurcation diagram
ax_hess   = fig.add_subplot(gs[0, 2])                       # Hessian grid
ax_noeth  = fig.add_subplot(gs[1, 0])                       # Noether along orbit
ax_flow   = fig.add_subplot(gs[1, 1])                       # gradient flow r→φ
ax_info   = fig.add_subplot(gs[1, 2])                       # text info panel

for ax in (ax_polar, ax_bifurc, ax_hess, ax_noeth, ax_flow):
    ax.set_facecolor(BG)
    ax.tick_params(colors=DIM, labelsize=7)
    for sp in ax.spines.values():
        sp.set_color(DIM)
ax_polar.set_facecolor(BG)
ax_polar.set_yticklabels([])
ax_polar.set_xticklabels([])
ax_info.set_facecolor('#050510')
ax_info.set_xticks([])
ax_info.set_yticks([])

# ── Titles ────────────────────────────────────────────────────────────────────
title_txt = fig.text(
    0.5, 0.935,
    'Ainulindalë — Transition Explorer  |  (I|O) Static Mode',
    ha='center', va='top', color=GOLD,
    fontsize=12, fontweight='bold', fontfamily='serif',
)
sub_txt = fig.text(
    0.5, 0.907,
    'Event-driven. No animation loop. Full resolution. CPU idle between steps.',
    ha='center', va='top', color='#8090a0', fontsize=8.5,
)
const_txt = fig.text(
    0.03, 0.932,
    f'Α_π={ALPHA_PI:.6f}  Ω_ζΣ={OMEGA_ZS:.5f}  φ={PHI:.5f}  d*={D_STAR:.5f}  '
    f'Engine:{ENGINE_MODE}',
    ha='left', va='top', color=DIM, fontsize=7, fontfamily='monospace',
)

# ── info panel text ───────────────────────────────────────────────────────────
info_txt = fig.text(
    0.685, 0.82,
    '', ha='left', va='top',
    color=WHITE, fontsize=7.5, fontfamily='monospace',
)

# ══════════════════════════════════════════════════════════════════════════════
# WIDGETS
# ══════════════════════════════════════════════════════════════════════════════

# λ blend slider — the primary axis
ax_lam = plt.axes([0.07, 0.225, 0.45, 0.022], facecolor='#111')
s_lam  = Slider(ax_lam, 'λ  blend depth  [0 = lower alg ... 0.5 = HORIZON ... 1 = upper alg]',
                0.0, 1.0, valinit=0.0, color=GOLD)
s_lam.label.set_color(WHITE)
s_lam.valtext.set_color(GOLD)

# r zoom slider
ax_rzoom = plt.axes([0.07, 0.196, 0.22, 0.022], facecolor='#111')
s_rzoom  = Slider(ax_rzoom, 'r zoom', 1.0, 12.0, valinit=5.0, color=CYAN)
s_rzoom.label.set_color(WHITE)
s_rzoom.valtext.set_color(CYAN)

# step count slider (λ resolution)
ax_step = plt.axes([0.34, 0.196, 0.18, 0.022], facecolor='#111')
s_step  = Slider(ax_step, 'λ steps', 20, 1000, valinit=200,
                 valstep=10, color=VIOLET)
s_step.label.set_color(WHITE)
s_step.valtext.set_color(VIOLET)

# Transition selector buttons
ax_t1 = plt.axes([0.57, 0.230, 0.09, 0.042])
ax_t2 = plt.axes([0.67, 0.230, 0.09, 0.042])
ax_t3 = plt.axes([0.77, 0.230, 0.09, 0.042])
btn_t1 = Button(ax_t1, 'T1: ℝ→ℂ',  color='#1a2a2e', hovercolor='#2a3a4e')
btn_t2 = Button(ax_t2, 'T2: ℂ→ℍ',  color='#1a1a0e', hovercolor='#2a2a1e')
btn_t3 = Button(ax_t3, 'T3: ℍ→𝕆',  color='#1a0a1e', hovercolor='#2a1a2e')
for b, c in [(btn_t1, CYAN), (btn_t2, GOLD), (btn_t3, ORANGE)]:
    b.label.set_color(c)
    b.label.set_fontsize(8)

# Navigation
ax_step_fwd  = plt.axes([0.57, 0.185, 0.07, 0.038])
ax_step_back = plt.axes([0.50, 0.185, 0.07, 0.038])
ax_snap_h    = plt.axes([0.65, 0.185, 0.10, 0.038])
ax_snap_phi  = plt.axes([0.76, 0.185, 0.10, 0.038])
ax_auto      = plt.axes([0.87, 0.185, 0.09, 0.038])

btn_sfwd   = Button(ax_step_fwd,  'λ ▶',     color='#1a1a2e', hovercolor='#2a2a4e')
btn_sback  = Button(ax_step_back, '◀ λ',     color='#1a1a2e', hovercolor='#2a2a4e')
btn_snap_h = Button(ax_snap_h,    'Snap r=1', color='#1a1a2e', hovercolor='#2a2a4e')
btn_snphi  = Button(ax_snap_phi,  'Snap r=φ', color='#1a1a2e', hovercolor='#2a2a4e')
btn_auto   = Button(ax_auto,      'Auto ▶',   color='#1a1a2e', hovercolor='#2a2a4e')

for b in (btn_sfwd, btn_sback, btn_snap_h, btn_snphi, btn_auto):
    b.label.set_color(WHITE)
    b.label.set_fontsize(8.5)

# ══════════════════════════════════════════════════════════════════════════════
# RENDER — all panels, called once per user interaction
# ══════════════════════════════════════════════════════════════════════════════

def recompute_orbit_diagram():
    """Recompute and cache the orbit diagram (slow — only on demand)."""
    t   = TRANSITIONS[xstate['transition']]
    lam_arr, r_finals = phys.orbit_diagram(
        xstate['r0'], xstate['theta0'],
        n_lambda=xstate['step_count'],
        n_iter=xstate['n_iter'],
    )
    xstate['_orb_lambdas'] = lam_arr
    xstate['_orb_rfinals'] = r_finals

    # Also recompute Hessian grid
    r_vals   = np.linspace(0.1, xstate['r_zoom'], 40)
    lam_vals = np.linspace(0.0, 1.0, 40)
    xstate['_hess_grid'] = (r_vals, lam_vals,
                             phys.hessian_grid(r_vals, lam_vals))


def render_all():
    """Full redraw of all six panels. Called after any state change."""
    t   = TRANSITIONS[xstate['transition']]
    lam = xstate['lam']

    # ── Panel 1: Polar orbit ─────────────────────────────────────────────────
    ax_polar.cla()
    ax_polar.set_facecolor(BG)
    ax_polar.grid(color=DIM, linestyle='--', linewidth=0.3, alpha=0.35)
    ax_polar.set_yticklabels([])
    ax_polar.set_xticklabels([])

    rs, thetas = phys.orbit(
        xstate['r0'], xstate['theta0'], lam, n_iter=200
    )

    if len(rs) > 1:
        # Color gradient along orbit — early=bright, late=dim
        n = len(rs)
        for i in range(n - 1):
            alpha_val = 0.3 + 0.7 * (i / n)
            ax_polar.plot(thetas[i:i+2], rs[i:i+2],
                          color=t['color'], lw=1.5, alpha=alpha_val)

    # Symmetry sectors
    if xstate['show_sectors']:
        sectors = phys.symmetry_sectors(t['symmetry'])
        for th, r_arr in sectors:
            ax_polar.plot([th]*len(r_arr), r_arr,
                          color=DIM, lw=0.5, ls=':', alpha=0.6)

    # Fixed point markers
    ax_polar.scatter([0], [1.0], s=60, c=GOLD, zorder=8, marker='o',
                     label='r=1 (I|O)=1')
    ax_polar.scatter([0], [PHI], s=60, c=ORANGE, zorder=8, marker='*',
                     label=f'r=φ={PHI:.3f}')

    ax_polar.set_ylim(0, xstate['r_zoom'])
    ax_polar.set_title(
        f'(I|O) Orbit at λ={lam:.3f}',
        color=t['color'], fontsize=8, pad=4,
    )
    ax_polar.legend(fontsize=6, loc='upper right',
                    facecolor='#0a0a18', labelcolor=WHITE, framealpha=0.5)

    # ── Panel 2: Bifurcation diagram ─────────────────────────────────────────
    ax_bifurc.cla()
    ax_bifurc.set_facecolor(BG)

    if xstate['_orb_lambdas'] is not None:
        lams = xstate['_orb_lambdas']
        rfin = xstate['_orb_rfinals']
        for i, (lam_i, r_list) in enumerate(zip(lams, rfin)):
            if r_list:
                ax_bifurc.scatter(
                    [lam_i] * len(r_list), r_list,
                    s=0.3, c=t['color'], alpha=0.4,
                )

        # Vertical line at current λ
        ax_bifurc.axvline(x=lam, color=WHITE, lw=0.8, ls='-', alpha=0.7)
        # Mark λ=0.5 horizon
        ax_bifurc.axvline(x=0.5, color=GOLD, lw=0.6, ls='--', alpha=0.6)
        ax_bifurc.text(0.51, ax_bifurc.get_ylim()[1] * 0.9 if ax_bifurc.get_ylim()[1] > 0 else 3,
                       '(I|O)=1\nhorizon', color=GOLD, fontsize=6)

        # Mark fixed points as horizontals
        ax_bifurc.axhline(y=1.0, color=GOLD,   lw=0.5, ls=':', alpha=0.5)
        ax_bifurc.axhline(y=PHI, color=ORANGE, lw=0.5, ls=':', alpha=0.5)

    ax_bifurc.set_xlabel('λ (blend depth)', color=DIM, fontsize=7)
    ax_bifurc.set_ylabel('r_∞ (final orbit r)', color=DIM, fontsize=7)
    ax_bifurc.set_title('Orbit Diagram — λ bifurcation', color=t['color'],
                        fontsize=8, pad=3)
    ax_bifurc.tick_params(colors=DIM, labelsize=6)
    for sp in ax_bifurc.spines.values():
        sp.set_color(DIM)

    ax_bifurc.text(0.02, 0.95,
                   f'λ steps={xstate["step_count"]}',
                   transform=ax_bifurc.transAxes,
                   color=DIM, fontsize=6, va='top')

    # ── Panel 3: Hessian grid (SSB map) ──────────────────────────────────────
    ax_hess.cla()
    ax_hess.set_facecolor(BG)

    if xstate['_hess_grid'] is not None and xstate['show_hessian']:
        r_vals, lam_vals, hess = xstate['_hess_grid']
        im = ax_hess.pcolormesh(
            lam_vals, r_vals, hess.T,
            cmap='RdBu_r', vmin=-1, vmax=1, alpha=0.85,
        )
        ax_hess.axvline(x=0.5, color=GOLD, lw=0.8, ls='--', alpha=0.7)
        ax_hess.axvline(x=lam, color=WHITE, lw=0.8, ls='-', alpha=0.7)
        ax_hess.axhline(y=1.0, color=GOLD,   lw=0.5, ls=':', alpha=0.6)
        ax_hess.axhline(y=PHI, color=ORANGE, lw=0.5, ls=':', alpha=0.6)
        ax_hess.set_xlabel('λ', color=DIM, fontsize=7)
        ax_hess.set_ylabel('r', color=DIM, fontsize=7)
        ax_hess.set_title('Hessian sign  (blue=SSB, red=sym)', color=VIOLET,
                          fontsize=8, pad=3)
        ax_hess.text(0.02, 0.96, 'Blue: ∂²V<0 (Mexican hat active)',
                     transform=ax_hess.transAxes, color=CYAN, fontsize=6, va='top')
        ax_hess.text(0.02, 0.88, 'Red:  ∂²V>0 (symmetric phase)',
                     transform=ax_hess.transAxes, color=RED, fontsize=6, va='top')
    else:
        ax_hess.text(0.5, 0.5, 'Hessian grid\n(click Recompute)',
                     ha='center', va='center', color=DIM, fontsize=9,
                     transform=ax_hess.transAxes)
        ax_hess.set_title('Hessian — SSB landscape', color=VIOLET,
                          fontsize=8, pad=3)
    ax_hess.tick_params(colors=DIM, labelsize=6)
    for sp in ax_hess.spines.values():
        sp.set_color(DIM)

    # ── Panel 4: Noether current along current orbit ──────────────────────────
    ax_noeth.cla()
    ax_noeth.set_facecolor(BG)

    rs_orb, _ = phys.orbit(xstate['r0'], xstate['theta0'], lam, n_iter=200)
    J_vals    = phys.noether_along_orbit(rs_orb)
    ax_noeth.plot(J_vals, color=GREEN, lw=1.2, alpha=0.85)
    ax_noeth.axhline(y=J_vals[0], color=GOLD, lw=0.6, ls='--', alpha=0.6,
                     label='J₀ (initial)')
    violation = (np.max(np.abs(J_vals - J_vals[0])) /
                 (abs(J_vals[0]) + 1e-30))
    ax_noeth.set_title(
        f'Noether current J(r)  |  violation={violation:.3e}',
        color=GREEN, fontsize=8, pad=3,
    )
    ax_noeth.set_xlabel('Orbit step', color=DIM, fontsize=7)
    ax_noeth.set_ylabel('J = 8/(π²r²)', color=DIM, fontsize=7)
    conservation = 'CONSERVED' if violation < 0.01 else 'VIOLATED'
    ax_noeth.text(0.7, 0.9, conservation,
                  transform=ax_noeth.transAxes,
                  color=GREEN if violation < 0.01 else RED,
                  fontsize=8, fontweight='bold')
    ax_noeth.tick_params(colors=DIM, labelsize=6)
    for sp in ax_noeth.spines.values():
        sp.set_color(DIM)

    # ── Panel 5: Gradient flow r=1 → φ ───────────────────────────────────────
    ax_flow.cla()
    ax_flow.set_facecolor(BG)

    flow_res = phys.flow.compute(verbose=False)
    traj     = flow_res.trajectory
    if traj:
        zs    = [p['z'] for p in traj]
        dists = [p['distance'] for p in traj]
        ax_flow.plot(zs, color=CYAN, lw=1.2, alpha=0.85,
                     label='z (converging to φ)')
        ax_flow.axhline(y=PHI, color=GOLD, lw=0.8, ls='--', alpha=0.8,
                        label=f'φ={PHI:.5f}')
        ax_flow.axhline(y=1.0, color=RED, lw=0.6, ls=':', alpha=0.6,
                        label='r=1 (horizon)')
        ax_flow.set_title(
            f'Gradient flow: r=1 → φ  |  pathway: π→ħ_NN→φ',
            color=CYAN, fontsize=8, pad=3,
        )
        ax_flow.legend(fontsize=6, facecolor='#0a0a18',
                       labelcolor=WHITE, framealpha=0.5)
        confirmed = flow_res.full_pathway_confirmed
        ax_flow.text(0.6, 0.15,
                     f'π→ħ→φ: {"✓ CONFIRMED" if confirmed else "partial"}',
                     transform=ax_flow.transAxes,
                     color=GREEN if confirmed else ORANGE, fontsize=7.5)
    ax_flow.set_xlabel('Iteration step', color=DIM, fontsize=7)
    ax_flow.tick_params(colors=DIM, labelsize=6)
    for sp in ax_flow.spines.values():
        sp.set_color(DIM)

    # ── Panel 6: Info text ────────────────────────────────────────────────────
    info_txt.set_text(
        f"{t['full']}\n\n"
        f"{t['description']}\n\n"
        f"λ = {lam:.4f}  {'← HORIZON' if abs(lam-0.5)<0.03 else ''}\n"
        f"(I|O) at r_N=1: unity (horizon)\n"
        f"(I|O) at r_N=φ: Gravinon pole\n\n"
        f"Gauge born:   {t['gauge_born']}\n"
        f"Symmetry:     {t['symmetry']}-fold\n"
        f"λ steps:      {xstate['step_count']}\n\n"
        f"Fixed points:\n"
        f"  r=1  →  (I|O)=1  (flat geom.)\n"
        f"  r=φ  →  (I|O)=φ  (curved geom.)\n\n"
        f"Open derivation:\n"
        f"  d*·ln10={D_STAR*math.log(10):.5f} ≈ Ω_ζΣ={OMEGA_ZS:.5f}\n"
        f"  gap = {abs(D_STAR*math.log(10)-OMEGA_ZS):.5f}\n\n"
        f"Engine: {ENGINE_MODE}\n"
        f"TF available: {TF_AVAILABLE}"
    )
    info_txt.set_color(t['color'])

    title_txt.set_text(
        f"Ainulindalë — Transition Explorer  |  {t['name']}  |  λ={lam:.3f}"
    )
    title_txt.set_color(t['color'])

    fig.canvas.draw_idle()


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

def on_lam(val):
    xstate['lam'] = val
    render_all()

def on_rzoom(val):
    xstate['r_zoom'] = val
    render_all()

def on_step_count(val):
    xstate['step_count'] = int(val)
    xstate['_orb_lambdas'] = None   # invalidate cache
    render_all()

def select_transition(idx):
    xstate['transition'] = idx
    xstate['_orb_lambdas'] = None   # invalidate cache
    xstate['_hess_grid']  = None
    recompute_orbit_diagram()
    render_all()

def on_t1(event): select_transition(0)
def on_t2(event): select_transition(1)
def on_t3(event): select_transition(2)

def on_step_fwd(event):
    step = 1.0 / max(xstate['step_count'], 1)
    xstate['lam'] = min(1.0, xstate['lam'] + step)
    s_lam.set_val(xstate['lam'])

def on_step_back(event):
    step = 1.0 / max(xstate['step_count'], 1)
    xstate['lam'] = max(0.0, xstate['lam'] - step)
    s_lam.set_val(xstate['lam'])

def on_snap_horizon(event):
    """Snap λ to 0.5 (the horizon) and zoom r around r=1."""
    s_lam.set_val(0.5)
    s_rzoom.set_val(3.0)
    xstate['r0'] = 1.5
    xstate['lam'] = 0.5
    xstate['r_zoom'] = 3.0
    render_all()

def on_snap_phi(event):
    """Snap λ to region and zoom r around r=φ (Gravinon)."""
    s_lam.set_val(0.618)   # near φ-crossing
    s_rzoom.set_val(4.0)
    xstate['r0'] = PHI * 1.1
    xstate['lam'] = 0.618
    xstate['r_zoom'] = 4.0
    render_all()

_auto_running = [False]

def on_auto(event):
    """Auto-step through λ — manual loop, interruptible."""
    if _auto_running[0]:
        _auto_running[0] = False
        btn_auto.label.set_text('Auto ▶')
        return
    _auto_running[0] = True
    btn_auto.label.set_text('■ Stop')
    step = 1.0 / max(xstate['step_count'], 1)
    import time
    while _auto_running[0] and xstate['lam'] < 1.0:
        xstate['lam'] = min(1.0, xstate['lam'] + step)
        s_lam.set_val(xstate['lam'])
        fig.canvas.flush_events()
        time.sleep(0.05)
    _auto_running[0] = False
    btn_auto.label.set_text('Auto ▶')

s_lam.on_changed(on_lam)
s_rzoom.on_changed(on_rzoom)
s_step.on_changed(on_step_count)
btn_t1.on_clicked(on_t1)
btn_t2.on_clicked(on_t2)
btn_t3.on_clicked(on_t3)
btn_sfwd.on_clicked(on_step_fwd)
btn_sback.on_clicked(on_step_back)
btn_snap_h.on_clicked(on_snap_horizon)
btn_snphi.on_clicked(on_snap_phi)
btn_auto.on_clicked(on_auto)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM ANNOTATIONS
# ══════════════════════════════════════════════════════════════════════════════

fig.text(0.03, 0.080,
    'Operator domain: Α_π ≤ (I|O) ≤ Ω_ζΣ  |  (I|O)=1 at r=1 (horizon)  |  (I|O)=φ at r=φ (Gravinon)',
    ha='left', color=GOLD, fontsize=7.5)
fig.text(0.03, 0.063,
    'λ=0: lower algebra  |  λ=0.5: HORIZON — both rules equally active  |  λ=1: upper algebra',
    ha='left', color=DIM, fontsize=7.5)
fig.text(0.03, 0.046,
    'Blue Hessian = symmetry breaking active (Mexican hat). Red = symmetric phase. Transition at sign change.',
    ha='left', color=DIM, fontsize=7.5)

# ══════════════════════════════════════════════════════════════════════════════
# LAUNCH
# ══════════════════════════════════════════════════════════════════════════════

print()
print("═" * 70)
print("  AINULINDALË — TRANSITION EXPLORER  (I|O)  Static Mode")
print("═" * 70)
print(f"  Engine mode  : {ENGINE_MODE}")
print(f"  TF available : {TF_AVAILABLE}")
print()
print(f"  Three transitions available:")
for i, t in enumerate(TRANSITIONS):
    print(f"    [{i+1}] {t['full']}")
print()
print(f"  Controls:")
print(f"    λ slider     — blend depth (0=lower, 0.5=horizon, 1=upper alg)")
print(f"    λ ▶ / ◀ λ    — single-step forward/backward")
print(f"    Auto ▶       — auto-step (interruptible)")
print(f"    Snap r=1     — zoom to (I|O)=1 horizon")
print(f"    Snap r=φ     — zoom to Gravinon pole")
print(f"    T1/T2/T3     — select transition")
print(f"    λ steps      — resolution (200=default, 1000=publication)")
print()
print(f"  No FuncAnimation — CPU idle between interactions.")
print(f"  Hessian grid uses TF batch autodiff when available.")
print("═" * 70)
print()

# Initial compute and render
print("  Computing initial orbit diagram... ", end='', flush=True)
recompute_orbit_diagram()
print("done.")
render_all()

plt.show()
