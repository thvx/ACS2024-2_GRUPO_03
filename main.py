from system.inverted_pendulum import InvertedPendulum
from system.animation import PendulumAnimation
from optimization.Optimization import PIDOptimizer
from design_implementation.PID import PendulumSystem

# Parámetros del sistema
car_mass = 1.0
pendulum_mass = 0.2
rod_length = 0.5
gravity = 9.81

# Funciones de transferencia
transfer_function_1 = {
    'numerator': [-1],
    'denominator': [car_mass * rod_length, 0, -(car_mass + pendulum_mass) * gravity]
}

transfer_function_2 = {
    'numerator': [rod_length, 0, -gravity],
    'denominator': [rod_length * car_mass, 0, -(car_mass + pendulum_mass) * gravity, 0, 0]
}

# Sistemas de péndulo invertido
pendulum_1 = InvertedPendulum(transfer_function_1)
pendulum_2 = InvertedPendulum(transfer_function_2)

# Sin PID
print("Sin PID:")
time_1_open, response_1_open = pendulum_1.simulate_without_pid()
pendulum_1.plot_response(time_1_open, response_1_open, "Respuesta sin PID (Sistema 1)")
animation_1_open = PendulumAnimation(time_1_open, response_1_open, rod_length)
animation_1_open.create_animation()

# Con PID
print("Con PID:")
K_p, K_i, K_d = 5, 0.001, 0.02
time_1_pid, response_1_pid = pendulum_1.simulate_with_pid(K_p, K_i, K_d)
pendulum_1.plot_response(time_1_pid, response_1_pid, "Respuesta con PID (Sistema 1)")
animation_1_pid = PendulumAnimation(time_1_pid, response_1_pid, rod_length)
animation_1_pid.create_animation()

optimizer = PIDOptimizer(transfer_function_1)
optimized_params = optimizer.optimize_pid()

K_p_optimized, K_i_optimized, K_d_optimized = optimizer.simulate_with_optimized_pid(*optimized_params)
time_1_optimized, response_1_optimized = pendulum_1.simulate_with_pid(K_p_optimized, K_i_optimized, K_d_optimized)
pendulum_1.plot_response(time_1_optimized, response_1_optimized, "Respuesta con PID Optimizado (Sistema 1)")
animation_1_optimized = PendulumAnimation(time_1_optimized, response_1_optimized, rod_length)
animation_1_optimized.create_animation()