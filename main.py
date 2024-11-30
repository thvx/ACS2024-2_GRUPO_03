from system.inverted_pendulum import InvertedPendulum
from system.animation import PendulumAnimation
from system.plot import plot_step_response

# Parámetros de prueba del sistema
car_mass = 1.0
pendulum_mass = 0.2
rod_length = 0.5
gravity = 9.81

# Función de transferencia para la ecuación (3)
transfer_function = {
    'numerator': [-1],
    'denominator': [car_mass * rod_length, 0, -(car_mass + pendulum_mass) * gravity]
}

# Inicializamos el sistema de péndulo invertido
inverted_pendulum = InvertedPendulum(transfer_function)

# Obtenemos datos de la respuesta al escalón
time_steps, response = inverted_pendulum.get_step_response_data()

# Creamos y mostramos la animación del péndulo invertido
animation = PendulumAnimation(time_steps, response, rod_length)
animation.show_animation()

# Mostramos el gráfico de la respuesta al escalón
plot_step_response(time_steps, response)
