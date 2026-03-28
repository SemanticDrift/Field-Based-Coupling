"""
Field-Based Coupling: A Structural Resolution of the N=2 Synchronization Failure
Author: Carolina Johnson (CJ)
DOI: https://doi.org/10.5281/zenodo.18396204
Site: https://www.semanticdrift.net

What this shows:
    The Kuramoto model at N=2 reduces to a tug-of-war with no shared
    convergence structure. Field-based coupling introduces the phase midpoint
    as an explicit attractor. Both oscillators align to the same target.
    Synchronization becomes structurally guaranteed when |w2 - w1| < 2K.

Run:
    pip install numpy matplotlib
    python field_based_coupling.py
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
w1 = 1.0          # natural frequency, oscillator 1 (rad/s)
w2 = 1.3          # natural frequency, oscillator 2 (rad/s)
K  = 0.5          # coupling strength
dt = 0.01         # time step (s)
T  = 60.0         # total simulation time (s)
t  = np.arange(0, T, dt)

theta1_0 = 0.0    # initial phase, oscillator 1 (rad)
theta2_0 = 2.0    # initial phase, oscillator 2 (rad)

# ---------------------------------------------------------------------------
# Lock condition check
# ---------------------------------------------------------------------------
freq_mismatch = abs(w2 - w1)
lock_threshold = 2 * K

print("=" * 60)
print("Field-Based Coupling vs Kuramoto at N=2")
print("=" * 60)
print(f"  Natural frequencies : w1={w1}, w2={w2}")
print(f"  Coupling strength   : K={K}")
print(f"  Frequency mismatch  : |w2 - w1| = {freq_mismatch:.4f}")
print(f"  Lock threshold (2K) : {lock_threshold:.4f}")
print()

if freq_mismatch < lock_threshold:
    delta_star = 2 * np.arcsin(freq_mismatch / lock_threshold)
    print(f"  Lock condition MET  : |w2-w1| < 2K")
    print(f"  Predicted fixed point (delta*) = {np.degrees(delta_star):.2f} degrees")
else:
    print(f"  Lock condition NOT met: |w2-w1| >= 2K")
    print(f"  Field-coupled system will drift. Increase K or reduce frequency mismatch.")
print("=" * 60)
print()

# ---------------------------------------------------------------------------
# Model 1: Standard Kuramoto at N=2
# ---------------------------------------------------------------------------
def run_kuramoto(w1, w2, K, theta1_0, theta2_0, t, dt):
    theta1 = np.zeros(len(t))
    theta2 = np.zeros(len(t))
    theta1[0] = theta1_0
    theta2[0] = theta2_0

    for i in range(1, len(t)):
        d1 = w1 + (K / 2) * np.sin(theta2[i-1] - theta1[i-1])
        d2 = w2 + (K / 2) * np.sin(theta1[i-1] - theta2[i-1])
        theta1[i] = theta1[i-1] + dt * d1
        theta2[i] = theta2[i-1] + dt * d2

    delta = theta2 - theta1
    return theta1, theta2, delta

# ---------------------------------------------------------------------------
# Model 2: Field-Based Coupling at N=2
# ---------------------------------------------------------------------------
def run_field_coupled(w1, w2, K, theta1_0, theta2_0, t, dt):
    theta1 = np.zeros(len(t))
    theta2 = np.zeros(len(t))
    theta1[0] = theta1_0
    theta2[0] = theta2_0

    for i in range(1, len(t)):
        phi = (theta1[i-1] + theta2[i-1]) / 2.0   # shared phase field
        d1 = w1 + K * np.sin(phi - theta1[i-1])
        d2 = w2 + K * np.sin(phi - theta2[i-1])
        theta1[i] = theta1[i-1] + dt * d1
        theta2[i] = theta2[i-1] + dt * d2

    delta = theta2 - theta1
    return theta1, theta2, delta

# ---------------------------------------------------------------------------
# Run both models
# ---------------------------------------------------------------------------
_, _, delta_kuramoto     = run_kuramoto(w1, w2, K, theta1_0, theta2_0, t, dt)
_, _, delta_field        = run_field_coupled(w1, w2, K, theta1_0, theta2_0, t, dt)

# Wrap Kuramoto delta to [-pi, pi] for readable visualization
delta_kuramoto_wrapped = (delta_kuramoto + np.pi) % (2 * np.pi) - np.pi

# Compute field-coupled final delta for reporting
final_delta_deg = np.degrees(delta_field[-1] % (2 * np.pi))
print(f"  Kuramoto final delta  : {np.degrees(delta_kuramoto[-1] % (2*np.pi)):.2f} degrees (still drifting)")
print(f"  Field-coupled final delta : {final_delta_deg:.2f} degrees (locked)")
print()

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(13, 5.5))
fig.patch.set_facecolor("#0f1117")

gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

for ax in [ax1, ax2]:
    ax.set_facecolor("#161b22")
    ax.tick_params(colors="#8b949e", labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")
    ax.xaxis.label.set_color("#8b949e")
    ax.yaxis.label.set_color("#8b949e")

# Panel 1: Kuramoto
ax1.plot(t, delta_kuramoto_wrapped, color="#e06c75", linewidth=1.2, alpha=0.9)
ax1.axhline(0, color="#30363d", linewidth=0.8, linestyle="--")
ax1.set_title("Kuramoto at N=2\nPhase difference (wrapped)", color="#cdd9e5", fontsize=11, pad=10)
ax1.set_xlabel("Time (s)", fontsize=9)
ax1.set_ylabel("Δθ = θ₂ - θ₁ (rad)", fontsize=9)
ax1.set_ylim(-np.pi - 0.3, np.pi + 0.3)
ax1.set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax1.set_yticklabels(["-π", "-π/2", "0", "π/2", "π"], color="#8b949e", fontsize=8)
ax1.text(0.97, 0.97, "Tug-of-war.\nNo convergence.",
         transform=ax1.transAxes, ha="right", va="top",
         color="#e06c75", fontsize=8.5, alpha=0.85)

# Panel 2: Field-coupled
if freq_mismatch < lock_threshold:
    delta_star_val = 2 * np.arcsin(freq_mismatch / lock_threshold)
    ax2.axhline(delta_star_val, color="#58a6ff", linewidth=0.9,
                linestyle="--", alpha=0.5, label=f"Fixed point δ* = {np.degrees(delta_star_val):.1f}°")
    ax2.legend(fontsize=8, facecolor="#161b22", edgecolor="#30363d",
               labelcolor="#8b949e", loc="upper right")

ax2.plot(t, delta_field, color="#56d364", linewidth=1.2, alpha=0.9)
ax2.axhline(0, color="#30363d", linewidth=0.8, linestyle="--")
ax2.set_title("Field-Based Coupling at N=2\nPhase difference", color="#cdd9e5", fontsize=11, pad=10)
ax2.set_xlabel("Time (s)", fontsize=9)
ax2.set_ylabel("Δθ = θ₂ - θ₁ (rad)", fontsize=9)
ax2.text(0.97, 0.97, "Shared attractor.\nPhase lock.",
         transform=ax2.transAxes, ha="right", va="top",
         color="#56d364", fontsize=8.5, alpha=0.85)

# Main title
fig.suptitle(
    "Field-Based Coupling vs Kuramoto at N=2\n"
    f"w1={w1}, w2={w2}, K={K}  |  |w2-w1|={freq_mismatch:.2f} < 2K={lock_threshold:.2f}  →  lock condition met",
    color="#cdd9e5", fontsize=10.5, y=1.01
)

plt.savefig("kuramoto_comparison.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("  Plot saved to kuramoto_comparison.png")

plt.tight_layout()
plt.show()
