import numpy as np
import control as ctrl


class InvertedPendulum:
    def __init__(self, transfer_function_dict):
        self.numerator = transfer_function_dict['numerator']
        self.denominator = transfer_function_dict['denominator']

    def get_transfer_function(self):
        return ctrl.TransferFunction(self.numerator, self.denominator)

    def get_step_response_data(self):
        transfer_function_system = self.get_transfer_function()

        # Definimos el tiempo de simulación con np.linspace
        # 5000 puntos en 5 segundos
        time = np.linspace(0, 5, 5000)

        # Obtenemos la respuesta al escalón utilizando step_response
        time, response = ctrl.step_response(transfer_function_system, time)

        return time, response
