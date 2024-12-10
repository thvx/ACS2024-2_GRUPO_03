import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

class PendulumSystem:
    def __init__(self, M, m, l, g=9.8):
        self.M = M
        self.m = m
        self.l = l
        self.g = g
        numtf = [1]
        dentf = [self.l * (self.M + self.m), 0, -self.g * (self.M + self.m)]
        self.G = ctrl.TransferFunction(numtf, dentf)

    def simulate(self, K_p, K_i, K_d, theta_0=0, t_end=5, steps=500):
        C = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])
        T = ctrl.feedback(self.G * C)
        t = np.linspace(0, t_end, steps)
        time, response = ctrl.impulse_response(T, T=t)
        response = response + theta_0 
        return time, response

M = 1.0
m = 0.1
l = 1.0

K_p = 1e-10
K_i = 0.4e-12
K_d = 1.5e-10

pendulum_system = PendulumSystem(M, m, l)

initial_angles = [0.1, 0.5, 0.9]
initial_positions = [0.0, 0.2, 0.5] 

fig, axs = plt.subplots(2, len(initial_angles), figsize=(15, 8))

for i, theta_0 in enumerate(initial_angles):
    time, response = pendulum_system.simulate(K_p, K_i, K_d, theta_0=theta_0)
    axs[0, i].plot(time, response, label=f"θ₀={theta_0} rad")
    axs[0, i].set_title(f"Ángulo inicial: θ₀={theta_0} rad")
    axs[0, i].set_xlabel("Tiempo (s)")
    axs[0, i].set_ylabel("Ángulo θ (rad)")
    axs[0, i].grid()
    axs[0, i].legend()

for i, x_0 in enumerate(initial_positions):
    time, response = pendulum_system.simulate(K_p, K_i, K_d, theta_0=x_0)
    axs[1, i].plot(time, response, label=f"x₀={x_0} m")
    axs[1, i].set_title(f"Posición inicial: x₀={x_0} m")
    axs[1, i].set_xlabel("Tiempo (s)")
    axs[1, i].set_ylabel("Ángulo θ (rad)")
    axs[1, i].grid()
    axs[1, i].legend()

plt.tight_layout()
plt.show()
