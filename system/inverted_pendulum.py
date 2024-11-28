import numpy as np
import control as ctrl
import matplotlib.pyplot as plt


class InvertedPendulum:
    def __init__(self, transfer_function_dict):
        self.numerator = transfer_function_dict['numerator']
        self.denominator = transfer_function_dict['denominator']

    def get_transfer_function(self):
        return ctrl.TransferFunction(self.numerator, self.denominator)

    # Función para graficar la respuesta al escalón
    def plot_step_response(self):
        transfer_function_system = self.get_transfer_function()

        # Definimos el tiempo de simulación con np.linspace
        # Tiempo de simulación (de 0 a 10 segundos, con 100 puntos)
        time = np.linspace(0, 10, 100)

        # Obtenemos la respuesta al escalón utilizando step_response
        time, response = ctrl.step_response(transfer_function_system, time)

        # Imprimimos los valores
        print(time)
        print(response)

        # Graficamos la respuesta
        plt.plot(time, response)
        plt.title("Respuesta al escalón del system de péndulo invertido")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo θ (rad)")
        plt.grid(True)
        plt.show()
