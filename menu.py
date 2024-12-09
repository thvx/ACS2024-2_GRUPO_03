import tkinter as tk
from system.inverted_pendulum import InvertedPendulum
from system.animation import PendulumAnimation
from optimization.Optimization import PIDOptimizer
from filtro_kalman.kalmanFilter import KalmanFilter
import matplotlib.pyplot as plt
import numpy as np

def run_pid_unoptimized():
    """Ejecuta la simulación del PID sin optimizar."""
    # Configuración del sistema
    transfer_function_angle = {
        'numerator': [-1],
        'denominator': [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81]
    }
    pendulum = InvertedPendulum(transfer_function_angle)
    time, response = pendulum.get_step_response()
    animation = PendulumAnimation(time, response, rod_length=0.5)
    animation.create_animation()
    pendulum.plot_response(time, response, "Ángulo θ (rad)", "PID Sin Optimizar")


def run_pid_optimized():
    """Ejecuta la simulación del PID optimizado."""
    # Configuración del sistema
    transfer_function_angle = {
        'numerator': [-1],
        'denominator': [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81]
    }
    pendulum = InvertedPendulum(transfer_function_angle)
    optimizer = PIDOptimizer(transfer_function_angle)
    K_p, K_i, K_d = optimizer.optimize_pid()
    time, response = pendulum.simulate_with_pid(K_p, K_i, K_d)
    animation = PendulumAnimation(time, response, rod_length=0.5)
    animation.create_animation()
    pendulum.plot_response(time, response, "Ángulo θ (rad)", "PID Optimizado")


def run_pid_with_kalman_filter():
    """Ejecuta la simulación del PID optimizado con filtro de Kalman."""
    # Configuración del sistema
    A = np.array([[1, 0.1], [0, 1]])
    B = np.array([[0], [0.1]])
    C = np.array([[1, 0]])
    Q = np.array([[1e-4, 0], [0, 1e-2]])
    R = np.array([[1e-1]])
    P_init = np.eye(2)
    x_init = np.array([[0], [0]])

    time = np.linspace(0, 5, 500)
    true_angle = np.sin(time)
    noisy_measurements = true_angle + np.random.normal(0, 0.1, size=len(time))
    u_pid = np.zeros_like(time)  # Reemplazar con señal de control PID

    kalman_estimates = KalmanFilter.simulate_kalman_with_pid(A, B, C, Q, R, P_init, x_init, time, true_angle, noisy_measurements, u_pid)

    # Animación
    animation = PendulumAnimation(time, true_angle, rod_length=0.5, kalman_estimates=kalman_estimates)
    animation.create_animation()

    # Gráficos
    plt.figure(figsize=(10, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(time, true_angle, label="Ángulo real")
    plt.plot(time, kalman_estimates[:, 0], label="Estimación Kalman")
    plt.title("Ángulo estimado vs real")
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(time, noisy_measurements, label="Mediciones ruidosas")
    plt.title("Ángulo medido")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time, true_angle - kalman_estimates[:, 0], label="Error de estimación")
    plt.title("Error de estimación")
    plt.legend()
    
    plt.tight_layout()
    plt.show()


# Creación de la interfaz gráfica
root = tk.Tk()
root.title("Menú de Simulación PID")

# Etiqueta principal
label = tk.Label(root, text="Seleccione una opción:", font=("Arial", 14))
label.pack(pady=10)

# Botones de opciones
btn_pid_unoptimized = tk.Button(root, text="PID Sin Optimizar", font=("Arial", 12),
                                 command=run_pid_unoptimized)
btn_pid_unoptimized.pack(pady=5)

btn_pid_optimized = tk.Button(root, text="PID Optimizado", font=("Arial", 12),
                               command=run_pid_optimized)
btn_pid_optimized.pack(pady=5)

btn_pid_kalman = tk.Button(root, text="PID Optimizado con Filtro de Kalman", font=("Arial", 12),
                           command=run_pid_with_kalman_filter)
btn_pid_kalman.pack(pady=5)

# Botón para salir
btn_exit = tk.Button(root, text="Salir", font=("Arial", 12), command=root.quit)
btn_exit.pack(pady=20)

# Ejecutar la interfaz gráfica
root.mainloop()