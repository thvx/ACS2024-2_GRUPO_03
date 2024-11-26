import gymnasium as gym
from PIDController import PIDController

# Inicializa el entorno CartPole
env = gym.make("CartPole-v1", render_mode="human")

# Parámetros del PID para el ángulo del péndulo
pid = PIDController(kp=5.0, ki=0.1, kd=2.0, setpoint=0.0)  # Setpoint: mantener el péndulo vertical

# Inicializa el entorno
observation, info = env.reset()
dt = 0.02  # Paso de tiempo entre frames (Gymnasium usa aproximadamente 50 fps)

try:
    for _ in range(2000):
        # Obtén la posición y el ángulo del sistema
        cart_position, cart_velocity, pole_angle, pole_angular_velocity = observation

        # El controlador PID controla el ángulo del péndulo
        control_signal = pid.update(pole_angle, dt)

        # Traducir la señal del controlador a una acción discreta
        # Gymnasium solo admite acciones discretas {0: empuje izquierda, 1: empuje derecha}.
        action = 1 if control_signal > 0 else 0

        # Realiza un paso en el entorno con la acción
        observation, reward, done, truncated, info = env.step(action)

        # Reinicia el entorno si termina el episodio
        if done or truncated:
            observation, info = env.reset()

finally:
    env.close()
