import numpy as np
import matplotlib.pyplot as plt
from system.inverted_pendulum import InvertedPendulum
from system.animation import PendulumAnimation
from optimization.Optimization import PIDOptimizer
from filtro_kalman.kalmanFilter import KalmanFilter
import design_implementation.PID
import tkinter as tk


def create_transfer_function(numerator, denominator):
    return {'numerator': numerator, 'denominator': denominator}


def setup_pendulum(transfer_function):
    return InvertedPendulum(transfer_function)


def create_and_animate_pendulum(pendulum, time, response, rod_length=0.5, cart_motion=None, kalman_estimates=None):
    animation = PendulumAnimation(time, response, rod_length=rod_length, cart_motion=cart_motion, kalman_estimates=kalman_estimates)
    animation.create_animation()


def run_system_simulation(title, ylabel, numerator, denominator):
    transfer_function = create_transfer_function(numerator, denominator)
    pendulum = setup_pendulum(transfer_function)
    time, response = pendulum.get_step_response()
    create_and_animate_pendulum(pendulum, time, response)
    pendulum.plot_response(time, response, ylabel, title)


def run_pid_simulation_with_params(K_p, K_i, K_d, rod_length=1.0):
    transfer_function = create_transfer_function([-1], [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81])
    pendulum = setup_pendulum(transfer_function)
    time, response = pendulum.simulate_with_pid(K_p, K_i, K_d)
    cart_motion = 0.1 * time
    create_and_animate_pendulum(pendulum, time, response, rod_length=rod_length, cart_motion=cart_motion)
    pendulum.plot_response(time, response, "Ángulo θ (rad)", "Respuesta Con PID")


def run_system_function_position():
    run_system_simulation(
        title="Respuesta sin PID (posición)",
        ylabel="Posición X (m)",
        numerator=[0.5, 0, -9.81],
        denominator=[0.5 * 1.0, 0, -(1.0 + 0.2) * 9.81, 0, 0]
    )


def run_system_function_angle():
    run_system_simulation(
        title="Respuesta sin PID (ángulo)",
        ylabel="Ángulo θ (rad)",
        numerator=[-1],
        denominator=[1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81]
    )


def run_pid_simulacion():
    run_pid_simulation_with_params(1e-10, 0.4e-12, 1.5e-10)
    root = tk.Tk()
    design_implementation.PID.PendulumApp(root)
    root.mainloop()


def run_pid_optimized():
    transfer_function = create_transfer_function([-1], [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81])
    pendulum = setup_pendulum(transfer_function)
    optimizer = PIDOptimizer(transfer_function)
    K_p, K_i, K_d = optimizer.optimize_pid()
    run_pid_simulation_with_params(K_p, K_i, K_d, rod_length=0.5)
    time, response = pendulum.simulate_with_pid(K_p, K_i, K_d)
    pendulum.plot_response(time, response, "Ángulo θ (rad)", "PID Optimizado")


def run_pid_with_kalman_filter():
    transfer_function = create_transfer_function([-1], [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81])
    pendulum = setup_pendulum(transfer_function)
    time, response = pendulum.simulate_with_pid(1e-15, 0.4e-17, 1.5e-15)
    cart_motion = 0.1 * time

    # Configurar filtro de Kalman
    A = np.array([[1, 0.1], [0, 1]])
    B = np.array([[0], [0.1]])
    C = np.array([[1, 0]])
    Q = np.array([[1e-4, 0], [0, 1e-2]])
    R = np.array([[0.1]])
    P_init = np.eye(2)
    x_init = np.array([[0], [0]])
    kalman_filter = KalmanFilter(A, B, C, Q, R, P_init, x_init)

    # Simulación
    t_end = 5
    steps = 500
    time = np.linspace(0, t_end, steps)
    true_angle = np.sin(time)
    noisy_measurements = true_angle + np.random.normal(0, 0.1, size=len(time))

    kalman_estimates = []
    for t, y in zip(time, noisy_measurements):
        kalman_filter.predict(np.array([[0]]))
        kalman_filter.update(np.array([[y]]))
        kalman_estimates.append(kalman_filter.get_state().flatten())
    kalman_estimates = np.array(kalman_estimates)

    create_and_animate_pendulum(pendulum, time, response, rod_length=1.0, cart_motion=cart_motion, kalman_estimates=kalman_estimates)

    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time, true_angle, label="Ángulo real")
    plt.plot(time, kalman_estimates[:, 0], label="Estimación Kalman")
    plt.title("Ángulo vs Tiempo")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time, noisy_measurements, label="Mediciones ruidosas")
    plt.title("Ruido vs Tiempo")
    plt.legend()

    plt.tight_layout()
    plt.show()
