import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class PendulumAnimation:
    def __init__(self, time_steps, response, rod_length):
        self.time_steps = time_steps
        self.response = response
        self.rod_length = rod_length

        # Configuración de la figura y el eje
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-1, 1)

        # Crear el carro y el péndulo
        self.car, = self.ax.plot([], [], 'ks-', lw=2, ms=10)
        self.pendulum_line, = self.ax.plot([], [], 'ro-', lw=2)
        self.wheels, = self.ax.plot([], [], 'ko', ms=5)

    def init_animation(self):
        self.car.set_data([], [])
        self.pendulum_line.set_data([], [])
        self.wheels.set_data([], [])
        return self.car, self.pendulum_line, self.wheels

    def animate(self, i):
        x = 0.5 * np.sin(self.time_steps[i])  # Simulamos el movimiento del carrito
        theta = self.response[i]

        # Coordenadas del carro
        self.car.set_data([x-0.1, x+0.1], [0, 0])

        # Coordenadas de las ruedas del carro
        wheel_x = [x-0.05, x+0.05, x-0.05, x+0.05]
        wheel_y = [-0.05, -0.05, 0.05, 0.05]
        self.wheels.set_data(wheel_x, wheel_y)

        # Ajustamos el ángulo para que el péndulo comience en la posición vertical invertida
        adjusted_theta = np.pi - theta

        # Coordenadas del péndulo
        pendulum_x = [x, x + self.rod_length * np.sin(adjusted_theta)]
        pendulum_y = [0, -self.rod_length * np.cos(adjusted_theta)]
        self.pendulum_line.set_data(pendulum_x, pendulum_y)

        return self.car, self.pendulum_line, self.wheels

    def show_animation(self):
        interval = 5000 / len(self.time_steps)  # Para que la animación dure 5 segundos
        animation_object = animation.FuncAnimation(self.fig, self.animate, init_func=self.init_animation, frames=len(self.time_steps), interval=interval, blit=True, repeat=False)

        # Mostramos la animación
        plt.title("Animación del Péndulo Invertido")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show(block=False)

        # Pausamos la ejecución del programa por 5 segundos para ver la animación
        plt.pause(5)
        plt.close(self.fig)
