from Optimization import PendulumPIDOptimizer
import matplotlib.pyplot as plt

pendulum_optimizer = PendulumPIDOptimizer()

# PID inicial sin sintonizar
Kp_initial, Ki_initial, Kd_initial = 100, 75, 10

# Graficar respuesta inicial
time, response = pendulum_optimizer.simulate_response(Kp_initial, Ki_initial, Kd_initial)
plt.figure()
plt.plot(time, response)
plt.ylim(-2, 2)
plt.title('Respuesta inicial sin sintonizar')
plt.xlabel('Tiempo (s)')
plt.ylabel('Ángulo θ (rad)')
plt.show()

# Optimizar PID
bounds = [(0, 200), (0, 100), (0, 50)]  # Límites para [Kp, Ki, Kd]
Kp_opt, Ki_opt, Kd_opt = pendulum_optimizer.optimize_pid(bounds)

print(f"Parámetros óptimos: Kp = {Kp_opt:.2f}, Ki = {Ki_opt:.2f}, Kd = {Kd_opt:.2f}")

# Graficar comparación entre PID sin sintonizar y optimizado
pendulum_optimizer.plot_responses(Kp_initial, Ki_initial, Kd_initial, Kp_opt, Ki_opt, Kd_opt)