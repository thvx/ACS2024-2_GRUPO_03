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
    
    def process_with_pid(self, K_p, K_i, K_d, u, theta_0=0, t_end=5, steps=500):
        """
        Procesa los datos de un sistema PID optimizado usando el filtro de Kalman.
        Args:
            K_p, K_i, K_d: Constantes PID.
            u (ndarray): Señal de control.
            theta_0: Ángulo inicial.
            t_end: Duración de la simulación.
            steps: Número de pasos de simulación.
        Returns:
            ndarray: Estados estimados por el filtro.
        """
        time = np.linspace(0, t_end, steps)
        true_states = np.zeros((steps, self.x.shape[0]))
        noisy_measurements = np.zeros(steps)
        kalman_estimates = np.zeros((steps, self.x.shape[0]))

        # Simulación de estados reales y mediciones ruidosas
        for t in range(steps):
            true_states[t, 0] = theta_0 + np.sin(t * 0.1)
            noisy_measurements[t] = true_states[t, 0] + np.random.normal(0, self.noise_std)

            # Predicción y corrección con el filtro de Kalman
            self.predict(u[t])
            self.update(np.array([[noisy_measurements[t]]]))
            kalman_estimates[t] = self.get_state().flatten()

        return time, true_states, noisy_measurements, kalman_estimates

    def simulate_kalman_with_pid(A, B, C, Q, R, P_init, x_init, time, true_angle, noisy_measurements, u_pid):
        kalman_filter = KalmanFilter(A, B, C, Q, R, P_init, x_init)
        estimates = []

        for t, u, y in zip(time, u_pid, noisy_measurements):
            kalman_filter.predict(np.array([[u]]))
            kalman_filter.update(np.array([[y]]))
            estimates.append(kalman_filter.get_state().flatten())
        
        return np.array(estimates)