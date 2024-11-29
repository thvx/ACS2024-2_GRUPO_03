from design_implementation.PID import PendulumSystem
from optimization.Optimization import PIDOptimizer
import matplotlib.pyplot as plt

def main():
    # Parámetros del sistema
    M = 1.0  # Masa del carrito
    m = 0.1  # Masa del péndulo
    l = 1.0  # Longitud de la varilla
    theta_0 = 0.5  # Ángulo inicial en radianes (por ejemplo, 30 grados)

    # Crear el sistema de péndulo
    pendulum_system = PendulumSystem(M, m, l)

    # Crear el optimizador PID
    pid_optimizer = PIDOptimizer(pendulum_system, theta_0=theta_0)

    # Definir los límites para la optimización de Kp, Ki, Kd
    bounds = [(0, 100), (0, 10), (0, 20)]

    # Optimizar los parámetros PID
    optimized_params = pid_optimizer.optimize(bounds)

    # Mostrar los parámetros optimizados
    print(f"Parámetros optimizados: Kp={optimized_params[0]}, Ki={optimized_params[1]}, Kd={optimized_params[2]}")

    # Simular la respuesta con PID manual y optimizado
    Kp_initial, Ki_initial, Kd_initial = 20, 0.7, 5  # PID inicial (ajustado manualmente)
    time_initial, response_initial = pendulum_system.simulate(Kp_initial, Ki_initial, Kd_initial, theta_0=theta_0)
    time_optimized, response_optimized = pendulum_system.simulate(optimized_params[0], optimized_params[1], optimized_params[2], theta_0=theta_0)

    # Graficar las respuestas
    plt.figure()
    plt.plot(time_initial, response_initial, label="PID Inicial", linestyle='-', color='r')
    plt.plot(time_optimized, response_optimized, label="PID Optimizado", linestyle='--', color='b')

    # Títulos y etiquetas
    plt.title("Comparación de Respuestas del Péndulo")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Ángulo θ (rad)")

    # Leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()