import numpy as np

class KalmanFilter:
    def __init__(self, A, B, C, Q, R, P_init, x_init):
        """
        Inicializa los parámetros del Filtro de Kalman.
        Args:
            A (ndarray): Matriz de transición de estado.
            B (ndarray): Matriz de control.
            C (ndarray): Matriz de observación.
            Q (ndarray): Covarianza del ruido del proceso.
            R (ndarray): Covarianza del ruido de la medición.
            P_init (ndarray): Matriz de covarianza inicial del estado.
            x_init (ndarray): Estado inicial estimado.
        """
        self.A = A
        self.B = B
        self.C = C
        self.Q = Q
        self.R = R
        self.P = P_init
        self.x = x_init

    def predict(self, u):
        """
        Predice el próximo estado.
        Args:
            u (ndarray): Entrada de control.
        """
        self.x = self.A @ self.x + self.B @ u
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, y):
        """
        Actualiza el estado estimado basado en la medición.
        Args:
            y (ndarray): Medición observada.
        """
        K = self.P @ self.C.T @ np.linalg.inv(self.C @ self.P @ self.C.T + self.R)
        self.x = self.x + K @ (y - self.C @ self.x)
        self.P = (np.eye(len(self.P)) - K @ self.C) @ self.P

    def get_state(self):
        """
        Retorna el estado estimado actual.
        """
        return self.x
    
    def process_with_pid(self, u, t_end=5, steps=500):
        """
        Procesa los datos de un sistema PID optimizado usando el filtro de Kalman.
        Args:
            u (ndarray): Señal de control.
            t_end: Duración de la simulación.
            steps: Número de pasos de simulación.
        Returns:
            ndarray: Estados estimados por el filtro.
        """
        time = np.linspace(0, t_end, steps)
        true_states = []
        kalman_estimates = []
        noisy_measurements = []

        # Simulación de estados reales y mediciones ruidosas
        for t in range(steps):
            true_state = [np.sin(t * 0.1), 0.1 * np.cos(t * 0.1)]
            measurement = true_state[0] + np.random.normal(0, 0.1)

            # Filtro de Kalman
            self.predict(u[t])
            self.update(np.array([[measurement]]))

            true_states.append(true_state)
            kalman_estimates.append(self.get_state().flatten())
            noisy_measurements.append(measurement)

        return np.array(time), np.array(true_states), np.array(noisy_measurements), np.array(kalman_estimates)

    def simulate_kalman_with_pid(A, B, C, Q, R, P_init, x_init, time, noisy_measurements, u_pid):
        kalman_filter = KalmanFilter(A, B, C, Q, R, P_init, x_init)
        estimates = []

        for t, u, y in zip(time, u_pid, noisy_measurements):
            kalman_filter.predict(np.array([[u]]))
            kalman_filter.update(np.array([[y]]))
            estimates.append(kalman_filter.get_state().flatten())
        
        return np.array(estimates)