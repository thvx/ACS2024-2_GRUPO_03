import numpy as np
import control as ctrl
from scipy.optimize import differential_evolution

class PIDOptimizer:
    def __init__(self, transfer_function_dict):
        self.numerator = transfer_function_dict['numerator']
        self.denominator = transfer_function_dict['denominator']
        self.tf = ctrl.TransferFunction(self.numerator, self.denominator)

    # Obtendremos el error mediante este método
    def objective_function(self, params):
        K_p, K_i, K_d = params # Obtenemos Kp,Ki y Kd en función de los parámetros que se pasan
        C = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])
        T = ctrl.feedback(self.tf * C)

        # Simular el sistema durante 5 segundos
        t_end = 5
        steps = 500
        time = np.linspace(0, t_end, steps)
        _, response = ctrl.step_response(T, T=time)

        # Obtener el error
        error = np.mean(np.square(response))
        return error

    def optimize_pid(self):
        # Rango de valores para K_p, K_i y K_d
        bounds = [(0.0, 10.0), (0.0, 5.0), (0.0, 5.0)]

        result = differential_evolution(self.objective_function, bounds)
        optimized_params = result.x

        # Mostrar parámetros optimizados
        print(f"Parámetros optimizados PID:")
        print(f"Kp: {optimized_params[0]}, Ki: {optimized_params[1]}, Kd: {optimized_params[2]}")

        return optimized_params

    def simulate_with_optimized_pid(self, K_p, K_i, K_d):
        # Simular la respuesta con parámetors optimizados
        C = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])
        T = ctrl.feedback(self.tf * C)

        t_end = 5
        steps = 500
        time = np.linspace(0, t_end, steps)
        _, response = ctrl.step_response(T, T=time)
        
        return K_p, K_i, K_d