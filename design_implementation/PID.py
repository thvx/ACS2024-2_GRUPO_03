import numpy as np
import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class PendulumSystem:
    def __init__(self, M, m, l, g=9.8):
        self.M = M
        self.m = m
        self.l = l
        self.g = g
        numtf = [1]
        dentf = [self.l * (self.M + self.m), 0, -self.g * (self.M + self.m)]
        self.G = ctrl.TransferFunction(numtf, dentf)
    def simulate(self, K_p, K_i, K_d, theta_0=0, u_func=None, t_end=5, steps=500):
        C = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])
        T = ctrl.feedback(self.G * C)
        t = np.linspace(0, t_end, steps)
        # Simulación con entrada personalizada
        if u_func is None:
            # Si no hay una función para \( u(t) \), usar un impulso
            time, response = ctrl.impulse_response(T, T=t)
        else:
            # Usar la función \( u(t) \) para generar la entrada
            u_values = np.array([u_func(ti) for ti in t])  # Evaluar \( u(t) \) en cada paso de tiempo
            time, response, _ = ctrl.forced_response(T, T=t, U=u_values)
        # Asegurarse de que el ángulo inicial se maneje correctamente
        response = response + theta_0  # Ajuste correcto del ángulo inicial
        
        return time, response
class PendulumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controlador de Péndulo Invertido")
        # Crear un marco para los sliders
        self.slider_frame = ttk.Frame(root)
        self.slider_frame.pack(side='left', padx=10, pady=10)
        # Inicializar parámetros del sistema del péndulo
        self.M = 1.0  # Masa del carrito
        self.m = 0.1  # Masa del péndulo
        self.l = 1.0  # Longitud del péndulo
        self.theta_0 = 0.5  # Ángulo inicial
        # Crear sliders para M, m y l
        self.M_slider = self.create_slider("M (Masa del Carrito)", 0.1, 5.0, self.M)
        self.m_slider = self.create_slider("m (Masa del Péndulo)", 0.01, 2.0, self.m)
        self.l_slider = self.create_slider("l (Longitud del Péndulo)", 0.1, 2.0, self.l)
        # Crear sliders para Kp, Ki y Kd
        self.Kp_slider = self.create_slider("Kp", 0, 100, 20)
        self.Ki_slider = self.create_slider("Ki", 0, 10, 0.7)
        self.Kd_slider = self.create_slider("Kd", 0, 20, 5)
        # Botón para actualizar las gráficas
        self.update_button = ttk.Button(self.slider_frame, text="Actualizar Gráficas", command=self.update_plots)
        self.update_button.pack(pady=10)
        # Crear un marco para las gráficas
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side='right', padx=10, pady=10)
        # Crear las figuras para las gráficas
        self.fig, self.axs = plt.subplots(2, 2, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack()
        # Graficar inicialmente
        self.update_plots()
    def create_slider(self, label, min_val, max_val, initial):
        frame = ttk.Frame(self.slider_frame)
        frame.pack(pady=5)
        slider = ttk.Scale(frame, from_=min_val, to=max_val, orient='horizontal', command=lambda e: self.update_plots())
        slider.set(initial)
        slider.pack(side='left')
        label = ttk.Label(frame, text=label)
        label.pack(side='left')
        return slider
    def update_plots(self):
        # Obtener valores de los sliders
        M = self.M_slider.get()
        m = self.m_slider.get()
        l = self.l_slider.get()
        Kp = self.Kp_slider.get()
        Ki = self.Ki_slider.get()
        Kd = self.Kd_slider.get()
        # Actualizar el sistema del péndulo con los nuevos parámetros
        self.pendulum_system = PendulumSystem(M, m, l)
        # Limpiar las gráficas
        for ax in self.axs.flatten():
            ax.clear()
        # Simulaciones para cada tipo de controlador
        controllers = {
            'P': (Kp, 0, 0),
            'PI': (Kp, Ki, 0),
            'PD': (Kp, 0, Kd),
            'PID': (Kp, Ki, Kd)
        }
        for i, (ctrl_type, gains) in enumerate(controllers.items()):
            Kp, Ki, Kd = gains
            time, response = self.pendulum_system.simulate(Kp, Ki, Kd, theta_0=self.theta_0)
            ax = self.axs[i // 2, i % 2]
            ax.plot(time, response, label=ctrl_type)
            ax.set_title(f'Respuesta del Controlador {ctrl_type}')
            ax.set_xlabel('Tiempo (s)')
            ax.set_ylabel('Ángulo θ (rad)')
            ax.grid()
            ax.legend()
        self.canvas.draw()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PendulumApp(root)
    root.mainloop()