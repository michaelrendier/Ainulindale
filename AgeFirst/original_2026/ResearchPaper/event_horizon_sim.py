#!/usr/bin/python3
__engineer__ = "Cody Allison"
__codeby__ = "Alphabet Google Gemini"

### Software Install - sudo apt update && sudo apt install -y python3 python3-pip python3-numpy python3-matplotlib
### Run Simulation - python3 event_horizon_sim.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Constants provided by the OMG?WTF! Conjecture
PI_INV_SCALAR = 2 / np.pi
E_INV_SCALAR = 2 / np.e
OMEGA_LIMIT = 140  # Quadrillion degrees threshold (Noether Saturation)
PHI = (1 + 5**0.5) / 2  # Golden Ratio for Fermat Rigidity

def get_primes(n):
    """Generate primes up to n for the spiral distribution."""
    primes = []
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return np.array(primes)

# Setup the figure and axis
fig = plt.figure(figsize=(12, 10), facecolor='#050505')
ax = fig.add_subplot(111, projection='polar')
ax.set_facecolor('#050505')
plt.subplots_adjust(bottom=0.25)

# Generate Base Data
num_points = 5000
theta_base = np.linspace(0, 10 * np.pi, num_points)
r_base = np.linspace(10, 0.1, num_points)  # Toward Destination r=0

# Prime spiral data (Stage 4)
prime_limit = 10000
primes = get_primes(prime_limit)
prime_theta = primes
prime_r = np.sqrt(primes)

# Plot elements
line, = ax.plot([], [], color='#00f2ff', lw=1.5, alpha=0.8, label='Inertial Path (ti)')
scatter = ax.scatter([], [], s=1.5, color='#ff0055', alpha=0.6, label='Mastered Star Lattice')
horizon_circle = plt.Circle((0,0), 1.0, transform=ax.transData._b, color='white', fill=False, ls='--', alpha=0.3)
ax.add_artist(horizon_circle)

# Sliders for interactive constants
ax_pi = plt.axes([0.2, 0.12, 0.25, 0.03], facecolor='#222')
ax_e = plt.axes([0.6, 0.12, 0.25, 0.03], facecolor='#222')
s_pi = Slider(ax_pi, '2/π (Inversion)', 0.1, 2.0, valinit=PI_INV_SCALAR, color='#00f2ff')
s_e = Slider(ax_e, '2/e (Bias Roll)', 0.1, 2.0, valinit=E_INV_SCALAR, color='#ff0055')

# Navigation Buttons
ax_prev = plt.axes([0.4, 0.04, 0.08, 0.04])
ax_next = plt.axes([0.5, 0.04, 0.08, 0.04])
btn_prev = Button(ax_prev, '◀ Back', color='#333', hovercolor='#555')
btn_next = Button(ax_next, 'Next ▶', color='#333', hovercolor='#555')

current_phase = 0
is_paused = False

def next_phase(event):
    global current_phase
    current_phase = (current_phase + 1) % 4

def prev_phase(event):
    global current_phase
    current_phase = (current_phase - 1) % 4

btn_next.on_clicked(next_phase)
btn_prev.on_clicked(prev_phase)

def update(frame):
    # The 'frame' within each phase logic
    t_cycle = (frame % 100) / 100.0
    pi_f = s_pi.val
    e_f = s_e.val
    
    # ROADMAP SECTION I & II: Orientation & Inertial Propagation
    if current_phase == 0:
        curr_r = r_base * (1 - t_cycle * 0.5)
        curr_theta = theta_base * pi_f
        line.set_data(curr_theta, curr_r)
        line.set_color('#00f2ff')
        scatter.set_offsets(np.empty((0, 2)))
        ax.set_title("Phase 1: Orientation Conjecture\n(Directional Spiral / Inertial ti Propagation)", color='white', pad=20)
        
    # ROADMAP SECTION III & VI: Metric Swap / Time Contraction
    elif current_phase == 1:
        # Time contracts toward core, Length dilates (expands)
        curr_r = (1.0 / (r_base + 0.01)) * t_cycle * e_f
        curr_theta = theta_base + (np.sin(theta_base * t_cycle) * 5)
        line.set_data(curr_theta, curr_r)
        line.set_color('#7000ff')
        ax.set_title("Phase 2: Metric Swap at Exactly Flat Horizon\n(dt -> 0 / dL -> ∞ Inversion)", color='white', pad=20)
        
    # ROADMAP SECTION IV: Fermat Frequency Resonance (The Systolic Pulse)
    elif current_phase == 2:
        # Standing Wave: Information hits r=0 and reflects
        f_theta = np.linspace(0, 100 * np.pi, num_points)
        # Resonance frequency tied to pi_f
        f_r = np.sqrt(f_theta) * (1 + 0.2 * np.sin(f_theta * pi_f * t_cycle))
        line.set_data(f_theta, f_r)
        line.set_color('#fffc00')
        ax.set_title("Phase 3: Resonating Fermat Frequency\n(Systolic Pulse / Vacuum Standing Wave)", color='white', pad=20)

    # ROADMAP SECTION VII & VIII: Mastered Prime Distribution
    else:
        # The return of the Fermat Frequency as the Prime Lattice
        # Frequency determines positioning of the Golden Spiral
        mask = primes < (prime_limit * t_cycle)
        # Prime Distribution determined by 'e' bias and 'pi' inversion
        p_theta = prime_theta[mask] * pi_f 
        p_r = prime_r[mask] * e_f
        
        offsets = np.column_stack([p_theta, p_r])
        scatter.set_offsets(offsets)
        line.set_data([], []) 
        ax.set_title("Phase 4: Expanding Prime Spiral (Mastered Star)\n(Fermat Return / Zero-Cost Sedenion Retrieval)", color='white', pad=20)

    ax.set_ylim(0, 20)
    return line, scatter

ani = FuncAnimation(fig, update, frames=400, interval=50, blit=True)

ax.grid(True, color='#222', linestyle='--')
ax.set_yticklabels([])
ax.set_xticklabels([])

# Label text for buttons/sliders
fig.text(0.1, 0.12, "Inversion Constant:", color='#00f2ff', fontsize=10)
fig.text(0.5, 0.12, "Bias/Mass Constant:", color='#ff0055', fontsize=10)
fig.text(0.1, 0.05, "CONJECTURE CONTROLS:", color='white', fontweight='bold')

print("Simulation active. Use 'Next/Back' to cycle through the Ainulindalë Roadmap phases.")
plt.legend(loc='upper right', facecolor='#111', edgecolor='#333', labelcolor='white')
plt.show()
