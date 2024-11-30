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
