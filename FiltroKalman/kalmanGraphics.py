import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from FiltroKalman.kalmanFilter import KalmanFilter

class KalmanGraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro de Kalman: Control y Gráficos")

        # Parámetros del sistema
        self.init_system()

        # Interfaz gráfica
        self.create_widgets()

    def init_system(self):
        """Inicializa el sistema y los parámetros del Filtro de Kalman."""
        # Parámetros del modelo
        self.A = np.array([[1, 0.1], [0, 1]])
        self.B = np.array([[0], [0.1]])
        self.C = np.array([[1, 0]])
        self.Q = np.array([[1e-4, 0], [0, 1e-2]])  # Ruido del proceso
        self.R = np.array([[1e-1]])  # Ruido de la medición
        self.P_init = np.eye(2)
        self.x_init = np.array([[0], [0]])

        self.kalman_filter = KalmanFilter(self.A, self.B, self.C, self.Q, self.R, self.P_init, self.x_init)
        self.noise_std = 0.1  # Desviación estándar del ruido

    def create_widgets(self):
        """Crea los widgets de control e interacción."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Barra para controlar el ruido del proceso
        ttk.Label(control_frame, text="Ruido del Proceso (Q)").pack(pady=5)
        self.q_scale = ttk.Scale(control_frame, from_=1e-5, to=1e-1, orient="horizontal", command=self.update_q)
        self.q_scale.set(1e-4)
        self.q_scale.pack(pady=5)

        # Barra para controlar el ruido de la medición
        ttk.Label(control_frame, text="Ruido de la Medición (R)").pack(pady=5)
        self.r_scale = ttk.Scale(control_frame, from_=1e-2, to=1, orient="horizontal", command=self.update_r)
        self.r_scale.set(1e-1)
        self.r_scale.pack(pady=5)

        # Botón para simular y mostrar gráficos
        ttk.Button(control_frame, text="Simular", command=self.simulate).pack(pady=20)

        # Frame para los gráficos
        self.fig, self.ax = plt.subplots(3, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def update_q(self, value):
        """Actualiza el ruido del proceso."""
        self.Q[0, 0] = float(value)
        self.Q[1, 1] = float(value)

    def update_r(self, value):
        """Actualiza el ruido de la medición."""
        self.R[0, 0] = float(value)

    def simulate(self):
        """Simula el sistema con el filtro de Kalman y muestra los gráficos."""
        # Configuración de la simulación
        steps = 100
        u = np.zeros((steps, 1))  # Entrada de control
        true_angle = np.zeros(steps)
        noisy_measurements = np.zeros(steps)
        kalman_estimates = np.zeros((steps, self.kalman_filter.x.shape[0]))

        # Simulación
        for t in range(steps):
            # Dinámica del sistema real
            true_angle[t] = np.sin(t * 0.1)  # Ejemplo: ángulo real
            noisy_measurements[t] = true_angle[t] + np.random.normal(0, self.noise_std)

            # Predicción y actualización de Kalman
            self.kalman_filter.predict(u[t])
            self.kalman_filter.update(np.array([[noisy_measurements[t]]]))
            kalman_estimates[t] = self.kalman_filter.get_state().flatten()[:2]

        # Actualizar gráficos
        self.ax[0].clear()
        self.ax[0].plot(true_angle, label="Ángulo Real", color="blue")
        self.ax[0].plot(kalman_estimates[:, 0], label="Estimación Kalman", color="red")
        self.ax[0].set_title("Variación del Ángulo")
        self.ax[0].legend()

        self.ax[1].clear()
        self.ax[1].plot(noisy_measurements, label="Medición con Ruido", color="green")
        self.ax[1].set_title("Ruido de la Medición")
        self.ax[1].legend()

        self.ax[2].clear()
        self.ax[2].plot(kalman_estimates[:, 1], label="Velocidad Estimada", color="purple")
        self.ax[2].set_title("Ruido del Proceso")
        self.ax[2].legend()

        self.canvas.draw()
