import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy.optimize import differential_evolution

class PendulumPIDOptimizer:
    def __init__(self, M=0, m=1, l=1, g=9.8):
        self.M = M  # Masa del carrito
        self.m = m  # Masa del péndulo
        self.l = l  # Longitud del péndulo
        self.g = g  # Gravedad
        self.G = self._create_transfer_function()  # Crear la función de transferencia

    # Función de transferencia
    def _create_transfer_function(self):
        numtf = [-1]
        dentf = [self.M * self.l, 0, -(self.M + self.m) * self.g]
        return ctrl.TransferFunction(numtf, dentf)

    # Controlador PID
    def create_pid_controller(self, Kp, Ki, Kd):
        return ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])
    
    # Simular respuesta
    def simulate_response(self, Kp, Ki, Kd, t=np.linspace(0, 5, 500)):
        C = self.create_pid_controller(Kp, Ki, Kd)
        T = ctrl.feedback(self.G * C)
        time, response = ctrl.impulse_response(T, T=t)
        return time, -response  # Invertir la respuesta para coincidir con MATLAB

    # Optimización de valores con algoritmo genético
    def optimize_pid(self, bounds, t=np.linspace(0, 5, 500)):
        # t: Vector de tiempo para la simulación
        # bounds: Lista de límites para [Kp, Ki, Kd]
        def fitness(params):
            Kp, Ki, Kd = params
            _, response = self.simulate_response(Kp, Ki, Kd, t)
            error = np.sum(np.abs(response))  # Minimizar el área bajo la curva (error absoluto)
            return error

        result = differential_evolution(fitness, bounds)
        return result.x  # Retorna los valores óptimos de [Kp, Ki, Kd]

    # Comparación de respuestas
    def plot_responses(self, Kp1, Ki1, Kd1, Kp2, Ki2, Kd2):
        t = np.linspace(0, 5, 500)
        _, response_no_sintonizado = self.simulate_response(Kp1, Ki1, Kd1, t)
        _, response_sintonizado = self.simulate_response(Kp2, Ki2, Kd2, t)

        plt.figure()
        plt.plot(t, response_no_sintonizado, 'b', label='PID no sintonizado')
        plt.plot(t, response_sintonizado, 'r', label='PID sintonizado')
        plt.legend()
        plt.ylim(-2, 2)
        plt.title('Comparación de respuestas al impulso')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Ángulo θ (rad)')
        plt.show()