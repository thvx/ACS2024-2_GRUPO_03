from system.inverted_pendulum import InvertedPendulum

# Parámetros de prueba
car_mass = 1.0
pendulum_mass = 0.2
rod_length = 0.5
gravity = 9.81

# Función de transferencia para la ecuación (3): θ(s)/u(s) = -1 / (M*l * s^2 - (M+m)*g)
transfer_function = {
    'numerator': [-1],
    'denominator': [car_mass * rod_length, 0, -(car_mass + pendulum_mass) * gravity]
}

inverted_pendulum = InvertedPendulum(transfer_function)

# Graficar la respuesta al escalón
inverted_pendulum.plot_step_response()