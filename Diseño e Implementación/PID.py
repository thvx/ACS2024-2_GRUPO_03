import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# PARAMETROS DEL SISTEMA
M = 0            # El carrito no tiene masa
m = 1            # Masa del péndulo
l = 1            # Longitud del péndulo
g = 9.8          # Gravedad
u = 0            # Fuerza

# FUNCION DE TRANSFERENCIA
numtf = [-1]                   # Numerador
dentf = [M*l, 0, -(M+m)*g]     # Denominador
G = ctrl.TransferFunction(numtf, dentf)  # Función de transferencia

# CONTROLADOR PID SIN SINTONIZAR
K_p = 100     # Constante proporcional
K_i = 75      # Constante integral
K_d = 10      # Constante derivativa
C_no_sintonizado = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])  # Transfer Function PID

# SISTEMA DE FEEDBACK
T_no_sintonizado = ctrl.feedback(G * C_no_sintonizado)

# GRAFICA DE LAS RAICES DEL PID
plt.figure(1)
ctrl.root_locus(T_no_sintonizado)
plt.title('Raices del PID sin sintonizar')

# GRAFICA DE LA RESPUESTA AL IMPULSO
plt.figure(2)
t = np.linspace(0, 5, 500)  # Tiempo de simulación a 5 segundos
time, response = ctrl.impulse_response(T_no_sintonizado, T=t)  # Respuesta al impulso

# Invertir la respuesta al impulso para que coincida con MATLAB
response = -response

plt.plot(time, response)
plt.ylim(-2, 2)  # Establecer límites del eje Y entre -2 y 2
plt.title('Resultado respecto al Ángulo θ')

# Para sintonizar automáticamente el PID, usamos la librería control (o en su defecto un enfoque manual)
# Aquí solo actualizamos las constantes manualmente para simular una sintonización
K_p = 0
K_i = 9.8
K_d = 0
C_sintonizado = ctrl.TransferFunction([K_d, K_p, K_i], [1, 0])  # Transfer Function PID

# SISTEMA DE FEEDBACK SINTONIZADO
T_sintonizado = ctrl.feedback(G * C_sintonizado)

# GRAFICA DE LAS RAICES DEL PID SINTONIZADO
plt.figure(3)
ctrl.root_locus(T_sintonizado)
plt.title('Lugar geométrico de las raíces PID sintonizado')

# GRAFICA DE LA RESPUESTA AL IMPULSO SINTONIZADO
plt.figure(4)
time, response = ctrl.impulse_response(T_sintonizado, T=t)  # Respuesta al impulso

# Invertir la respuesta al impulso para que coincida con MATLAB
response = -response

plt.plot(time, response)
plt.ylim(-2, 2)  # Establecer límites del eje Y entre -2 y 2
plt.title('Respuesta péndulo mejorado respecto al Ángulo θ')

# GRAFICA DE COMPARACION DE LA RESPUESTA DEL IMPULSO
plt.figure(5)
time, response_no_sintonizado = ctrl.impulse_response(T_no_sintonizado, T=t)
time, response_sintonizado = ctrl.impulse_response(T_sintonizado, T=t)

# Invertir la respuesta al impulso para que coincida con MATLAB
response_no_sintonizado = -response_no_sintonizado
response_sintonizado = -response_sintonizado

plt.plot(time, response_no_sintonizado, 'b', label='PID no sintonizado')
plt.plot(time, response_sintonizado, 'r', label='PID sintonizado')
plt.legend()
plt.ylim(-2, 2)  # Establecer límites del eje Y entre -2 y 2
plt.title('Comparación de respuestas al impulso')

# Mostrar las gráficas
plt.show()
