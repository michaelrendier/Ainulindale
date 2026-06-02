#!/usr/bin/env python3
"""
witches_hat_triptych.py
=======================
Three-panel animation: null cone ↣ galactic particle (inside-out conformal inversion).

Three simultaneous views of the same transformation:

  LEFT    — THE POTENTIAL      V(r) = -μ²r² + λr⁴  (Mexican Hat / Sombrero)
  CENTER  — THE BRIM           r = R_H = 1/√2  (fixed through all of spacetime)
  RIGHT   — THE ACTION         S(t) = ∫L dt  [Lichtenberg Lagrangian of Action Potential]

The inside-out transformation:   r  →  R_H² / r
  Null cone tip (r→0)   maps to the outer halo (r→∞)
  Cone fabric (r>R_H)   maps to the galaxy interior (r<R_H)
  The brim (r=R_H)      maps to itself — the only fixed point

The Lichtenberg Lagrangian of Action Potential (new physics):
  The action S(t) charges up like a neuron — building toward the brim threshold.
  At t_brim the system FIRES (the action potential): brim crossing = threshold voltage.
  Post-brim: the action settles into the attractor — the galaxy state.
  The branching structure of near-paths IS the Hawking soft hair on the horizon.
  Paths that don't cross the brim = sub-threshold dendrites that die.
  The minimum-action path = the physical path = the Lichtenberg trunk.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, FancyArrow
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap

np.random.seed(42)

# ── Physics constants ──────────────────────────────────────────────────────────
MU  = 1.0
LAM = 1.0
R_H = MU / np.sqrt(2.0 * LAM)          # = 1/√2 ≈ 0.7071  (the brim)

# ── Field equations ────────────────────────────────────────────────────────────
def V(r):
    """Mexican Hat / Sombrero potential."""
    return -MU**2 * r**2 + LAM * r**4

def dV(r):
    return -2*MU**2*r + 4*LAM*r**3

def r_trans(r0, t):
    """Conformal inversion path, linear interpolation in t."""
    return (1.0 - t)*r0 + t*(R_H**2 / r0)

def rdot(r0):
    """dr/dt — constant for linear inversion path."""
    return R_H**2/r0 - r0

def t_brim(r0):
    """Transition parameter at which r(t) = R_H (the firing moment)."""
    # r(t) = R_H  ⟹  t = r0 / (R_H + r0)
    return r0 / (R_H + r0)

def lagrangian(r0, t):
    r  = r_trans(r0, t)
    rd = rdot(r0)
    return 0.5*rd**2 - V(r)

def action(r0, T_arr):
    """Accumulated action S(t) = ∫₀ᵗ L dt'."""
    L_arr = np.array([lagrangian(r0, t) for t in T_arr])
    dt    = T_arr[1] - T_arr[0]
    return np.cumsum(L_arr) * dt


# ── Pre-compute all paths ──────────────────────────────────────────────────────
N_FRAMES = 360
T = np.linspace(0, 1, N_FRAMES)

# Lichtenberg ensemble: paths at varying r0
# Inside brim: small r0 → will invert to large r (cone tip → halo)
r0_in  = np.linspace(0.09, 0.67, 32)
# Outside brim: large r0 → will invert to small r (cone fabric → galaxy interior)
r0_out = np.linspace(0.78, 1.92, 32)
r0_all = np.concatenate([r0_in, r0_out])
N_PATHS = len(r0_all)

# All path data: shape (N_PATHS, N_FRAMES)
R_mat = np.array([r_trans(r0, T) for r0 in r0_all])
S_mat = np.array([action(r0, T)  for r0 in r0_all])
rdot_vals    = np.array([rdot(r0) for r0 in r0_all])
t_brim_vals  = np.array([t_brim(r0) for r0 in r0_all])

# Attractor = path with minimum |rdot| (barely crosses brim — minimum kinetic energy)
attractor_idx = np.argmin(np.abs(rdot_vals))
S_attractor   = S_mat[attractor_idx]

# Deviation: how far is each path from the attractor at t=1?
S_final  = S_mat[:, -1]
S_dev    = np.abs(S_final - S_final.min())
S_dev   /= (S_dev.max() + 1e-10)

# Pre-compute "firing intensity" per path per frame
# Each path fires when r(t) ≈ R_H
firing_intensity = np.exp(-40 * (R_mat - R_H)**2)   # (N, N_FRAMES)

# Path visual properties
def make_color(r0, dev):
    """Attractor (dev=0) → cyan. Deviating → dim red (inside) or dim blue (outside)."""
    d = dev
    if r0 < R_H:
        return (0.3 + 0.7*d,  0.8 - 0.6*d,  0.8 - 0.4*d)
    else:
        return (0.2 + 0.4*d,  0.5 - 0.3*d,  1.0 - 0.1*d)

path_colors = [make_color(r0, d) for r0, d in zip(r0_all, S_dev)]
path_alphas = np.clip(0.85 - 0.70*S_dev, 0.12, 0.88)
path_lws    = 0.4 + 2.2*(1.0 - S_dev)


# ── Figure ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 20, 7
fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor='#020208', dpi=100)

fig.text(0.5, 0.975,
         'WITCHES HAT  ⟶  GALACTIC PARTICLE  ·  NULL CONE CONFORMAL INVERSION  ·  r → R_H²/r',
         color='#8899cc', fontsize=9.5, ha='center', va='top')

gs = GridSpec(1, 3, figure=fig,
              left=0.055, right=0.975, wspace=0.20, bottom=0.11, top=0.91)
ax1 = fig.add_subplot(gs[0])   # Potential
ax2 = fig.add_subplot(gs[1])   # Brim
ax3 = fig.add_subplot(gs[2])   # Action / Lichtenberg

BG = '#020208'
GRID = '#111128'
for ax in (ax1, ax2, ax3):
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_edgecolor('#1a1a33')
    ax.tick_params(colors='#445566', labelsize=7)


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 1: THE POTENTIAL
# ══════════════════════════════════════════════════════════════════════════════
ax1.set_title('THE POTENTIAL', color='#7799ff', fontsize=9, pad=8, fontweight='bold')
ax1.set_xlabel('radius  r', color='#556688', fontsize=8)
ax1.set_ylabel('V(r)  =  −μ²r²  +  λr⁴', color='#556688', fontsize=8)
ax1.set_xlim(0.0, 2.15)
ax1.set_ylim(-0.33, 0.85)

r_curve = np.linspace(0.005, 2.15, 1200)
V_curve = V(r_curve)

# Shaded regions
ax1.fill_between(r_curve, V_curve, -0.33,
                  where=(r_curve <= R_H), color='#cc2211', alpha=0.14)
ax1.fill_between(r_curve, V_curve, -0.33,
                  where=(r_curve >= R_H), color='#2233cc', alpha=0.14)
ax1.plot(r_curve, V_curve, color='#5566aa', lw=1.6, zorder=5)
ax1.axhline(0, color=GRID, lw=0.6)
ax1.axvline(R_H, color='#00cccc', lw=1.1, ls='--', alpha=0.65, zorder=4)

# Brim annotation
ax1.plot(R_H, V(R_H), 'o', color='#00ffff', ms=7, zorder=15)
ax1.annotate(f'Brim  r=R_H\nσ=½ node\nV={V(R_H):.4f}',
             xy=(R_H, V(R_H)),
             xytext=(R_H + 0.38, V(R_H) + 0.22),
             color='#00eeee', fontsize=7,
             arrowprops=dict(arrowstyle='->', color='#00aaaa', lw=0.8))

# Labels
ax1.text(0.20, -0.295, 'J_pos\nMatter 31%', color='#ff6655', fontsize=7, ha='center')
ax1.text(1.55, -0.295, 'J_neg\nΛ dark energy 69%', color='#5577ff', fontsize=7, ha='center')

# Animated: moving dot + phase label
dot_v, = ax1.plot([], [], 'o', ms=12, zorder=20)
phase_lbl = ax1.text(0.04, 0.94, '', color='#aabbcc', fontsize=7.5,
                      transform=ax1.transAxes, va='top')

# Ghost trail (last 20 positions)
TRAIL_LEN = 25
trail_v, = ax1.plot([], [], '-', color='#2244aa', lw=0.8, alpha=0.4, zorder=8)
trail_r_buf = np.full(TRAIL_LEN, np.nan)
trail_V_buf = np.full(TRAIL_LEN, np.nan)


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 2: THE BRIM
# ══════════════════════════════════════════════════════════════════════════════
ax2.set_title('THE BRIM  r = R_H  [The Fixed Point]', color='#7799ff',
               fontsize=9, pad=8, fontweight='bold')
ax2.set_aspect('equal')
LIM2 = 2.02
ax2.set_xlim(-LIM2, LIM2)
ax2.set_ylim(-LIM2, LIM2)
ax2.axis('off')

# Guide circles
for rr, lw_, a_ in [(0.5, 0.3, 0.3), (1.0, 0.4, 0.4), (1.5, 0.3, 0.3), (2.0, 0.3, 0.3)]:
    ax2.add_patch(Circle((0, 0), rr, fill=False, color='#111133', lw=lw_, alpha=a_))

# Interior fill (J_pos / matter)
th = np.linspace(0, 2*np.pi, 300)
ax2.fill(R_H*np.cos(th), R_H*np.sin(th), color='#ff1111', alpha=0.09)

# Exterior fill (J_neg / Λ) — use a large filled circle minus interior
outer_R = 2.02
ax2.fill(np.r_[outer_R*np.cos(th), R_H*np.cos(th[::-1])],
          np.r_[outer_R*np.sin(th), R_H*np.sin(th[::-1])],
          color='#1122cc', alpha=0.07)

# THE BRIM CIRCLE — never moves
brim_circ = Circle((0, 0), R_H, fill=False, color='#00ffff', lw=2.4, zorder=50)
ax2.add_patch(brim_circ)
ax2.text(0, R_H + 0.11, 'σ = ½\n event horizon', color='#00ffff',
          fontsize=6.5, ha='center', va='bottom', zorder=55)

# Axis labels (inside/outside)
ax2.text(-LIM2+0.08,  LIM2-0.12, 'J_pos  (matter)', color='#ff5544', fontsize=7)
ax2.text(-LIM2+0.08,  LIM2-0.28, 'J_neg  (Λ dark energy)', color='#4466ff', fontsize=7)
ax2.text(-LIM2+0.08, -LIM2+0.12, 'Brim  ─ ─ ─', color='#00cccc', fontsize=7)

# Spokes: show radial inversion at 20 angles × 4 r0 values
N_SPK_ANG  = 20
SPK_ANGLES = np.linspace(0, 2*np.pi, N_SPK_ANG, endpoint=False)
r0_spk_in  = [0.22, 0.52]     # inside brim
r0_spk_out = [0.94, 1.62]     # outside brim
r0_spk     = r0_spk_in + r0_spk_out
spk_cols   = ['#ff4433', '#ff6655', '#4455ff', '#6677ff']
spk_sizes  = [5, 4, 4, 3]

spoke_pts = []
for ang in SPK_ANGLES:
    for r0_, col_, sz_ in zip(r0_spk, spk_cols, spk_sizes):
        pt_, = ax2.plot([], [], 'o', color=col_, ms=sz_, alpha=0.8, zorder=20)
        spoke_pts.append((pt_, r0_, ang))

# Inversion arrows (static, 8 directions, drawn once per frame via set_data)
arrow_base = {}
ARROW_ANGS = np.linspace(0, 2*np.pi, 8, endpoint=False)
for ang_ in ARROW_ANGS:
    arr_in,  = ax2.plot([], [], '->', color='#ff4433', lw=0.7, alpha=0.5, zorder=12)
    arr_out, = ax2.plot([], [], '->', color='#4455ff', lw=0.7, alpha=0.5, zorder=12)
    arrow_base[ang_] = (arr_in, arr_out)

brim_t2 = ax2.text(0.0, -LIM2+0.12, '', color='#88aacc', fontsize=7.5, ha='center', zorder=30)

# Glow circle (flashes at brim crossing)
glow_circ = Circle((0, 0), R_H, fill=False, color='white', lw=0, alpha=0, zorder=40)
ax2.add_patch(glow_circ)


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 3: THE ACTION — Lichtenberg Lagrangian of Action Potential
# ══════════════════════════════════════════════════════════════════════════════
ax3.set_title(
    'THE ACTION   S(t) = ∫L dt   [Lichtenberg Lagrangian of Action Potential]',
    color='#7799ff', fontsize=9, pad=8, fontweight='bold'
)
ax3.set_xlabel('transition  t  ∈ [0 → 1]', color='#556688', fontsize=8)
ax3.set_ylabel('Action  S(t)', color='#556688', fontsize=8)

S_ymin = S_mat.min() - 0.08
S_ymax = S_mat.max() + 0.22
ax3.set_xlim(0, 1.0)
ax3.set_ylim(S_ymin, S_ymax)

# Background: divide into pre-brim and post-brim regions
ax3.axvspan(0, 0.5, color='#ff1111', alpha=0.035)
ax3.axvspan(0.5, 1, color='#1122ff', alpha=0.035)
ax3.axhline(S_final.min(), color='#ffaa22', lw=0.8, alpha=0.4, ls=':', zorder=2)
ax3.text(0.03, S_final.min() + 0.04, 'attractor level', color='#ffaa22', fontsize=6.5)

# Brim crossing line (t≈0.5 for the symmetric path)
ax3.axvline(0.5, color='#00cccc', lw=0.9, alpha=0.5, ls='--', zorder=3)
ax3.text(0.52, S_ymax - 0.08, 'Brim\n(firing)', color='#00cccc', fontsize=6.5, va='top')

# Phase labels
ax3.text(0.12, S_ymin + 0.04, 'charging ↑', color='#ff6655', fontsize=7, alpha=0.7)
ax3.text(0.65, S_ymin + 0.04, 'galaxy forming ↺', color='#5577ff', fontsize=7, alpha=0.7)

# ── Lichtenberg tree: all paths ───────────────────────────────────────────────
# Each path is an S(t) curve. Paths cluster near the attractor = Lichtenberg trunk.
# Branching = spread of firing times t_brim(r0) across different r0 values.

action_lines = []
for i in range(N_PATHS):
    ln, = ax3.plot([], [], '-',
                   color=path_colors[i],
                   lw=float(path_lws[i]),
                   alpha=float(path_alphas[i]),
                   zorder=3 + int(7*(1.0 - S_dev[i])))
    action_lines.append(ln)

# The attractor trunk (minimum action path)
trunk, = ax3.plot([], [], '-', color='#00ffee', lw=2.8, alpha=0.95, zorder=20)

# "Firing" burst markers — per path, shows when each path crosses brim
# (drawn as small flashes along the S-axis at their t_brim value)
fire_markers = []
for i in range(N_PATHS):
    fm, = ax3.plot([], [], '*', color='white', ms=0, alpha=0, zorder=25)
    fire_markers.append(fm)

# Action gauge
action_gauge = ax3.text(0.67, 0.94, '', color='#ffdd00',
                          fontsize=9.5, transform=ax3.transAxes, fontweight='bold')
# Phase text
phase_lbl3 = ax3.text(0.67, 0.86, '', color='#88ccff',
                        fontsize=7.5, transform=ax3.transAxes)
# "FIRING" flash text
firing_flash = ax3.text(0.5, 0.55, '', color='white', fontsize=20,
                          transform=ax3.transAxes, ha='center', va='center',
                          fontweight='bold', alpha=0)
# Δ annotation (deviation spread = soft hair)
ax3.text(0.67, 0.78, 'Branch spread\n= Hawking soft hair', color='#776699',
          fontsize=6.5, transform=ax3.transAxes)


# ── Animation ──────────────────────────────────────────────────────────────────
def init():
    dot_v.set_data([], [])
    trail_v.set_data([], [])
    for pt, _, _ in spoke_pts:
        pt.set_data([], [])
    for ang_ in ARROW_ANGS:
        arrow_base[ang_][0].set_data([], [])
        arrow_base[ang_][1].set_data([], [])
    for ln in action_lines:
        ln.set_data([], [])
    trunk.set_data([], [])
    for fm in fire_markers:
        fm.set_data([], [])
        fm.set_markersize(0)
        fm.set_alpha(0)
    return []


def update(frame):
    global trail_r_buf, trail_V_buf
    t   = T[frame]
    idx = frame

    # ── Panel 1: Potential ────────────────────────────────────────────────────
    # Main path: r0 = 0.06 (near cone tip, will map to far outer halo)
    r0_main = 0.06
    r_now   = r_trans(r0_main, t)
    col_now = '#ff5544' if r_now < R_H else '#4466ff'
    V_now   = V(r_now)

    # Pulse size at brim crossing
    prox = np.exp(-35*(r_now - R_H)**2)
    dot_v.set_data([r_now], [V_now])
    dot_v.set_color(col_now)
    dot_v.set_markersize(10 + 12*prox)

    # Trail
    trail_r_buf = np.roll(trail_r_buf, -1)
    trail_V_buf = np.roll(trail_V_buf, -1)
    trail_r_buf[-1] = r_now
    trail_V_buf[-1] = V_now
    valid = ~np.isnan(trail_r_buf)
    trail_v.set_data(trail_r_buf[valid], trail_V_buf[valid])

    # Phase label
    if r_now < R_H - 0.06:
        phase_str = 'null cone  [charging]'
    elif r_now < R_H + 0.06:
        phase_str = '>>> BRIM CROSSING <<<'
    else:
        phase_str = 'galaxy forming  [post-brim]'
    phase_lbl.set_text(f't = {t:.3f}   {phase_str}')
    phase_lbl.set_color('#ffffff' if prox > 0.3 else '#aabbcc')

    # ── Panel 2: Brim ─────────────────────────────────────────────────────────
    # Overall "firing" glow
    total_fire = np.mean(firing_intensity[:, idx])
    glow_circ.set_linewidth(4.0 * total_fire)
    glow_circ.set_alpha(0.6 * total_fire)

    # Spoke dots: show current r(t) position
    for pt, r0_spk_, ang_ in spoke_pts:
        r_sp = r_trans(r0_spk_, t)
        # Soft-hair wobble near brim
        prox_sp = np.exp(-40*(r_sp - R_H)**2)
        wobble  = 0.025 * prox_sp * np.sin(frame*0.2 + r0_spk_*10 + ang_)
        ang_disp = ang_ + wobble
        r_disp   = r_sp * (1 + 0.01*prox_sp*np.sin(frame*0.3))
        pt.set_data([r_disp*np.cos(ang_disp)], [r_disp*np.sin(ang_disp)])
        pt.set_markersize(4 + 6*prox_sp)
        pt.set_alpha(0.7 + 0.3*prox_sp)

    # Inversion arrows: draw from r0_in → R_H and R_H → inverted(r0_out)
    for ang_ in ARROW_ANGS:
        # Inside→brim arrow
        r_a_in = r_trans(0.38, t)
        x0_i, y0_i = 0.38*np.cos(ang_),    0.38*np.sin(ang_)
        x1_i, y1_i = r_a_in*np.cos(ang_),  r_a_in*np.sin(ang_)
        arrow_base[ang_][0].set_data([x0_i, x1_i], [y0_i, y1_i])
        # Outside→brim arrow
        r_a_out = r_trans(1.35, t)
        x0_o, y0_o = 1.35*np.cos(ang_),    1.35*np.sin(ang_)
        x1_o, y1_o = r_a_out*np.cos(ang_), r_a_out*np.sin(ang_)
        arrow_base[ang_][1].set_data([x0_o, x1_o], [y0_o, y1_o])

    brim_t2.set_text(f'  t = {t:.3f}   |   Brim = fixed  r = {R_H:.4f}')

    # ── Panel 3: Action / Lichtenberg ─────────────────────────────────────────
    # Draw all paths up to current frame
    for i, ln in enumerate(action_lines):
        ln.set_data(T[:idx+1], S_mat[i, :idx+1])

    # Attractor trunk
    trunk.set_data(T[:idx+1], S_attractor[:idx+1])

    # Firing markers: each path fires at its own t_brim
    for i, fm in enumerate(fire_markers):
        tb = t_brim_vals[i]
        if t >= tb:
            # Already fired — show a brief flash that then fades
            age = t - tb           # how long ago it fired
            flash_alpha = np.exp(-15*age) * (1 - S_dev[i]*0.8)
            fm.set_data([tb], [S_mat[i, int(tb * (N_FRAMES-1))]])
            fm.set_markersize(6 + 8*np.exp(-15*age))
            fm.set_alpha(float(flash_alpha))
        else:
            fm.set_markersize(0)
            fm.set_alpha(0)

    # Action gauge (attractor path)
    S_now = S_attractor[idx]
    action_gauge.set_text(f'S = {S_now:+.4f}')

    # Phase text
    r_att_now = R_mat[attractor_idx, idx]
    prox_att  = np.exp(-35*(r_att_now - R_H)**2)
    if r_att_now < R_H - 0.05:
        phase_lbl3.set_text('pre-brim  [action potential charging]')
        phase_lbl3.set_color('#ff9966')
    elif prox_att > 0.3:
        phase_lbl3.set_text('FIRING  —  threshold crossed')
        phase_lbl3.set_color('#ffffff')
    else:
        phase_lbl3.set_text('post-brim  [galaxy / attractor]')
        phase_lbl3.set_color('#66aaff')

    # "FIRING" flash text
    max_fire = firing_intensity[:, idx].max()
    if max_fire > 0.05:
        firing_flash.set_text('⚡ FIRE ⚡')
        firing_flash.set_alpha(float(min(max_fire * 1.5, 0.95)))
        firing_flash.set_color('#ffffaa')
    else:
        firing_flash.set_alpha(0)

    return []


# ── Legend box ─────────────────────────────────────────────────────────────────
legend_text = (
    'J_pos = Red = matter = escaping Hawking particle\n'
    'J_neg = Blue = Λ dark energy = infalling particle\n'
    'Brim  = σ=½ = event horizon = fixed point of inversion\n'
    'Trunk = minimum-action path = physical trajectory (attractor)\n'
    'Branches = near-paths = Hawking soft hair = fractal fur'
)
fig.text(0.50, 0.005, legend_text,
          color='#445566', fontsize=5.8, ha='center', va='bottom',
          family='monospace')


# ── Build animation ────────────────────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig, update,
    frames=N_FRAMES,
    init_func=init,
    interval=33,
    blit=False,
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_GIF = os.path.join(OUT_DIR, 'witches_hat_triptych.gif')

print(f'Rendering {N_FRAMES} frames...')
writer = animation.PillowWriter(fps=30)
ani.save(OUT_GIF, writer=writer, dpi=100)
print(f'Saved → {OUT_GIF}')

# Also save a static preview at t=0.50 (the firing moment)
update(N_FRAMES // 2)
PREVIEW = os.path.join(OUT_DIR, 'witches_hat_triptych_firing.png')
fig.savefig(PREVIEW, dpi=120, facecolor=BG)
print(f'Preview → {PREVIEW}')
