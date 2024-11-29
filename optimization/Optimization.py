import numpy as np
from scipy.optimize import differential_evolution

class PIDOptimizer:
    def __init__(self, pendulum_system, theta_0=0, t_end=5, steps=500):
        # pendulum_system: Instancia del sistema de péndulo
        # theta_0: Ángulo inicial del péndulo
        # t_end: Tiempo final de la simulación
        # steps: Número de pasos de tiempo en la simulación
        self.pendulum_system = pendulum_system
        self.theta_0 = theta_0
        self.t_end = t_end
        self.steps = steps

    def cost_function(self, params):
        # Calcula el error total
        K_p, K_i, K_d = params
        time, response = self.pendulum_system.simulate(K_p, K_i, K_d, theta_0=self.theta_0, t_end=self.t_end, steps=self.steps)
        error = np.sum(np.abs(response))  # Error total como suma de valores absolutos
        return error

    def optimize(self, bounds):
        # bounds: [(min, max), (min, max), (min, max)]
        result = differential_evolution(self.cost_function, bounds, strategy='best1bin', maxiter=100, popsize=15, seed=42)
        return result.x  # Devuelve las constantes optimizadas
