import numpy as np
import control as ctrl
import matplotlib.pyplot as plt


class InvertedPendulum:
    def __init__(self, transfer_function_dict):
        self.numerator = transfer_function_dict['numerator']
        self.denominator = transfer_function_dict['denominator']
        self.tf = ctrl.TransferFunction(self.numerator, self.denominator)

    def get_transfer_function(self):
        return self.tf

    def simulate_without_pid(self, t_end=5, steps=500):
        """Simula la respuesta del sistema sin control (sistema abierto)."""
        time = np.linspace(0, t_end, steps)
        time, response = ctrl.step_response(self.tf, T=time)
        return time, response

    def simulate_with_pid(self, K_p, K_i, K_d, t_end=5, steps=500):
        """Simula la respuesta del sistema con un controlador PID (sistema cerrado)."""
        # Controlador PID
        C = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])
        # Sistema en lazo cerrado
        T = ctrl.feedback(self.tf * C)
        time = np.linspace(0, t_end, steps)
        time, response = ctrl.step_response(T, T=time)
        return time, response

    def plot_response(self, time, response, title="Respuesta del sistema"):
        """Grafica la respuesta del sistema."""
        plt.figure()
        plt.plot(time, response)
        plt.title(title)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo θ (rad)")
        plt.grid()
        plt.show()
