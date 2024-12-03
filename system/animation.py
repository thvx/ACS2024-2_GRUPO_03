import numpy as np
import plotly.graph_objects as go


class PendulumAnimation:
    def __init__(self, time_steps, response, rod_length):
        self.time_steps = time_steps
        self.response = response * 100  # Aumentamos la escala para una animación más rápida
        self.rod_length = rod_length

    def create_animation(self):
        frames = []  # Lista para almacenar los frames de la animación
        x_data = 0  # Posición inicial del carrito

        for i in range(len(self.time_steps)):
            # Calculamos el ángulo y ajusta para la posición vertical invertida
            theta = self.response[i]
            adjusted_theta = np.pi - theta

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

            # Desplazamos el carrito proporcionalmente al ángulo
            x_data += 0.05 * np.sin(theta)

        # Creamos la figura de la animación
        fig = go.Figure(
            data=[
                # Carrito en su posición inicial
                go.Scatter(x=[0, 0], y=[0, 0], mode='lines', line=dict(width=10)),
                # Péndulo en su posición inicial
                go.Scatter(x=[0, 0], y=[0, 0], mode='lines+markers', line=dict(width=4), marker=dict(size=8))
            ],
            layout=go.Layout(
                # Configuración de los ejes
                xaxis=dict(range=[-1, 1], autorange=False),
                yaxis=dict(range=[-1.5, 1.5], autorange=False),
                # Botones para controlar la animación
                updatemenus=[dict(type="buttons", showactive=False, buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 20}, "fromcurrent": True}])])],
            ),
            frames=frames  # Añadimos los frames creados
        )

        fig.show()
