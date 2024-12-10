import tkinter as tk
from system.inverted_pendulum import InvertedPendulum
from system.animation import PendulumAnimation
from optimization.Optimization import PIDOptimizer
from filtro_kalman.kalmanFilter import KalmanFilter
import matplotlib.pyplot as plt
import design_implementation.PID
import numpy as np
import tkinter as tk

# Simulación con la función de transferencia que involucra la posición del carrito
def run_system_function_position():
    car_mass = 1.0
    pendulum_mass = 0.2
    rod_length = 0.5
    gravity = 9.81
    # Configuración del sistema
    transfer_function_position = {
        'numerator': [rod_length, 0, -gravity],
        'denominator': [rod_length * car_mass, 0, -(car_mass + pendulum_mass) * gravity, 0, 0]
    }
    pendulum = InvertedPendulum(transfer_function_position)
    time, response = pendulum.get_step_response()
    animation = PendulumAnimation(time, response, rod_length=0.5)
    animation.create_animation()
    pendulum.plot_response(time, response, "Posición X (m)", "Respuesta sin PID (posición)")

# Simulación con la función de transferencia que involucra el ángulo
def run_system_function_angle():
    # Configuración del sistema
    transfer_function_angle = {
        'numerator': [-1],
        'denominator': [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81]
    }
    pendulum = InvertedPendulum(transfer_function_angle)
    time, response = pendulum.get_step_response()
    animation = PendulumAnimation(time, response, rod_length=0.5)
    animation.create_animation()
    pendulum.plot_response(time, response, "Ángulo θ (rad)", "Respuesta sin PID (ángulo)")

def run_pid_simulacion():
    transfer_function_angle = {
        'numerator': [-1],
        'denominator': [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81]
    }
    pendulum = InvertedPendulum(transfer_function_angle)
    time, response = pendulum.simulate_with_pid(1e-15, 0.4e-17, 1.5e-15)
    cart_motion = 0.1 * time  # El carrito se mueve hacia la derecha linealmente

    # Crear animación
    animation = PendulumAnimation(time, response, rod_length=1.0, cart_motion=cart_motion)
    animation.create_animation()
    root = tk.Tk()
    design_implementation.PID.PendulumApp(root)
    root.mainloop()

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
    cart_motion = 0.1 * time  # El carrito se mueve hacia la derecha linealmente
    animation = PendulumAnimation(time, response, rod_length=0.5, cart_motion=cart_motion)
    animation.create_animation()
    pendulum.plot_response(time, response, "Ángulo θ (rad)", "PID Optimizado")


def run_pid_with_kalman_filter():
   # Simulación con la función de transferencia que involucra el ángulo
    transfer_function_angle = {
        'numerator': [-1],
        'denominator': [1.0 * 0.5, 0, -(1.0 + 0.2) * 9.81]
    }
    pendulum = InvertedPendulum(transfer_function_angle)
    time, response = pendulum.simulate_with_pid(1e-15, 0.4e-17, 1.5e-15)
    cart_motion = 0.1 * time

    # Configurar el filtro de Kalman
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
        kalman_filter.predict(np.array([[0]]))  # Control sin fuerza inicial
        kalman_filter.update(np.array([[y]]))
        kalman_estimates.append(kalman_filter.get_state().flatten())
    kalman_estimates = np.array(kalman_estimates)

    # Crear animación
    animation = PendulumAnimation(time, response, rod_length=1.0, cart_motion=cart_motion, kalman_estimates=kalman_estimates)
    animation.create_animation()

    # Gráficos
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

# Creación de la interfaz gráfica
root = tk.Tk()
root.title("Menú de Simulación PID")

# Etiqueta principal
label = tk.Label(root, text="Seleccione una opción:", font=("Arial", 14))
label.pack(pady=10)

# Botones de opciones
btn_withoud_pid_position = tk.Button(root, text="Sistema sin PID (posición)", font=("Arial", 12),
                                 command=run_system_function_position)
btn_withoud_pid_position.pack(pady=5)

btn_withoud_pid_angle = tk.Button(root, text="Sistema sin PID (ángulo)", font=("Arial", 12),
                                 command=run_system_function_angle)
btn_withoud_pid_angle.pack(pady=5)

btn_pid_unoptimized = tk.Button(root, text="Simulacion PID", font=("Arial", 12),
                                 command=run_pid_simulacion)
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
