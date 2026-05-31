#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   C Y M A T I C   R E S O N A N C E   O F   C R E A T I O N                ║
║   Universe = Chladni plate / Fibonacci sphere driven by spacetime expansion. ║
║   Matter = sand accumulating at nodes.                                      ║
║                                                                             ║
║   Engineer : Cody Michael Allison                                           ║
║   Code     : Claude Sonnet (Anthropic) — May 2026                          ║
║   Sources  : All EHS variants unified (see TODO.md CRC section)             ║
║                                                                             ║
║   PANEL LAYOUT (2D mode):                                                   ║
║   ┌────────────┬────────────┐                                               ║
║   │ 1. SPIRAL  │ 2. CHLADNI │  ← prime walk | sand at nodes                ║
║   ├────────────┼────────────┤                                               ║
║   │ 3. NOETHER │ 4. MORPH   │  ← J_cross | morphology snapshot             ║
║   ├────────────┴────────────┤                                               ║
║   │ 5. RIEMANN | 6. FERMAT  │  ← horizon invariance (the money shot)       ║
║   └─────────────────────────┘                                               ║
║                                                                             ║
║   [UNS] checkbox replaces Panel 1 with 3D Fibonacci sphere.                ║
║   Universal Native Space: longitude=golden_angle, latitude=equal_area,     ║
║   radius=φ^-n (Fermat), sphere breathes with Heartbeat.                    ║
║   Riemann zeros → latitudinal node rings on the sphere.                    ║
║                                                                             ║
║   UNIVERSAL RESONANT CAVITY EQUATION:                                      ║
║   □Ψ = Σ_n  [φ^{-n} · ζ(½+iγ_n) · ∂_μJ^μ]                               ║
║   Eigenspectrum: λ_n = γ_n² · φ^{-n}                                      ║
║   Ground state:  λ_0 → OMEGA_ZS = 0.56714  (Lambert W fixed point)        ║
║   Boundary:      Ψ|_{∂M} = 0  at sedenion zero-divisor surface (S⁷)        ║
║   Driving:       J^0 ≈ H(t)  (Hubble parameter IS the plate driver)        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Install:  pip install numpy matplotlib scipy
Run:      python3 CRC_engine.py

Controls:
  [UNS] checkbox         — toggle Universal Native Space 3D Fibonacci sphere
  Phase buttons          — cycle phases (TransitionManager LERP between all)
  φ slider               — attractor depth (correct: n×2π/φ² golden angle)
  Ω slider               — thermal ceiling
  ℏ_NN slider            — node spacing → controls BAO scale
  Bias slider            — 0 → 1/φ  (NOT 2/e; corrected per conjecture_proof.py)
  Drive slider           — Chladni plate amplitude
  Space / Pause          — pause/resume animation

UNS mode — Fibonacci sphere:
  longitude ψ_n = n × GOLDEN_ANG   (same golden angle as 2D, unchanged)
  latitude  θ_n = arccos(1 - 2n/N) (equal-area: equal sphere fraction per prime)
  radius    ρ_n = φ^{-n} × R(t)    (Fermat weight, breathes with Heartbeat)
  node rings at each Riemann zero latitude (γ_n maps to arccos band)

Galaxy morphology from node geometry when BAO → OMEGA_ZS:
  spiral    = active node boundary trace   (J_cross flowing along nodal line)
  elliptical= closed circular nodes        (3D sphere on node line = corn starch)
  cluster   = overlapping node circles
  filament  = single extended node line
  void      = antinode (particles repelled)
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D          # noqa: F401 — registers 3d projection
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, CheckButtons
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS — authoritative from conjecture_proof.py
# Bias coupling = 1/φ (NOT 2/e; proven §VIII conjecture_proof.py)
# ══════════════════════════════════════════════════════════════════════════════

PHI         = (1 + np.sqrt(5)) / 2          # φ ≈ 1.618
INV_PHI     = PHI - 1                       # 1/φ ≈ 0.618 — bias coupling
GOLDEN_ANG  = 2 * np.pi / PHI**2            # 2π/φ² ≈ 137.508° — correct prime spiral
GAP         = 0.000707                      # Noether ground state
OMEGA_ZS    = 0.56714                       # Lambert W fixed point = BAO eigenvalue
ALPHA_INV   = 137.035999
TWO_OVER_PI = 2 / np.pi

# Beat frequencies — ω_i ≠ ω_e (§VI conjecture_proof: the hum, not silence)
OMEGA_I = 1.0       # internal sedenion clock
OMEGA_E = 0.95      # external clock — mismatch = Lissajous complexity

# First 20 Riemann zeta zeros (imaginary parts, Re(s)=½)
ZETA_ZEROS = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
])

def _sieve(limit):
    s = [True] * (limit + 1)
    s[0] = s[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if s[i]:
            for j in range(i*i, limit+1, i):
                s[j] = False
    return np.array([i for i in range(2, limit+1) if s[i]])

PRIMES        = _sieve(8000)
N_PRIMES      = len(PRIMES)
PRIME_INDICES = np.arange(1, N_PRIMES + 1)
PRIME_THETA   = PRIME_INDICES * GOLDEN_ANG    # correct: index × GOLDEN_ANG
PRIME_R       = np.sqrt(PRIMES)
PRIME_W       = PHI ** (-PRIME_INDICES.astype(float))  # Fermat weight φ^-n

# Chladni grid
GRID_N = 128
_cx = np.linspace(-1, 1, GRID_N)
_cy = np.linspace(-1, 1, GRID_N)
CX, CY = np.meshgrid(_cx, _cy)

# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════════════════════════════════

BG      = '#07070f'
GOLD    = '#c9a84c'
CYAN    = '#00e5ff'
MAGENTA = '#ff00ff'
VIOLET  = '#9c27b0'
YELLOW  = '#fffc00'
GREEN   = '#00e676'
RED     = '#ff1744'
WHITE   = '#ffffff'
DIM     = '#404060'

MORPH_COLORS = {
    'spiral': CYAN, 'elliptical': GOLD, 'cluster': VIOLET,
    'filament': GREEN, 'void': DIM
}

# ══════════════════════════════════════════════════════════════════════════════
# TRANSITION MANAGER — from Gemini_Revised_2_EHS.py
# LERP between phases with cyan→magenta entropy spike during transition
# ══════════════════════════════════════════════════════════════════════════════

PHASE_NAMES = ["Inertial", "Metric Swap", "Heartbeat", "Prime Spiral", "Horizon"]

class TransitionManager:
    """LERP interpolator between named phases. Cyan→magenta during transition."""

    def __init__(self):
        self.source = "Inertial"
        self.target = "Inertial"
        self.alpha  = 1.0
        self.step   = 0.03

    def trigger(self, new_phase):
        if new_phase != self.target:
            self.source = self.target
            self.target = new_phase
            self.alpha  = 0.0

    def advance(self):
        if self.alpha < 1.0:
            self.alpha = min(1.0, self.alpha + self.step)

    @property
    def in_transition(self):
        return self.alpha < 1.0

    @property
    def point_color(self):
        return MAGENTA if self.in_transition else CYAN


tm = TransitionManager()

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE — 3×2 GridSpec + 3D UNS overlay on Panel 1 position
# ══════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(16, 14), facecolor=BG)
try:
    fig.canvas.manager.set_window_title("Cymatic Resonance of Creation")
except Exception:
    pass

gs = gridspec.GridSpec(3, 2, figure=fig,
                       left=0.06, right=0.96,
                       top=0.93, bottom=0.23,
                       hspace=0.42, wspace=0.30)

ax_spiral  = fig.add_subplot(gs[0, 0], projection='polar')
ax_chlad   = fig.add_subplot(gs[0, 1])
ax_noether = fig.add_subplot(gs[1, 0])
ax_morph   = fig.add_subplot(gs[1, 1])
ax_riem    = fig.add_subplot(gs[2, 0])
ax_ferm    = fig.add_subplot(gs[2, 1])

ax_spiral.set_facecolor(BG)
ax_spiral.grid(color=DIM, linestyle='--', linewidth=0.4, alpha=0.5)
ax_spiral.set_yticklabels([])
ax_spiral.set_xticklabels([])

ax_chlad.set_facecolor(BG)
ax_chlad.set_aspect('equal')
ax_chlad.tick_params(colors=DIM, labelsize=7)

for ax in (ax_noether, ax_morph, ax_riem, ax_ferm):
    ax.set_facecolor(BG)
    ax.tick_params(colors=DIM, labelsize=7)
    for spine in ax.spines.values():
        spine.set_color(DIM)

# ── 3D UNS panel — occupies same figure region as ax_spiral ─────────────────
# Position is derived from the SubplotSpec so they're always co-registered.
_sp0_pos = gs[0, 0].get_position(fig)
ax_uns = fig.add_axes(
    [_sp0_pos.x0, _sp0_pos.y0, _sp0_pos.width, _sp0_pos.height],
    projection='3d'
)
ax_uns.set_facecolor(BG)
ax_uns.set_visible(False)   # hidden until UNS checkbox is ticked

# 3D panel dark panes
for pane in (ax_uns.xaxis.pane, ax_uns.yaxis.pane, ax_uns.zaxis.pane):
    pane.fill = False
    pane.set_edgecolor(DIM)
ax_uns.tick_params(colors=DIM, labelsize=5)

# ── 2D spiral panel artists ───────────────────────────────────────────────────
scat_spiral = ax_spiral.scatter([], [], s=3, c=[], cmap='plasma', alpha=0.8)
scat_zeros  = ax_spiral.scatter([], [], s=25, c=RED, marker='x', alpha=0.9, zorder=5)

# ── 3D UNS panel artists (pre-created, replaced each frame in UNS mode) ──────
_uns_scat    = [None]   # mutable container — replaced on first render
_uns_rings   = []       # list of ring Line3D objects

# ── Chladni panel artists ─────────────────────────────────────────────────────
_zero_img = np.zeros((GRID_N, GRID_N))
chlad_img = ax_chlad.imshow(_zero_img, cmap='inferno', origin='lower',
                             extent=[-1, 1, -1, 1], vmin=0, vmax=1, animated=True)
sand_scat = ax_chlad.scatter([], [], s=1, c=GOLD, alpha=0.7)

# ── Noether panel artists ─────────────────────────────────────────────────────
noether_line, = ax_noether.plot([], [], color=RED, lw=1.5)
ax_noether.axhline(y=OMEGA_ZS, color=GREEN, lw=1.0, ls='--', alpha=0.7)
ax_noether.text(0.01, OMEGA_ZS + 0.05, f"OMEGA_ZS={OMEGA_ZS}",
                color=GREEN, fontsize=7,
                transform=ax_noether.get_yaxis_transform())

# ── Morphology panel artists ──────────────────────────────────────────────────
morph_img = ax_morph.imshow(_zero_img, cmap='viridis', origin='lower',
                             extent=[-1, 1, -1, 1], animated=True)
morph_label = ax_morph.text(0.5, 0.5, "awaiting\nBAO convergence",
                             ha='center', va='center', color=DIM,
                             fontsize=10, transform=ax_morph.transAxes)

# ── Title / subtitle ─────────────────────────────────────────────────────────
title_text = fig.text(
    0.5, 0.96,
    "Cymatic Resonance of Creation  —  Universal Resonant Cavity",
    ha='center', va='top', color=GOLD, fontsize=12, fontweight='bold',
    fontfamily='serif')
phase_subtitle = fig.text(
    0.5, 0.935,
    "□Ψ = Σ[φ^{-n}·ζ(½+iγ_n)·∂J]  |  λ_0→OMEGA_ZS  |  Phase: Inertial",
    ha='center', va='top', color='#8090a0', fontsize=8)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDERS
# ══════════════════════════════════════════════════════════════════════════════

_sl_specs = [
    (0.07,  0.145, 'φ  (attractor depth)',  1.0,     2.5,        PHI,           GOLD),
    (0.07,  0.105, 'Ω  (thermal ceiling)',  5.0,     50.0,       np.e**np.pi,   VIOLET),
    (0.55,  0.145, 'ℏ_NN  (node spacing)', 0.5,     2.0,        1.0,           CYAN),
    (0.55,  0.105, 'Bias  (0 → 1/φ)',      0.0,     INV_PHI,    INV_PHI * 0.5, YELLOW),
    (0.07,  0.065, 'Drive  (plate amp)',   0.01,    1.0,        0.5,           GREEN),
]
sliders = []
for x, y, label, vmin, vmax, vinit, col in _sl_specs:
    ax_sl = plt.axes([x, y, 0.35, 0.022], facecolor='#111')
    sl = Slider(ax_sl, label, vmin, vmax, valinit=vinit, color=col)
    sl.label.set_color(WHITE)
    sl.valtext.set_color(CYAN)
    sliders.append(sl)
s_phi, s_omega, s_hbar, s_bias, s_drive = sliders

# ══════════════════════════════════════════════════════════════════════════════
# BUTTONS  +  UNS CHECKBOX
# ══════════════════════════════════════════════════════════════════════════════

_btn_y = 0.195
phase_btns = []
for i, pname in enumerate(PHASE_NAMES):
    ax_b = plt.axes([0.07 + i * 0.155, _btn_y, 0.132, 0.030])
    b = Button(ax_b, pname, color='#1a1a2e', hovercolor='#2a2a4e')
    b.label.set_color(WHITE)
    b.label.set_fontsize(8)
    b.on_clicked(lambda _, p=pname: tm.trigger(p))
    phase_btns.append(b)

ax_pause = plt.axes([0.855, _btn_y, 0.042, 0.030])
btn_pause = Button(ax_pause, '⏸', color='#1a1a2e', hovercolor='#2a2a4e')
btn_pause.label.set_color(WHITE)

# UNS checkbox — toggles 3D Fibonacci sphere for Panel 1
ax_check = plt.axes([0.902, _btn_y, 0.058, 0.032], facecolor='#111')
check_uns = CheckButtons(ax_check, ['UNS 3D'], [False])
check_uns.labels[0].set_color(GOLD)
check_uns.labels[0].set_fontsize(8)

state = {
    'paused':     False,
    'frame':      0,
    'uns_mode':   False,
    'morph_snap': None,
    'bao_history': [],
}

def _toggle_uns(label):
    state['uns_mode'] = not state['uns_mode']
    ax_spiral.set_visible(not state['uns_mode'])
    ax_uns.set_visible(state['uns_mode'])

def _toggle_pause(event):
    state['paused'] = not state['paused']
    btn_pause.label.set_text('▶' if state['paused'] else '⏸')

check_uns.on_clicked(_toggle_uns)
btn_pause.on_clicked(_toggle_pause)
fig.canvas.mpl_connect('key_press_event',
                        lambda e: _toggle_pause(None) if e.key == ' ' else None)

# ══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL NATIVE SPACE — Fibonacci sphere projection
#
# The 2D prime spiral IS the projection of this sphere onto a plane.
# UNS coordinates:
#   longitude ψ = n × GOLDEN_ANG   (same golden angle as 2D — unchanged)
#   latitude  θ = arccos(1 - 2n/N) (equal-area: equal sphere fraction per point)
#   radius    ρ = φ^{-n} × R(t)    (Fermat weight, breathing with Heartbeat)
#
# Riemann zero rings: circles at latitudes θ_γ where the cavity has nodes.
# The sphere breathes at beat frequency ω_i vs ω_e.
# When node ring spacing → OMEGA_ZS: BAO convergence, morphology snapshot.
# ══════════════════════════════════════════════════════════════════════════════

def fibonacci_sphere_coords(n_show, phi_val, t_abs, heartbeat=True):
    """Project prime indices to Fibonacci sphere in Universal Native Space.

    :param n_show: number of prime points to place
    :param phi_val: golden ratio slider value
    :param t_abs: absolute time (for breathing radius)
    :param heartbeat: if True, sphere radius breathes with Heartbeat formula
    :returns: (x, y, z, weights) arrays of length n_show
    """
    n_show = min(n_show, N_PRIMES)
    n = np.arange(1, n_show + 1, dtype=float)

    # UNS angular coordinates (same golden angle as 2D — this is the key identity)
    ga   = 2 * np.pi / phi_val**2
    psi  = n * ga                            # longitude (unbounded; sin/cos wraps)
    theta = np.arccos(np.clip(1.0 - 2*n / n_show, -1, 1))  # equal-area latitude

    # Fermat radial weight — breathing Heartbeat radius
    w = phi_val ** (-n)
    if heartbeat:
        pulse = (np.sin(t_abs * np.pi * OMEGA_I) + 1.0) / 2.0
        R = (1.0 + (phi_val - 1.0) * pulse + GAP) * 4.0   # scale for visibility
    else:
        R = 4.0
    rho = w * R

    x = rho * np.sin(theta) * np.cos(psi)
    y = rho * np.sin(theta) * np.sin(psi)
    z = rho * np.cos(theta)
    return x, y, z, w


def zeta_rings_on_sphere(phi_val, t_abs, n_total):
    """Circles on the sphere at Riemann zero latitudes.

    Each γ_n maps to the latitude where that zero's node ring sits.
    The rings are the cavity's resonance bands — nodes of the URC eigenspectrum.

    :returns: list of (x_ring, y_ring, z_ring, gamma) tuples
    """
    pulse = (np.sin(t_abs * np.pi * OMEGA_I) + 1.0) / 2.0
    R = (1.0 + (phi_val - 1.0) * pulse + GAP) * 4.0

    psi_ring = np.linspace(0, 2 * np.pi, 120)
    rings = []
    for gamma in ZETA_ZEROS[:10]:
        # Map gamma → latitude: γ_n / γ_max × π  (linear mapping to [0, π])
        lat = (gamma / ZETA_ZEROS[-1]) * np.pi
        r_ring = R * 0.9 * np.sin(lat)     # ring radius at this latitude
        z_ring = R * 0.9 * np.cos(lat)
        x_ring = r_ring * np.cos(psi_ring)
        y_ring = r_ring * np.sin(psi_ring)
        rings.append((x_ring, y_ring, np.full_like(psi_ring, z_ring), gamma))
    return rings


def render_uns_sphere(t_abs, phi_val, hbar_val, phase_name, n_show=500):
    """Draw the 3D Fibonacci sphere in Universal Native Space.

    Panel replaces the 2D spiral when UNS checkbox is active.
    The sphere breathes with the Heartbeat. Riemann zeros are node rings.
    The golden angle spiral traces a helix crossing every node ring once
    per golden-ratio step — prime gaps are ring crossings, prime clusters
    are inter-ring passages.
    """
    ax_uns.cla()
    ax_uns.set_facecolor(BG)
    for pane in (ax_uns.xaxis.pane, ax_uns.yaxis.pane, ax_uns.zaxis.pane):
        pane.fill = False
        pane.set_edgecolor(DIM)
    ax_uns.tick_params(colors=DIM, labelsize=5)

    # ── Prime points on Fibonacci sphere ──────────────────────────────────
    x, y, z, w = fibonacci_sphere_coords(n_show, phi_val, t_abs)
    colors = plt.cm.plasma(w / (w.max() + 1e-10))
    ax_uns.scatter(x, y, z, s=2, c=colors, alpha=0.7, depthshade=True)

    # ── Heartbeat sphere envelope (wireframe) ─────────────────────────────
    pulse = (np.sin(t_abs * np.pi * OMEGA_I) + 1.0) / 2.0
    R_env = (1.0 + (phi_val - 1.0) * pulse + GAP) * 4.0
    u_sph = np.linspace(0, 2*np.pi, 18)
    v_sph = np.linspace(0, np.pi,   10)
    xs = R_env * 0.92 * np.outer(np.cos(u_sph), np.sin(v_sph))
    ys = R_env * 0.92 * np.outer(np.sin(u_sph), np.sin(v_sph))
    zs = R_env * 0.92 * np.outer(np.ones_like(u_sph), np.cos(v_sph))
    ax_uns.plot_wireframe(xs, ys, zs, color=GOLD, alpha=0.06, lw=0.4)

    # ── Riemann zero rings (node circles) ─────────────────────────────────
    for x_r, y_r, z_r, gamma in zeta_rings_on_sphere(phi_val, t_abs, n_show):
        ax_uns.plot(x_r, y_r, z_r, color=RED, lw=0.8, alpha=0.50)
        # Label the first 4 zeros
        if gamma < ZETA_ZEROS[4]:
            ax_uns.text(x_r[0]*1.05, y_r[0]*1.05, z_r[0]*1.02,
                        f"γ={gamma:.2f}", color=RED, fontsize=5, alpha=0.8)

    # ── Golden helix spiral path (the Riemann spiral on the sphere) ────────
    n_helix = min(n_show, 300)
    ga = 2 * np.pi / phi_val**2
    n_h = np.arange(1, n_helix + 1, dtype=float)
    psi_h  = n_h * ga
    theta_h = np.arccos(np.clip(1.0 - 2*n_h / n_helix, -1, 1))
    r_h = R_env * 0.95
    xh = r_h * np.sin(theta_h) * np.cos(psi_h)
    yh = r_h * np.sin(theta_h) * np.sin(psi_h)
    zh = r_h * np.cos(theta_h)
    ax_uns.plot(xh, yh, zh, color=CYAN, lw=0.6, alpha=0.4)

    # ── Equatorial critical line ring Re(s)=½ ─────────────────────────────
    eq_ang = np.linspace(0, 2*np.pi, 200)
    eq_r   = R_env * 0.93
    ax_uns.plot(eq_r*np.cos(eq_ang), eq_r*np.sin(eq_ang),
                np.zeros(200), color=GOLD, lw=1.2, ls='--', alpha=0.6)

    # ── Labels ────────────────────────────────────────────────────────────
    ax_uns.set_title(
        f"FIBONACCI SPHERE — Universal Native Space\n"
        f"ψ=n×GOLDEN_ANG  θ=arccos(1-2n/N)  ρ=φ^{{-n}}×R(t)",
        color=GOLD, fontsize=7, pad=4)
    ax_uns.set_xlabel("x", color=DIM, fontsize=6, labelpad=-8)
    ax_uns.set_ylabel("y", color=DIM, fontsize=6, labelpad=-8)
    ax_uns.set_zlabel("z", color=DIM, fontsize=6, labelpad=-8)

    lim = R_env
    ax_uns.set_xlim(-lim, lim)
    ax_uns.set_ylim(-lim, lim)
    ax_uns.set_zlim(-lim, lim)

    # Slowly rotate the isometric view
    az = (t_abs * 8) % 360
    ax_uns.view_init(elev=28, azim=az)


# ══════════════════════════════════════════════════════════════════════════════
# CHLADNI FIELD ENGINE
# 2D standing wave driven by Zeta-Fermat beat frequencies.
# Nodes = matter accumulation sites = BAO wavefronts.
# ══════════════════════════════════════════════════════════════════════════════

def compute_chladni(t_abs, phi_val, hbar_val, drive_val, bias_val):
    """2D Chladni wave field U(x,y,t).

    :param t_abs: absolute time (seconds)
    :param phi_val: golden ratio slider value
    :param hbar_val: ℏ_NN node spacing multiplier
    :param drive_val: amplitude of driving
    :param bias_val: forward/backward current ratio (0 → 1/φ)
    :returns: (GRID_N, GRID_N) float array
    """
    f1 = OMEGA_I * hbar_val
    f2 = OMEGA_E * hbar_val * (1.0 + bias_val * 0.12)

    U = np.zeros((GRID_N, GRID_N))
    for n, gamma in enumerate(ZETA_ZEROS[:8]):
        k  = gamma / (18.0 * phi_val)
        An = float(PRIME_W[n]) * drive_val

        ph1 = 2 * np.pi * f1 * t_abs + n * GOLDEN_ANG
        ph2 = 2 * np.pi * f2 * t_abs + n * GOLDEN_ANG * phi_val

        U += An * (
            np.sin(k * CX * np.pi) * np.cos(k * CY * np.pi) * np.cos(ph1) +
            np.cos(k * CX * np.pi) * np.sin(k * CY * np.pi) * np.cos(ph2)
        )
    return U


def sand_positions(U, n_particles=600):
    """Sample particle positions weighted inverse to |U|² (sand at nodes).

    :param U: Chladni field array
    :param n_particles: number of sand grains
    :returns: (x_positions, y_positions) in [-1, 1]
    """
    prob = np.exp(-U**2 * 20.0)
    prob /= prob.sum() + 1e-30
    flat = np.random.choice(GRID_N * GRID_N, size=n_particles,
                            replace=False, p=prob.ravel())
    iy, ix = np.unravel_index(flat, (GRID_N, GRID_N))
    return ix / GRID_N * 2 - 1, iy / GRID_N * 2 - 1


def bao_ratio(U):
    """Mean node spacing normalized to OMEGA_ZS. Returns ~1.0 at BAO convergence."""
    diag = U[np.arange(GRID_N), np.arange(GRID_N)]
    crossings = int(np.sum(np.diff(np.sign(diag)) != 0))
    if crossings < 2:
        return 0.0
    return (1.0 / crossings) / OMEGA_ZS


def classify_morphology(U):
    """Label galaxy morphology from node geometry.

    :returns: one of 'spiral', 'elliptical', 'cluster', 'filament', 'void'
    """
    nf = float(np.mean(np.abs(U) < 0.12))
    if nf < 0.02:   return 'void'
    if nf < 0.06:   return 'spiral'
    if nf < 0.15:   return 'elliptical'
    if nf < 0.28:   return 'cluster'
    return 'filament'


# ══════════════════════════════════════════════════════════════════════════════
# NOETHER VIOLATION — from Gemini_Transition_EHS.py
# J_red × J_blue cross product at the boundary crossing
# ══════════════════════════════════════════════════════════════════════════════

def noether_violation(t, phi_val, hbar_val):
    """Forward/backward current cross-product magnitude over boundary crossing.

    :returns: (x_axis, violation_array) both length 200
    """
    t_vals = np.linspace(1.5, 0.5, 200)
    J_red  = np.sin(t * OMEGA_I * t_vals) * phi_val
    J_blue = np.cos(t * OMEGA_E * t_vals) * phi_val
    J_cross = np.abs(J_red * J_blue)
    J_cross[int(np.argmin(np.abs(t_vals - 1.0)))] = hbar_val * 1.5
    return np.arange(200), J_cross


# ══════════════════════════════════════════════════════════════════════════════
# SPIRAL COORDINATES per phase (LERP interpolated via TransitionManager)
# Golden angle corrected from conjecture_proof.py: idx × 2π/φ²
# ══════════════════════════════════════════════════════════════════════════════

def spiral_coords(phase, t, phi_val, hbar_val, bias_val):
    """Return (theta, r, weights) for the named phase.

    :param phase: phase name string
    :param t: cycle time [0, 1]
    """
    ga = 2 * np.pi / phi_val**2
    n  = np.arange(1, 601)

    if phase == "Inertial":
        r     = n * 0.02 * t
        theta = n * (np.pi / 2) * TWO_OVER_PI
        w     = np.ones(len(n))

    elif phase == "Metric Swap":
        base_r = np.maximum(n * 0.02 * max(t, 0.01), 1e-6)
        r      = (1.0 / base_r) * (1.0 + GAP)
        theta  = n * TWO_OVER_PI + np.pi / 2 * hbar_val
        w      = np.ones(len(n))

    elif phase == "Heartbeat":
        pulse    = (np.sin(t * np.pi * OMEGA_I) + 1.0) / 2.0
        r_target = 1.0 + (phi_val - 1.0) * pulse
        r        = (np.sqrt(n) * 0.5) * (r_target + GAP)
        theta    = n * TWO_OVER_PI * max(t, 1e-3)
        w        = np.ones(len(n))

    elif phase == "Prime Spiral":
        n_show  = min(N_PRIMES, max(20, int(t * N_PRIMES * 1.6)))
        idx     = PRIME_INDICES[:n_show]
        theta   = idx * ga
        r       = PRIME_R[:n_show]
        w       = phi_val ** (-idx.astype(float))

    else:  # "Horizon"
        idx   = PRIME_INDICES
        theta = idx * ga
        r     = PRIME_R
        w     = phi_val ** (-idx.astype(float)) * (1.0 + bias_val)

    return np.asarray(theta), np.asarray(r), np.asarray(w)


# ══════════════════════════════════════════════════════════════════════════════
# HORIZON INVARIANCE — from Claude rewrite Phase 5
# Hardy Z-function (Riemann) LEFT + Fermat lattice RIGHT at Re(s)=½
# ══════════════════════════════════════════════════════════════════════════════

def render_horizon_panels(t, phi_val, omega_val):
    """Riemann wave LEFT meets Fermat lattice RIGHT at the critical line."""
    ax_riem.cla(); ax_ferm.cla()
    for ax in (ax_riem, ax_ferm):
        ax.set_facecolor(BG)
        ax.tick_params(colors=DIM, labelsize=7)
        for spine in ax.spines.values():
            spine.set_color(DIM)

    x     = np.linspace(0, 1.0, 2000)
    freq  = 8.0 + t * 4.0
    decay = np.exp(-8 * (x - 0.5)**2 * (1.0 + t))
    z_wave = np.sin(2 * np.pi * freq * x) * (1.0 - x) * decay

    ax_riem.plot(x, z_wave, color=CYAN, lw=1.5, alpha=0.9)
    ax_riem.axhline(y=0, color=RED,  lw=0.6, ls='--', alpha=0.5)
    ax_riem.axvline(x=0.5, color=GOLD, lw=1.5, ls='--', alpha=0.8)

    zc = x[:-1][(z_wave[:-1] * z_wave[1:]) < 0]
    if len(zc):
        ax_riem.scatter(zc, np.zeros(len(zc)), c=RED, s=15, zorder=5)

    intersect_y = float(np.sin(2 * np.pi * freq * 0.5)) * float(decay[1000])
    ax_riem.scatter([0.5], [intersect_y], s=120, c=GOLD, zorder=10,
                    alpha=min(1.0, t * 3))
    ax_riem.set_xlim(0, 1); ax_riem.set_ylim(-1.2, 1.2)
    ax_riem.set_title("RIEMANN WAVE  Re(s)=½", color=CYAN, fontsize=8, pad=3)
    ax_riem.set_xlabel("← critical line", color=GOLD, fontsize=7)

    ga    = 2 * np.pi / phi_val**2
    n_s   = min(N_PRIMES, max(20, int(t * 600 + 60)))
    idx   = PRIME_INDICES[:n_s]
    p_r   = PRIME_R[:n_s]
    p_w   = phi_val ** (-idx.astype(float))
    r_max = max(p_r.max(), 1e-6)
    x_f   = 0.5 + (p_r / r_max) * 0.47
    y_f   = np.sin(idx * ga) * (p_r / r_max) * 0.8
    ax_ferm.scatter(x_f, y_f, s=np.clip(p_w * 1000 + 0.5, 0.5, 18),
                    c=p_w / p_w.max(), cmap='Greens', alpha=0.8, vmin=0, vmax=1)
    ax_ferm.axvline(x=0.5, color=GOLD, lw=1.5, ls='--', alpha=0.8)
    ax_ferm.scatter([0.5], [intersect_y * 0.8], s=120, c=GOLD, zorder=10,
                    alpha=min(1.0, t * 3))
    ax_ferm.set_xlim(0, 1); ax_ferm.set_ylim(-1.0, 1.0)
    ax_ferm.set_title("FERMAT LATTICE  φ^{-n} weights", color=GREEN, fontsize=8, pad=3)
    ax_ferm.set_xlabel("critical line →", color=GOLD, fontsize=7)
    ax_ferm.text(0.98, 0.02, "entropy = 5/6", ha='right', va='bottom',
                 color=GOLD, fontsize=7, transform=ax_ferm.transAxes)


# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION LOOP
# ══════════════════════════════════════════════════════════════════════════════

def animate(frame_num):
    if state['paused']:
        return []

    state['frame'] += 1
    f = state['frame']
    tm.advance()

    phi_v   = s_phi.val
    omega_v = s_omega.val
    hbar_v  = s_hbar.val
    bias_v  = s_bias.val
    drive_v = s_drive.val
    t       = (f % 300) / 300.0
    t_abs   = f * 0.033

    # ── Panel 1a: 2D Prime Spiral (visible when UNS off) ─────────────────
    if not state['uns_mode']:
        try:
            th_a, r_a, w_a = spiral_coords(tm.source, t, phi_v, hbar_v, bias_v)
            th_b, r_b, w_b = spiral_coords(tm.target, t, phi_v, hbar_v, bias_v)
            n = min(len(th_a), len(th_b), 600)
            alpha = tm.alpha
            th_i  = th_a[:n] * (1-alpha) + th_b[:n] * alpha
            r_i   = r_a[:n]  * (1-alpha) + r_b[:n]  * alpha
            w_i   = w_a[:n]  * (1-alpha) + w_b[:n]  * alpha
            scat_spiral.set_offsets(np.column_stack([th_i, r_i]))
            scat_spiral.set_array(w_i / (w_i.max() + 1e-10))
            scat_spiral.set_color(tm.point_color)
            ax_spiral.set_ylim(0, max(r_i.max() * 1.1, 2.0))
            z_r = np.sqrt(ZETA_ZEROS)
            z_t = (ZETA_ZEROS / ALPHA_INV * 2 * np.pi) % (2 * np.pi)
            scat_zeros.set_offsets(np.column_stack([z_t, z_r]))
            if tm.in_transition:
                ax_spiral.set_title(
                    f"Transition: {tm.source} → {tm.target}  (entropy spike ↑)",
                    color=MAGENTA, fontsize=8, pad=4)
            else:
                ax_spiral.set_title(f"Phase: {tm.target}", color=GOLD,
                                    fontsize=8, pad=4)
        except Exception:
            pass

    # ── Panel 1b: 3D Fibonacci Sphere (visible when UNS on) ──────────────
    else:
        try:
            n_show = min(N_PRIMES, max(50, int(t * 800 + 100)))
            render_uns_sphere(t_abs, phi_v, hbar_v, tm.target, n_show)
        except Exception:
            pass

    # ── Subtitle ──────────────────────────────────────────────────────────
    if state['uns_mode']:
        phase_subtitle.set_text(
            "UNS MODE: Fibonacci sphere  |  ψ=n×GOLDEN_ANG  θ=arccos(1-2n/N)  "
            "ρ=φ^{-n}·R(t)  |  RED rings = Riemann zero nodes")
    elif tm.in_transition:
        phase_subtitle.set_text(
            f"LERP α={tm.alpha:.2f}  |  entropy spike in Noether panel  |  "
            f"cyan→magenta→cyan")
    else:
        phase_subtitle.set_text(
            f"□Ψ=Σ[φ^{{-n}}·ζ(½+iγ_n)·∂J]  λ_0→{OMEGA_ZS}  Phase: {tm.target}")

    # ── Panel 2: Chladni field ────────────────────────────────────────────
    U = None
    try:
        U = compute_chladni(t_abs, phi_v, hbar_v, drive_v, bias_v)
        U_sq      = U**2
        U_sq_norm = U_sq / (U_sq.max() + 1e-10)
        chlad_img.set_data(U_sq_norm)
        chlad_img.set_clim(0, 1)
        x_s, y_s = sand_positions(U, n_particles=500)
        sand_scat.set_offsets(np.column_stack([x_s, y_s]))
        br = bao_ratio(U)
        state['bao_history'].append(br)
        if len(state['bao_history']) > 300:
            state['bao_history'].pop(0)
        converging = abs(br - 1.0) < 0.08
        ax_chlad.set_title(
            f"CHLADNI FIELD  BAO={br:.3f} (target 1.0)",
            color=GREEN if converging else GOLD, fontsize=8, pad=3)
        if converging and (f % 90 == 0):
            state['morph_snap'] = (U_sq_norm.copy(), classify_morphology(U))
    except Exception:
        pass

    # ── Panel 3: Noether violation ────────────────────────────────────────
    try:
        x_v, v_arr = noether_violation(t, phi_v, hbar_v)
        noether_line.set_data(x_v, v_arr)
        ax_noether.set_xlim(0, 200)
        ax_noether.set_ylim(-0.05, max(v_arr.max(), 0.5) * 1.15)
        ax_noether.set_title(
            "NOETHER VIOLATION  ∂_μJ^μ  (spike = boundary crossing)",
            color=RED, fontsize=8, pad=3)
        ax_noether.set_ylabel("J_cross", color=DIM, fontsize=7)
    except Exception:
        pass

    # ── Panel 4: Morphology snapshot ──────────────────────────────────────
    try:
        if state['morph_snap'] is not None:
            snap, name = state['morph_snap']
            morph_img.set_data(snap)
            morph_img.set_clim(0, 1)
            col = MORPH_COLORS.get(name, WHITE)
            morph_label.set_text(f"BAO ≈ OMEGA_ZS\n→ {name.upper()}")
            morph_label.set_color(col)
            ax_morph.set_title(f"MORPHOLOGY: {name}", color=col, fontsize=8, pad=3)
        else:
            br_now = state['bao_history'][-1] if state['bao_history'] else 0.0
            morph_label.set_text(
                f"BAO: {br_now:.3f}\ntarget: 1.0 ± 0.08\nawaiting...")
            ax_morph.set_title("MORPHOLOGY  (awaiting BAO)", color=DIM,
                               fontsize=8, pad=3)
    except Exception:
        pass

    # ── Panels 5+6: Horizon Invariance ────────────────────────────────────
    try:
        if tm.target == "Horizon" and tm.alpha > 0.5:
            render_horizon_panels(t, phi_v, omega_v)
    except Exception:
        pass

    return []


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER ANNOTATIONS
# ══════════════════════════════════════════════════════════════════════════════

_note = dict(ha='left', color=DIM, fontsize=7, fontfamily='monospace')
fig.text(0.06, 0.220,
    f"φ={PHI:.4f}  1/φ={INV_PHI:.4f} (bias=1/φ, NOT 2/e)  "
    f"GAP={GAP}  OMEGA_ZS={OMEGA_ZS}  GOLDEN_ANG={np.degrees(GOLDEN_ANG):.3f}°",
    **_note)
fig.text(0.06, 0.206,
    f"URC: □Ψ=Σ[φ^{{-n}}·ζ(½+iγ_n)·∂J]  λ_n=γ_n²·φ^{{-n}}  "
    f"λ_0→OMEGA_ZS  Boundary: Ψ|_{{S⁷}}=0  Driving: J⁰≈H(t)",
    **_note)
fig.text(0.06, 0.192,
    f"UNS: ψ=n×GOLDEN_ANG  θ=arccos(1-2n/N)  ρ=φ^{{-n}}·R  "
    f"[UNS checkbox] = Fibonacci sphere  ω_i={OMEGA_I} ≠ ω_e={OMEGA_E} (the hum)",
    **_note)

print("CRC Engine — Cymatic Resonance of Creation — ACTIVE")
print(f"  φ={PHI:.6f}  INV_PHI={INV_PHI:.6f}  GAP={GAP}  OMEGA_ZS={OMEGA_ZS}")
print(f"  GOLDEN_ANG={np.degrees(GOLDEN_ANG):.4f}° (idx×2π/φ², corrected)")
print(f"  Beat: ω_i={OMEGA_I} ≠ ω_e={OMEGA_E}  → Lissajous node complexity")
print(f"  Bias: 0 → 1/φ={INV_PHI:.4f}  (replaces Gemini's 2/e={2/np.e:.4f})")
print()
print("  URC: □Ψ = Σ[φ^{-n}·ζ(½+iγ_n)·∂J]")
print(f"  Eigenspectrum: λ_n=γ_n²·φ^{{-n}}  Ground state: λ_0→{OMEGA_ZS}")
print(f"  Boundary: Ψ|_{{S⁷}}=0  (sedenion zero-divisor surface)")
print(f"  Driving: J^0 ≈ H(t)  (Hubble parameter = plate driver)")
print()
print("  [UNS] checkbox → Fibonacci sphere (Universal Native Space)")
print("  ψ=n×GOLDEN_ANG  θ=arccos(1-2n/N)  ρ=φ^{-n}·R(t)")
print("  Red rings = Riemann zero node circles  Gold ring = Re(s)=½ equator")
print("  Sphere breathes at ω_i/ω_e beat  Slow rotation = isometric view")
print()
print("  Phase HORIZON = money shot (Riemann wave ↔ Fermat lattice at Re(s)=½)")

# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════

ani = FuncAnimation(fig, animate, frames=10000, interval=50, blit=False)
plt.show()
