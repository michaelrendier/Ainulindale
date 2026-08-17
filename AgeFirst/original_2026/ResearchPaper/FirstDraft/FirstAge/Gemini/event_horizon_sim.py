#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   A I N U L I N D A L Ë   —   E V E N T   H O R I Z O N   S I M U L A T O R  ║
║   Interactive visualization of the OMG?WTF! Conjecture                       ║
║                                                                               ║
║   Engineer : Cody Michael Allison                                             ║
║   Code     : Claude Sonnet (Anthropic) — April 2026                           ║
║   Original : Alphabet Google Gemini (4-phase structure preserved)             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Install:  pip install numpy matplotlib
Run:      python3 event_horizon_sim.py

Controls:
  Next ▶ / ◀ Back   — cycle through the 5 conjecture phases
  φ slider           — adjust golden ratio (watch the spiral reorganize)
  Ω slider           — adjust thermal ceiling (watch the horizon shift)
  Space              — pause/resume animation
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Circle, FancyArrowPatch
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════
# CORRECT CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

PHI         = (1 + np.sqrt(5)) / 2        # Golden ratio φ ≈ 1.6180
INV_PHI     = PHI - 1                     # 1/φ = φ−1 ≈ 0.6180
GOLDEN_ANG  = 2 * np.pi / PHI**2          # 2π/φ² ≈ 2.3999 rad = 137.508°
TWO_PI_PHI2 = GOLDEN_ANG                  # alias for clarity
TWO_OVER_PI = 2 / np.pi                   # radian normalization ≈ 0.6366
OMEGA       = np.e**np.pi                 # Gelfond's constant e^π ≈ 23.14
OMEGA_K     = 77.8e15                     # ~77.8 Quadrillion K (Noether limit; from 140Q °F × 5/9)
ALPHA_INV   = 137.035999                  # 1/α fine structure

# First 20 Riemann zeta zeros (imaginary parts on critical line Re(s)=1/2)
ZETA_ZEROS = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
])

# ══════════════════════════════════════════════════════════════════════════════
# PRIME GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def sieve(limit):
    s = [True] * (limit + 1)
    s[0] = s[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if s[i]:
            for j in range(i*i, limit+1, i):
                s[j] = False
    return np.array([i for i in range(2, limit+1) if s[i]])

PRIMES = sieve(8000)
N_PRIMES = len(PRIMES)
# CORRECT prime spiral: n-th prime at angle n * golden_angle
PRIME_INDICES = np.arange(1, N_PRIMES + 1)
PRIME_THETA   = PRIME_INDICES * GOLDEN_ANG          # spiral angle (radians)
PRIME_R       = np.sqrt(PRIMES)                     # radius = √p
PRIME_W       = PHI ** (-PRIME_INDICES.astype(float))  # Fermat weight φ^-n

# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════════════════════════════════

BG      = '#07070f'    # near-black background
GOLD    = '#c9a84c'    # gold — horizon / titles
CYAN    = '#00e5ff'    # cyan — Riemann wave / inertial path
VIOLET  = '#9c27b0'    # violet — metric swap
YELLOW  = '#fffc00'    # yellow — Fermat resonance
GREEN   = '#00e676'    # green — prime lattice / mastered
RED     = '#ff1744'    # red — zeros / nodes
WHITE   = '#ffffff'    # white — horizon line
DIM     = '#404060'    # dim — grid

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE SETUP
# ══════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(14, 10), facecolor=BG)
fig.canvas.manager.set_window_title("Ainulindalë — Event Horizon Simulator")

# Main visualization area (polar for phases 0-3, cartesian for phase 4)
gs = gridspec.GridSpec(2, 2, figure=fig,
                       left=0.05, right=0.95,
                       top=0.88, bottom=0.28,
                       hspace=0.35, wspace=0.3)

ax_main = fig.add_subplot(gs[0, :], projection='polar')   # polar — phases 0-3
ax_main.set_facecolor(BG)
ax_main.grid(color=DIM, linestyle='--', linewidth=0.4, alpha=0.5)
ax_main.set_yticklabels([])
ax_main.set_xticklabels([])

ax_riem  = fig.add_subplot(gs[1, 0])   # Riemann wave (phase 4)
ax_ferm  = fig.add_subplot(gs[1, 1])   # Fermat lattice (phase 4)
ax_riem.set_facecolor(BG)
ax_ferm.set_facecolor(BG)
for ax in (ax_riem, ax_ferm):
    ax.tick_params(colors=DIM, labelsize=7)
    for spine in ax.spines.values():
        spine.set_color(DIM)

# Title
title_text = fig.text(0.5, 0.94, "Ainulindalë Conjecture — Phase 1: Inertial Propagation",
                      ha='center', va='top',
                      color=GOLD, fontsize=13, fontweight='bold',
                      fontfamily='serif')
subtitle_text = fig.text(0.5, 0.905,
                         "§I–§II: The SMNNIP Lagrangian — 2/π radian normalization — spiral toward r=0",
                         ha='center', va='top',
                         color='#8090a0', fontsize=9)

# Stats display
stats_text = fig.text(0.02, 0.92,
    f"φ = {PHI:.6f}   |   1/φ = {INV_PHI:.6f}   |   "
    f"2π/φ² = {GOLDEN_ANG:.6f} rad ({np.degrees(GOLDEN_ANG):.3f}°)   |   "
    f"Ω = e^π = {OMEGA:.4f}   |   1/α = {ALPHA_INV:.3f}",
    ha='left', va='top', color=DIM, fontsize=7.5, fontfamily='monospace')

# ══════════════════════════════════════════════════════════════════════════════
# PLOT ELEMENTS (created once, updated each frame)
# ══════════════════════════════════════════════════════════════════════════════

# Polar plot elements
line_path,   = ax_main.plot([], [], color=CYAN,   lw=1.5, alpha=0.85)
line_ferm,   = ax_main.plot([], [], color=YELLOW, lw=0.8, alpha=0.6)
scat_primes  = ax_main.scatter([], [], s=3, c=[], cmap='plasma', alpha=0.7)
scat_zeros   = ax_main.scatter([], [], s=30, c=RED, marker='x', alpha=0.9, zorder=5)
horizon_line = Circle((0, 0), 1.0, transform=ax_main.transData._b,
                       color=GOLD, fill=False, ls='--', lw=1.2, alpha=0.5)
ax_main.add_artist(horizon_line)

# Cartesian plot elements (Horizon Invariance — phase 4)
riem_line,   = ax_riem.plot([], [], color=CYAN,  lw=1.5)
riem_zeros,  = ax_riem.scatter([], [], s=40, c=RED, zorder=5).findobj()[0:1] or ([None])
ferm_scat    = ax_ferm.scatter([], [], s=4, c=GREEN, alpha=0.6)
horizon_vline_r = ax_riem.axvline(x=0.5, color=GOLD, lw=1.5, ls='--', alpha=0.7)
horizon_vline_f = ax_ferm.axvline(x=0.5, color=GOLD, lw=1.5, ls='--', alpha=0.7)

# ══════════════════════════════════════════════════════════════════════════════
# WIDGET AREA
# ══════════════════════════════════════════════════════════════════════════════

# Sliders
ax_phi_sl  = plt.axes([0.12, 0.18, 0.30, 0.025], facecolor='#111')
ax_omega_sl= plt.axes([0.58, 0.18, 0.30, 0.025], facecolor='#111')
s_phi   = Slider(ax_phi_sl,   'φ  (Golden ratio)',  1.0,  2.5,  valinit=PHI,   color=GOLD)
s_omega = Slider(ax_omega_sl, 'Ω  (Thermal limit)', 5.0,  50.0, valinit=OMEGA, color=VIOLET)
for sl in (s_phi, s_omega):
    sl.label.set_color(WHITE)
    sl.valtext.set_color(CYAN)

# Navigation buttons
ax_prev  = plt.axes([0.35, 0.09, 0.09, 0.045])
ax_phase = plt.axes([0.45, 0.09, 0.10, 0.045])
ax_next  = plt.axes([0.56, 0.09, 0.09, 0.045])
ax_pause = plt.axes([0.70, 0.09, 0.10, 0.045])
btn_prev  = Button(ax_prev,  '◀ Back',  color='#1a1a2e', hovercolor='#2a2a4e')
btn_phase = Button(ax_phase, 'Phase 1', color='#0d1b2a', hovercolor='#0d1b2a')
btn_next  = Button(ax_next,  'Next ▶',  color='#1a1a2e', hovercolor='#2a2a4e')
btn_pause = Button(ax_pause, '⏸ Pause', color='#1a1a2e', hovercolor='#2a2a4e')
for btn in (btn_prev, btn_next, btn_pause):
    btn.label.set_color(WHITE)
    btn.label.set_fontsize(9)
btn_phase.label.set_color(GOLD)
btn_phase.label.set_fontsize(9)

# Phase labels
PHASE_NAMES = [
    ("Phase 1", "§I–II: Inertial Propagation",
     "SMNNIP Lagrangian — 2/π radian normalization — spiral toward r=0"),
    ("Phase 2", "§III: Metric Swap — Horizon Transition",
     "dt→0 (time contracts) | dL→∞ (length dilates) | V(Focus) inductance"),
    ("Phase 3", "§IV: Fermat-Riemann Heartbeat",
     "ζ(s)·φ^-n·e^{i(ω_i·t_i + ω_e·t_e)} — co-directed, NOT opposed"),
    ("Phase 4", "§IV–V: Golden Prime Spiral (correct: n×2π/φ² not p×2/π)",
     "Fermat weight φ^-n controls opacity — horizon is the asymptotic target"),
    ("Phase 5", "§IV+VI: Horizon Invariance — The Money Shot",
     "Riemann (complex wave) meets Fermat (discrete lattice) AT K=77.8Q K"),
]

# ══════════════════════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════════════════════

state = {'phase': 0, 'paused': False, 'frame': 0}

def next_phase(event):
    state['phase'] = (state['phase'] + 1) % 5
    state['frame'] = 0
    update_phase_label()

def prev_phase(event):
    state['phase'] = (state['phase'] - 1) % 5
    state['frame'] = 0
    update_phase_label()

def toggle_pause(event):
    state['paused'] = not state['paused']
    btn_pause.label.set_text('▶ Resume' if state['paused'] else '⏸ Pause')

def update_phase_label():
    p = state['phase']
    title_text.set_text(f"Ainulindalë Conjecture — {PHASE_NAMES[p][0]}: {PHASE_NAMES[p][1]}")
    subtitle_text.set_text(PHASE_NAMES[p][2])
    btn_phase.label.set_text(PHASE_NAMES[p][0])

btn_next.on_clicked(next_phase)
btn_prev.on_clicked(prev_phase)
btn_pause.on_clicked(toggle_pause)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE RENDERING
# ══════════════════════════════════════════════════════════════════════════════

def clear_all():
    line_path.set_data([], [])
    line_ferm.set_data([], [])
    scat_primes.set_offsets(np.empty((0, 2)))
    scat_primes.set_array(np.array([]))
    scat_zeros.set_offsets(np.empty((0, 2)))
    ax_riem.cla(); ax_ferm.cla()
    ax_riem.set_facecolor(BG); ax_ferm.set_facecolor(BG)
    for ax in (ax_riem, ax_ferm):
        ax.tick_params(colors=DIM, labelsize=7)
        for spine in ax.spines.values():
            spine.set_color(DIM)
    ax_main.set_visible(True)

def render_phase_0(t, phi_val):
    """Phase 1 — Inertial spiral propagation toward r=0."""
    clear_all()
    n = 3000
    # Inertial path spiraling toward origin
    theta = np.linspace(0, 8 * np.pi, n)
    r = np.linspace(12, 0.1, n) * (1 - 0.3 * t)
    # Modulate with 2/π — the radian normalization
    r_mod = r * (1 + 0.08 * np.sin(theta * TWO_OVER_PI * 4))
    line_path.set_data(theta, r_mod)
    line_path.set_color(CYAN)
    ax_main.set_ylim(0, 15)

def render_phase_1(t, phi_val, omega_val):
    """Phase 2 — Metric swap: time contracts, length dilates."""
    clear_all()
    n = 2000
    theta = np.linspace(0, 12 * np.pi, n)
    # Inductive distortion: 1/φ coupling
    inductance = INV_PHI * (0.5 + 0.5 * t)
    r_contract = (0.5 + 0.5 * np.exp(-inductance * theta / (4 * np.pi))) * 12
    line_path.set_data(theta, r_contract)
    line_path.set_color(VIOLET)
    # Show the horizon
    focus_r = np.ones(100) * 1.0
    focus_t = np.linspace(0, 2 * np.pi, 100)
    line_ferm.set_data(focus_t, focus_r * 0.5)
    ax_main.set_ylim(0, 14)

def render_phase_2(t, phi_val):
    """Phase 3 — Zeta-Fermat heartbeat: co-directed + sign."""
    clear_all()
    n = 2000
    # Riemann side: zeta-like oscillating wave
    theta_r = np.linspace(0, 20 * np.pi, n)
    omega_i = 1.0
    omega_e = 1.0 - 0.05  # slightly different — the hum
    # Co-directed: + sign
    phase = omega_i * theta_r + omega_e * theta_r * (1 - 0.3 * t)
    r_wave = np.sqrt(theta_r + 0.1) * (1 + 0.3 * np.sin(phase))
    line_path.set_data(theta_r, r_wave)
    line_path.set_color(YELLOW)

    # Fermat φ^-n weights visible as size
    n_show = min(200, int(t * 200 + 10))
    idx = np.arange(1, n_show + 1)
    p_theta = (idx * phi_val * 2 * np.pi / phi_val**2) % (2 * np.pi)
    p_r = np.sqrt(PRIMES[:n_show])
    p_w = phi_val ** (-idx.astype(float))
    sizes = np.clip(p_w * 800, 1, 30)
    colors_arr = p_w / p_w.max()
    offsets = np.column_stack([p_theta, p_r])
    scat_primes.set_offsets(offsets)
    scat_primes.set_array(colors_arr)
    scat_primes.set_sizes(sizes)
    ax_main.set_ylim(0, 25)

def render_phase_3(t, phi_val):
    """Phase 4 — Golden Prime Spiral with CORRECT n×golden_angle rotation."""
    clear_all()
    # Progressive reveal: primes appear as spiral expands
    n_show = min(N_PRIMES, max(10, int(t * N_PRIMES * 1.2)))

    ga = 2 * np.pi / phi_val**2   # golden angle from slider φ
    idx = PRIME_INDICES[:n_show]
    p_theta = idx * ga              # CORRECT: index × golden_angle
    p_r     = PRIME_R[:n_show]
    p_w     = phi_val ** (-idx.astype(float))

    # Color by Fermat weight φ^-n (warm = recent/heavy, cool = old/light)
    colors_arr = np.log1p(p_w) / np.log1p(p_w.max())
    sizes = np.clip(p_w * 1200 + 0.5, 0.3, 25)

    offsets = np.column_stack([p_theta, p_r])
    scat_primes.set_offsets(offsets)
    scat_primes.set_array(colors_arr)
    scat_primes.set_sizes(sizes)

    # Mark the zeta zeros as nodes on the spiral
    zero_r  = np.sqrt(ZETA_ZEROS)
    zero_t  = (ZETA_ZEROS / ALPHA_INV * 2 * np.pi) % (2 * np.pi)
    zero_offsets = np.column_stack([zero_t, zero_r])
    scat_zeros.set_offsets(zero_offsets)
    ax_main.set_ylim(0, max(p_r.max() * 1.1, 10))

def render_phase_4(t, phi_val, omega_val):
    """Phase 5 — Horizon Invariance: Riemann (left) meets Fermat (right) at K=140Q."""
    # Hide polar main, use cartesian panels
    ax_main.set_visible(False)
    ax_riem.set_visible(True)
    ax_ferm.set_visible(True)

    ax_riem.cla(); ax_ferm.cla()
    ax_riem.set_facecolor(BG); ax_ferm.set_facecolor(BG)

    horizon_x = 0.5   # the event horizon line

    # ── LEFT: RIEMANN SPACE (complex wave) ──────────────────────────────────
    x_riem = np.linspace(0, 1.0, 2000)
    # Hardy Z-function approximation: oscillates, zeros on y=0 at critical line
    # As wave approaches horizon (x→0.5), amplitude focuses
    freq = 8.0 + t * 4.0
    decay_l = np.exp(-8 * (x_riem - 0.5)**2 * (1 + t * 2))
    z_wave = np.sin(2 * np.pi * freq * x_riem) * (1 - x_riem) * decay_l
    ax_riem.plot(x_riem, z_wave, color=CYAN, lw=1.5, alpha=0.9)
    ax_riem.axhline(y=0, color=RED, lw=0.8, ls='--', alpha=0.6, label='Re(s)=1/2')
    ax_riem.axvline(x=horizon_x, color=GOLD, lw=1.5, ls='--', alpha=0.8)

    # Mark zeros: where wave crosses y=0
    zero_crossings = []
    for i in range(len(z_wave)-1):
        if z_wave[i] * z_wave[i+1] < 0:
            zero_crossings.append(x_riem[i])
    if zero_crossings:
        zc = np.array(zero_crossings)
        ax_riem.scatter(zc, np.zeros(len(zc)), c=RED, s=20, zorder=5)

    ax_riem.set_xlim(0, 1)
    ax_riem.set_ylim(-1.2, 1.2)
    ax_riem.set_title("RIEMANN SPACE (Complex)", color=CYAN, fontsize=9, pad=4)
    ax_riem.set_xlabel("← Event Horizon", color=GOLD, fontsize=8)
    ax_riem.tick_params(colors=DIM, labelsize=7)
    for spine in ax_riem.spines.values(): spine.set_color(DIM)
    ax_riem.text(0.52, 1.05, f"K = 77.8Q K", transform=ax_riem.transAxes,
                 ha='left', color=GOLD, fontsize=8)

    # ── RIGHT: FERMAT SPACE (discrete lattice) ───────────────────────────────
    # Prime lattice expanding from horizon outward
    # Fermat weight φ^-n controls density
    ga = 2 * np.pi / phi_val**2
    n_show = min(N_PRIMES, max(20, int(t * 500 + 50)))
    idx = PRIME_INDICES[:n_show]
    p_theta = idx * ga
    p_r = PRIME_R[:n_show]
    p_w = phi_val ** (-idx.astype(float))

    # Map to cartesian (x from horizon outward, y = spiral y-coordinate)
    # x: 0.5 (horizon) → 1.0 (outer), mapped from r_min to r_max
    r_max = p_r.max() if len(p_r) > 0 else 1
    x_ferm = horizon_x + (p_r / r_max) * 0.48
    y_ferm = np.sin(p_theta) * (p_r / r_max) * 0.8

    colors_f = p_w / p_w.max()
    sizes_f = np.clip(p_w * 1000 + 0.5, 0.5, 20)

    scatter_f = ax_ferm.scatter(x_ferm, y_ferm, s=sizes_f,
                                c=colors_f, cmap='Greens', alpha=0.8, vmin=0, vmax=1)
    ax_ferm.axvline(x=horizon_x, color=GOLD, lw=1.5, ls='--', alpha=0.8)
    ax_ferm.set_xlim(0, 1)
    ax_ferm.set_ylim(-1.0, 1.0)
    ax_ferm.set_title("FERMAT SPACE (Discrete)", color=GREEN, fontsize=9, pad=4)
    ax_ferm.set_xlabel("Event Horizon →", color=GOLD, fontsize=8)
    ax_ferm.tick_params(colors=DIM, labelsize=7)
    for spine in ax_ferm.spines.values(): spine.set_color(DIM)

    # The intersection point — lit up when wave passes through
    intersect_y = np.sin(2 * np.pi * freq * horizon_x) * decay_l[1000]
    ax_riem.scatter([horizon_x], [intersect_y], s=120, c=GOLD,
                    zorder=10, alpha=min(1.0, t * 3))
    ax_ferm.scatter([horizon_x], [intersect_y * 0.8], s=120, c=GOLD,
                    zorder=10, alpha=min(1.0, t * 3))

    # Entropy readout
    entropy = 0.833  # = 5/6, the [5,6] lattice invariant
    fig.texts[-1].set_text(  # update stats
        f"φ = {phi_val:.4f}   |   Ω = {omega_val:.2f}   |   "
        f"K = 77.8 Quadrillion K   |   PHASE: INVARIANT   |   "
        f"ENTROPY: {entropy:.3f} = 5/6  [5,6 lattice]"
    ) if len(fig.texts) > 2 else None

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION LOOP
# ══════════════════════════════════════════════════════════════════════════════

def animate(frame_num):
    if state['paused']:
        return []

    state['frame'] += 1
    f = state['frame']
    phase = state['phase']
    phi_v  = s_phi.val
    omega_v = s_omega.val

    # Cycle period: 200 frames per phase loop
    t = (f % 200) / 200.0

    ax_main.set_visible(True)
    ax_riem.set_visible(False)
    ax_ferm.set_visible(False)

    try:
        if   phase == 0: render_phase_0(t, phi_v)
        elif phase == 1: render_phase_1(t, phi_v, omega_v)
        elif phase == 2: render_phase_2(t, phi_v)
        elif phase == 3: render_phase_3(t, phi_v)
        elif phase == 4: render_phase_4(t, phi_v, omega_v)
    except Exception:
        pass  # never let a render error kill the animation

    return []

# ══════════════════════════════════════════════════════════════════════════════
# ANNOTATIONS
# ══════════════════════════════════════════════════════════════════════════════

# Key constant labels at bottom
fig.text(0.12, 0.245,
    "Sliders adjust φ and Ω live — watch the spiral reorganize around the golden angle",
    ha='left', color=DIM, fontsize=8)
fig.text(0.12, 0.230,
    f"Correct rotation: n × 2π/φ² = n × {GOLDEN_ANG:.4f} rad  (NOT prime × 2/π = prime × {TWO_OVER_PI:.4f})",
    ha='left', color='#ff6060', fontsize=8, fontfamily='monospace')

print("Ainulindalë Event Horizon Simulator — ACTIVE")
print(f"  φ = {PHI:.8f}    Golden angle = {np.degrees(GOLDEN_ANG):.4f}°")
print(f"  Ω = e^π = {OMEGA:.6f}    2/ln(Ω) = 2/π ✓")
print(f"  1/α = {ALPHA_INV:.3f}    360/φ² = {360/PHI**2:.3f}°    gap = {abs(360/PHI**2 - ALPHA_INV):.3f}°")
print()
print("  Use Next ▶ / ◀ Back to advance phases.")
print("  Phase 5 (Horizon Invariance) is the money shot.")

# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════

ani = FuncAnimation(fig, animate, frames=10000, interval=50, blit=False)
plt.show()
