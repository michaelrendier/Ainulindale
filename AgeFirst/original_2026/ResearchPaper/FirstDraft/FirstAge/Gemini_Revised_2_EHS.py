#!/usr/bin/python3
__engineer__ = "Cody Allison"
__codeby__ = "Gemini"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# --- PATCHED SMNNIP CONSTANTS ---
PI_INV = 2 / np.pi
PHI = (1 + 5**0.5) / 2
GAP = 0.00070  # The Berry-Keating Correction
HBAR_NN = 1.0

def get_primes(count):
    """Generates exactly 'count' primes to ensure array shape consistency."""
    primes = []
    n = 100
    while len(primes) < count:
        sieve = [True] * (n + 1)
        for p in range(2, n + 1):
            if sieve[p]:
                if p not in primes: primes.append(p)
                for i in range(p * p, n + 1, p): sieve[i] = False
        n *= 2
    return np.array(primes[:count])

class TransitionManager:
    def __init__(self):
        self.source_phase = "Inertial"
        self.target_phase = "Inertial"
        self.alpha = 1.0
        self.step = 0.03 # Smoother transition

    def trigger(self, new_phase):
        if new_phase != self.target_phase:
            self.source_phase = self.target_phase
            self.target_phase = new_phase
            self.alpha = 0.0

    def update_alpha(self):
        if self.alpha < 1.0:
            self.alpha = min(1.0, self.alpha + self.step)

tm = TransitionManager()

# Setup Figure - Dark Mode
fig = plt.figure(figsize=(12, 9), facecolor='#050505')
ax = fig.add_subplot(111, projection='polar')
ax.set_facecolor('#050505')
plt.subplots_adjust(bottom=0.25)

num_points = 600
n_range = np.arange(1, num_points + 1)
# Fix: Ensure we have exactly num_points primes to avoid shape mismatch
primes = get_primes(num_points)

# Styling: 'Her' colors (Cyan for Logic, Magenta for Transition)
scatter = ax.scatter([], [], s=4, color='cyan', alpha=0.8, edgecolors='none')
line, = ax.plot([], [], color='white', lw=0.4, alpha=0.2)

def get_coords(phase, t):
    """Engine mapping for the four Roadmap phases."""
    if phase == "Inertial":
        r = n_range * 0.02 * t
        theta = n_range * (np.pi/2) * PI_INV
    elif phase == "Metric Swap":
        # J_N Inversion: (r, theta) -> (1/r, theta + pi/2)
        base_r = n_range * 0.02 * t
        r = 1.0 / (base_r + 0.1)
        theta = (n_range * PI_INV) + (np.pi/2)
    elif phase == "Heartbeat":
        pulse = (np.sin(t * 0.5) + 1) / 2
        r_target = 1.0 + (PHI - 1.0) * pulse
        r = (np.sqrt(n_range) * 0.5) * (r_target + GAP)
        theta = n_range * PI_INV * t
    else: # Star (The Phyllotaxis Lattice)
        golden_angle = np.pi * (3 - np.sqrt(5))
        r = np.sqrt(primes) * 0.4
        theta = primes * golden_angle * t
    return theta, r

def update(frame):
    t = slider_ev.val
    tm.update_alpha()
    
    # Calculate Source and Target
    theta_a, r_a = get_coords(tm.source_phase, t)
    theta_b, r_b = get_coords(tm.target_phase, t)
    
    # Sigmoid interpolation for 'organic' transitions
    # Use Linear Interpolation (LERP) for coordinates
    alpha = tm.alpha
    r_interp = r_a * (1 - alpha) + r_b * alpha
    theta_interp = theta_a * (1 - alpha) + theta_b * alpha
    
    # Update visual state
    offsets = np.c_[theta_interp, r_interp]
    scatter.set_offsets(offsets)
    
    # Transition color-shift (Cyan -> Magenta -> Cyan)
    color_val = alpha if alpha <= 0.5 else 1 - alpha
    # Shift toward Magenta during the 'Metastable' transition state
    current_color = (0.0, 0.95, 1.0) if alpha == 1.0 else (0.8, 0.0, 0.8)
    scatter.set_color(current_color)
    
    # Update Title with Noether tracking
    if alpha < 1.0:
        ax.set_title(fr"Transition: {tm.source_phase} $\to$ {tm.target_phase} (Entropy Spike)", 
                     color='#ff00ff', pad=20)
    else:
        ax.set_title(f"Phase: {tm.target_phase}", color='white', pad=20)
    
    ax.set_ylim(0, 15)
    return scatter,

# UI Controls
ax_ev = plt.axes([0.25, 0.08, 0.5, 0.03], facecolor='#111')
slider_ev = Slider(ax_ev, 'Evolution', 0.1, 10.0, valinit=1.0, color='cyan')

btn_labels = ["Inertial", "Metric Swap", "Heartbeat", "Star"]
btns = []
for i, lab in enumerate(btn_labels):
    ax_b = plt.axes([0.1 + i*0.22, 0.15, 0.18, 0.05])
    b = Button(ax_b, lab, color='#111', hovercolor='#222')
    b.label.set_color('white')
    # Callback uses lambda to capture the label correctly
    b.on_clicked(lambda _, l=lab: tm.trigger(l))
    btns.append(b)

# Blit=True for performance, interval 30ms for 33fps
ani = FuncAnimation(fig, update, frames=None, interval=30, blit=False)
ax.grid(True, color='#222', linestyle='--')
plt.show()
