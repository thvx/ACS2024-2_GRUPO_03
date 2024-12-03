from system.inverted_pendulum import InvertedPendulum
from system.plot import plot_step_response
from system.animation import PendulumAnimation

# Parámetros de prueba del sistema
car_mass = 1.0
pendulum_mass = 0.2
rod_length = 0.5
gravity = 9.81

# Función de transferencia para la ecuación (3)
transfer_function_1 = {
    'numerator': [-1],
    'denominator': [car_mass * rod_length, 0, -(car_mass + pendulum_mass) * gravity]
}

# Función de transferencia adicional con el término correcto
transfer_function_2 = {
    'numerator': [rod_length, 0, -gravity],
    'denominator': [rod_length * car_mass, 0, -(car_mass + pendulum_mass) * gravity, 0, 0]
}

# Inicializamos los sistemas de péndulo invertido
inverted_pendulum_1 = InvertedPendulum(transfer_function_1)
inverted_pendulum_2 = InvertedPendulum(transfer_function_2)

# Obtenemos datos de la respuesta al escalón
time_steps_1, response_1 = inverted_pendulum_1.get_step_response_data()
time_steps_2, response_2 = inverted_pendulum_2.get_step_response_data()

# Creamos y mostramos la animación del primer péndulo invertido
animation_1 = PendulumAnimation(time_steps_1, response_1, rod_length)
animation_1.create_animation()

# Mostramos el gráfico de la respuesta al escalón para el primer sistema
plot_step_response(time_steps_1, response_1)

# Creamos y mostramos la animación del segundo péndulo invertido
animation_2 = PendulumAnimation(time_steps_2, response_2, rod_length)
animation_2.create_animation()

# Mostramos el gráfico de la respuesta al escalón para el segundo sistema
plot_step_response(time_steps_2, response_2)
