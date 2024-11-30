import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from DisenoPID.PID import PendulumApp
from Optimizacion.Optimization import PendulumPIDOptimizer
from System.animation import PendulumAnimation
from System.inverted_pendulum import InvertedPendulum
from System.plot import plot_step_response
from FiltroKalman.kalmanGraphics import KalmanGraphicsApp

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Péndulo Invertido")

        # Título principal
        title_label = ttk.Label(root, text="Menú Principal", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Opciones del menú
        ttk.Button(root, text="PID sin optimización", command=self.open_pid_app).pack(pady=10)
        ttk.Button(root, text="PID optimizado", command=self.show_pid_optimized).pack(pady=10)
        ttk.Button(root, text="Péndulo invertido con filtro de Kalman", command=self.kalman_option).pack(pady=10)

    def open_pid_app(self):
        """Abre la interfaz de diseño e implementación de PID sin optimización."""
        pid_window = tk.Toplevel(self.root)
        PendulumApp(pid_window)

    def show_pid_optimized(self):
        """Muestra la animación y gráficas del PID optimizado."""
        # Parámetros iniciales
        car_mass = 1.0
        pendulum_mass = 0.2
        rod_length = 1.0
        gravity = 9.81

        # Crear el optimizador
        optimizer = PendulumPIDOptimizer(M=car_mass, m=pendulum_mass, l=rod_length, g=gravity)

        # PID inicial y optimización
        Kp_initial, Ki_initial, Kd_initial = 50, 5, 10
        bounds = [(0, 100), (0, 10), (0, 50)]  # Límites para los parámetros
        Kp_opt, Ki_opt, Kd_opt = optimizer.optimize_pid(bounds)

        # Respuesta inicial y optimizada
        time_steps = np.linspace(0, 5, 500)
        _, response_initial = optimizer.simulate_response(Kp_initial, Ki_initial, Kd_initial, time_steps)
        _, response_optimized = optimizer.simulate_response(Kp_opt, Ki_opt, Kd_opt, time_steps)

        # Crear ventana nueva para mostrar resultados
        optimized_window = tk.Toplevel(self.root)
        optimized_window.title("PID Optimizado")

        fig_frame = ttk.Frame(optimized_window)
        fig_frame.pack(fill="both", expand=True)

        # Configurar las gráficas
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))
        ax[0].plot(time_steps, response_initial, label="PID Inicial", color="blue")
        ax[0].set_title("Respuesta sin optimización")
        ax[0].set_xlabel("Tiempo (s)")
        ax[0].set_ylabel("Ángulo θ (rad)")
        ax[0].grid()
        ax[0].legend()

        ax[1].plot(time_steps, response_optimized, label="PID Optimizado", color="red")
        ax[1].set_title("Respuesta con optimización")
        ax[1].set_xlabel("Tiempo (s)")
        ax[1].set_ylabel("Ángulo θ (rad)")
        ax[1].grid()
        ax[1].legend()

        # Integrar con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def kalman_option(self):
        """Abre la interfaz de control y gráficos del filtro de Kalman."""
        kalman_window = tk.Toplevel(self.root)
        KalmanGraphicsApp(kalman_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
