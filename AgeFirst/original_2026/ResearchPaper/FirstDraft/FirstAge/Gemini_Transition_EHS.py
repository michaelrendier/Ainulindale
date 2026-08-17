import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- SMNNIP BOUNDARY CONSTANTS ---
PI_INV = 2 / np.pi
PHI = (1 + 5**0.5) / 2
GAP = 0.00070  # The Berry-Keating Open Flag
HBAR_NN = 1.0  # Governing the crossing step

# Fix: Initialize the figure and axes properly to avoid auto-removal warnings
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='#050505', 
                               subplot_kw={'projection': None})

# Re-assign ax1 as a polar plot correctly
ax1.remove()
ax1 = fig.add_subplot(121, projection='polar')
ax1.set_facecolor('#050505')
ax1.set_ylim(0.5, 1.5) 

ax2.set_facecolor('#050505')
# Fix: Use raw strings (r"") for LaTeX to avoid SyntaxWarnings
ax2.set_title(r"Noether Current Violation ($\partial_\mu J^\mu$)", color='white')
ax2.tick_params(colors='white')

# Generate sample points crossing the boundary
t_vals = np.linspace(1.5, 0.5, 200) 
theta_vals = t_vals * PI_INV * np.pi

# Plotting elements
trace, = ax1.plot([], [], 'cyan', lw=1, alpha=0.8, label='Inertial Path')
inv_trace, = ax1.plot([], [], '#ff00ff', lw=2, alpha=0.9, label='Inverted Path')
horizon = ax1.axhline(1.0, color='white', ls='--', alpha=0.3)
violation_line, = ax2.plot([], [], color='red', lw=1.5)

def update_sim(h_val):
    step = (np.pi / 2) * h_val
    
    mask_outer = t_vals >= 1.0
    mask_inner = t_vals < 1.0
    
    trace.set_data(theta_vals[mask_outer], t_vals[mask_outer])
    
    r_inv = 1.0 / t_vals[mask_inner]
    r_inv_corrected = r_inv * (1.0 + GAP)
    theta_inv = theta_vals[mask_inner] + step
    inv_trace.set_data(theta_inv, r_inv_corrected)
    
    v_data = np.zeros_like(t_vals)
    crossing_idx = np.argmin(np.abs(t_vals - 1.0))
    v_data[crossing_idx] = h_val * 1.5 
    violation_line.set_data(np.arange(len(t_vals)), v_data)
    ax2.set_ylim(-0.1, 2.5)
    
    fig.canvas.draw_idle()

plt.subplots_adjust(bottom=0.2)
ax_h = plt.axes([0.25, 0.05, 0.5, 0.03], facecolor='#222')
# Fix: Raw string for hbar_NN
h_slider = Slider(ax_h, r'$\hbar_{NN}$', 0.5, 2.0, valinit=1.0)
h_slider.on_changed(update_sim)

update_sim(1.0)
ax1.legend(loc='upper right', fontsize='small')
plt.show()
