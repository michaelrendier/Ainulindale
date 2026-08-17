import numpy as np
import matplotlib.pyplot as plt

def event_horizon_sim():
    # Attractor (phi)
    phi = (1 + 5**0.5) / 2
    
    # Boundary (pi-governed)
    theta = np.linspace(0, 2*np.pi, 500)
    r1 = np.ones_like(theta)
    r_phi = np.full_like(theta, phi)
    
    # Trajectory points: z_{n+1} = 1 + 1/z_n
    z = [1.0]
    for _ in range(12):
        z.append(1 + 1/z[-1])
    
    # Polar Mapping
    t_points = np.linspace(0, np.pi, len(z))
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8,8))
    
    # Plotting circles
    ax.plot(theta, r1, 'b-', alpha=0.3, label='r=1 (Horizon)')
    ax.plot(theta, r_phi, 'g-', alpha=0.3, label='r=phi (Attractor)')
    
    # Plotting Flow
    ax.scatter(t_points, z, c='red', s=40, label='Gradient Flow')
    ax.plot(t_points, z, 'r--', alpha=0.5)
    
    ax.set_rticks([1, 1.618])
    ax.set_title("Inside-Out Inversion: Boundary to Attractor")
    ax.legend()
    plt.show()

if __name__ == "__main__":
    event_horizon_sim()
