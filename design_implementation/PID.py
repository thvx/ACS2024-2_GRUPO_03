import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

class PendulumSystem:
    def __init__(self, M, m, l, g=9.8):
        """
        Inicializa el sistema del péndulo invertido.
        M: Masa del carrito
        m: Masa del péndulo
        l: Longitud de la varilla
        g: Gravedad
        """
        self.M = M  # Masa del carrito
        self.m = m  # Masa del péndulo
        self.l = l  # Longitud de la varilla
        self.g = g  # Gravedad

        # Crear la función de transferencia del sistema
        numtf = [1]  # El efecto de la fuerza está en el numerador
        dentf = [self.l * (self.M + self.m), 0, -self.g * (self.M + self.m)]  # Denominador ajustado
        self.G = ctrl.TransferFunction(numtf, dentf)

    def simulate(self, K_p, K_i, K_d, theta_0=0, u_func=None, t_end=5, steps=500):
        # Crear el controlador PID
        C = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])
        
        # Crear el sistema en lazo cerrado
        T = ctrl.feedback(self.G * C)
        
        # Tiempo de simulación
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

    def plot_response(self, time, response, title="Respuesta del sistema"):
        """
        Grafica la respuesta del sistema.
        """
        plt.figure()
        plt.plot(time, response)
        plt.title(title)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo θ (rad)")
        plt.grid()
        plt.show()