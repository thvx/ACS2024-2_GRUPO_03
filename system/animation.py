import plotly.graph_objects as go
import numpy as np

class PendulumAnimation:
    def __init__(self, time_steps, response, rod_length, cart_motion=None):
        """
        Inicializa la animación del péndulo.
        
        :param time_steps: Array de tiempos.
        :param response: Respuesta angular del péndulo.
        :param rod_length: Longitud de la varilla del péndulo.
        :param cart_motion: Array opcional que define el desplazamiento del carrito en cada paso.
        """
        self.time_steps = time_steps
        self.response = response
        self.rod_length = rod_length
        self.cart_motion = cart_motion

    def create_animation(self):
        """Crea una animación basada en los datos de la simulación."""
        frames = []  # Lista para almacenar los frames de la animación
        x_data = 0  # Posición inicial del carrito

        for i in range(len(self.time_steps)):
            theta = self.response[i]
            adjusted_theta = np.pi - theta

            # Si no se proporciona un cart_motion, calcula dinámicamente el movimiento
            if self.cart_motion is None:
                x_data += 0.05 * np.sin(theta)
            else:
                x_data = self.cart_motion[i]

            # Coordenadas del péndulo
            pendulum_x = [x_data, x_data + self.rod_length * np.sin(adjusted_theta)]
            pendulum_y = [0, -self.rod_length * np.cos(adjusted_theta)]

            # Creamos un frame para la animación
            frames.append(go.Frame(data=[
                # Dibujamos el carrito
                go.Scatter(x=[x_data - 0.1, x_data + 0.1], y=[0, 0], mode='lines', line=dict(width=10)),
                # Dibujamos el péndulo
                go.Scatter(x=pendulum_x, y=pendulum_y, mode='lines+markers', line=dict(width=4), marker=dict(size=8))
            ]))

        # Creamos la figura de la animación
        fig = go.Figure(
            data=[
                go.Scatter(x=[0, 0], y=[0, 0], mode='lines', line=dict(width=10)),
                go.Scatter(x=[0, 0], y=[0, 0], mode='lines+markers', line=dict(width=4), marker=dict(size=8))
            ],
            layout=go.Layout(
                xaxis=dict(range=[-2, 2], autorange=False),
                yaxis=dict(range=[-1.5, 1.5], autorange=False),
                updatemenus=[dict(type="buttons", showactive=False,
                                  buttons=[dict(label="Play", method="animate",
                                                args=[None, {"frame": {"duration": 20}, "fromcurrent": True}])])],
            ),
            frames=frames
        )

        fig.show()
