import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'design_implementation'))
from PID import PendulumSystem

M = 1.0
m = 0.1
l = 1.0
theta_0 = 0.5

pid_manual = {"K_p": 1e-10, "K_i": 0.4e-12, "K_d": 1.5e-10}
pid_optimizado = {"K_p": 4.440892098500626e-15, "K_i": 0.0, "K_d": 4.884981308350689e-15}

pendulum_system = PendulumSystem(M, m, l)

time_manual, response_manual = pendulum_system.simulate(
    pid_manual["K_p"], pid_manual["K_i"], pid_manual["K_d"], theta_0
)
error_manual = theta_0 - response_manual

time_opt, response_opt = pendulum_system.simulate(
    pid_optimizado["K_p"], pid_optimizado["K_i"], pid_optimizado["K_d"], theta_0
)
error_opt = theta_0 - response_opt

plt.figure(figsize=(10, 6))

plt.plot(time_manual, error_manual, label="PID Manual", color="red", linestyle="--")

plt.plot(time_opt, error_opt, label="PID Optimizado", color="green", linestyle="-")

plt.title("Curvas de Error: PID Manual vs. PID Optimizado")
plt.xlabel("Tiempo (s)")
plt.ylabel("Error (rad)")
plt.legend()
plt.grid()
plt.show()