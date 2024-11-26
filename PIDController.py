class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp  # Ganancia proporcional
        self.ki = ki  # Ganancia integral
        self.kd = kd  # Ganancia derivativa
        self.setpoint = setpoint  # Punto de referencia (setpoint)
        self.integral = 0
        self.prev_error = 0

    def update(self, measurement, dt):
        # Error entre el punto de referencia y la medición actual
        error = self.setpoint - measurement

        # Componente integral
        self.integral += error * dt

        # Componente derivativa
        derivative = (error - self.prev_error) / dt

        # Salida del controlador PID
        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Actualizar el error previo
        self.prev_error = error

        return output
